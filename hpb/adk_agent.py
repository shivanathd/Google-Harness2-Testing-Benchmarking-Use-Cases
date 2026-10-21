"""A small Google ADK coding agent whose behaviour is set by a Harness² tree.

Run with the ADK venv:  adk-venv/bin/python adk_agent.py --harness H --work W --prompt-file P --out O
Harness mapping: always-on files -> instruction; skills/<n>/SKILL.md -> load_skill tool;
scripts/*.py -> copied into the workspace; hooks.json Stop hooks -> run when the model
finishes, and a command exiting 2 re-prompts it with its stderr (Claude Code semantics).
Every tool is confined to the workspace.
"""

from __future__ import annotations

import argparse
import asyncio
import functools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.agents.run_config import RunConfig
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

ALWAYS_ON = ("systemprompt.md", "guardrails.md", "LongTermMEMORY.md",
             "tool_descriptions/tool_guidance.md")
OUT_CAP = 6000
MAX_STOP_BLOCKS = 3


def stop_hook(harness: Path, work: Path) -> str | None:
    """Run hooks.json Stop commands in the workspace; the stderr of the first one that exits 2
    (blocks finishing), else None. Malformed hooks or other exits never block."""
    try:
        entries = json.loads((harness / "hooks.json").read_text())["hooks"].get("Stop", [])
        cmds = [h["command"] for e in entries for h in e["hooks"] if h.get("type") == "command"]
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None
    for cmd in cmds:
        try:
            p = subprocess.run(["bash", "-lc", cmd], cwd=work, capture_output=True, text=True,
                               timeout=60, input=json.dumps({"hook_event_name": "Stop"}),
                               env={"PATH": os.environ["PATH"], "HOME": str(work)})
        except subprocess.TimeoutExpired:
            continue
        if p.returncode == 2:
            return (p.stderr.strip() or "A Stop hook blocked finishing.")[:OUT_CAP]
    return None


def compose_instruction(harness: Path, work: Path) -> tuple[str, dict[str, str]]:
    parts = []
    for rel in ALWAYS_ON:
        f = harness / rel
        if f.is_file() and f.read_text().strip():
            parts.append(f"## {rel}\n\n{f.read_text().strip()}")
    skills = {}
    for sk in sorted((harness / "skills").glob("*/SKILL.md")):
        body = sk.read_text()
        desc = re.search(r"^description:\s*(.+)$", body, re.M)
        skills[sk.parent.name] = body
        for extra in sk.parent.glob("scripts/*"):
            dest = work / "skills" / sk.parent.name / "scripts" / extra.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(extra, dest)
    if skills:
        parts.append("## Skills (call load_skill(name) before using one)\n\n" + "\n".join(
            f"- {n}: {(re.search(r'^description:\s*(.+)$', b, re.M) or [None, ''])[1]}"
            for n, b in skills.items()))
    scripts = sorted((harness / "scripts").glob("*.py"))
    if scripts:
        (work / "scripts").mkdir(exist_ok=True)
        for s in scripts:
            shutil.copy(s, work / "scripts" / s.name)
        parts.append("## Helper scripts (run with run_command, e.g. `python3 scripts/x.py`)\n\n"
                     + "\n".join(f"- scripts/{s.name}" for s in scripts))
    parts.append("## Tools\n\nYou work inside one workspace directory. Use list_files, "
                 "read_file, write_file and run_command (bash, cwd = workspace). "
                 "Finish only after the requested files exist under output/.")
    return "\n\n".join(parts), skills


def make_tools(work: Path, skills: dict[str, str], log: list):
    root = work.resolve()

    def _inside(path: str) -> Path:
        p = (root / path).resolve()
        if p != root and root not in p.parents:
            raise ValueError("path is outside the workspace")
        return p

    def list_files(path: str = ".") -> str:
        """List files under a workspace directory (recursive, up to 200 entries)."""
        base = _inside(path)
        if not base.is_dir():
            raise ValueError(f"no such directory: {path!r} (paths are relative to the workspace root)")
        names = [str(p.relative_to(root)) for p in sorted(base.rglob("*")) if p.is_file()]
        return "\n".join(names[:200]) or "(empty)"

    def read_file(path: str, start_line: int = 1, max_lines: int = 200) -> str:
        """Read lines [start_line, start_line+max_lines) of a workspace text file."""
        lines = _inside(path).read_text(errors="replace").splitlines()
        chunk = lines[max(0, start_line - 1): start_line - 1 + max_lines]
        return f"[{len(lines)} lines total]\n" + "\n".join(chunk)

    def write_file(path: str, content: str) -> str:
        """Create or overwrite a workspace file with content."""
        p = _inside(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"wrote {len(content)} chars to {path}"

    def run_command(command: str) -> str:
        """Run a bash command in the workspace (60 s timeout); returns exit code and output."""
        try:
            p = subprocess.run(["bash", "-lc", command], cwd=root, capture_output=True,
                               text=True, timeout=60,
                               env={"PATH": os.environ["PATH"], "HOME": str(root)})
            out = (p.stdout + p.stderr)[-OUT_CAP:]
            return f"exit={p.returncode}\n{out}"
        except subprocess.TimeoutExpired:
            return "exit=timeout"

    def load_skill(name: str) -> str:
        """Load the full instructions of a named skill."""
        return skills.get(name, f"no skill named {name!r}; available: {sorted(skills)}")

    def as_observation(fn):
        """ADK aborts the run on a tool exception; return the error to the model instead."""
        @functools.wraps(fn)
        def wrapped(*a, **kw):
            try:
                return fn(*a, **kw)
            except Exception as exc:
                return f"ERROR: {type(exc).__name__}: {exc}"
        return wrapped

    tools = [list_files, read_file, write_file, run_command]
    if skills:
        tools.append(load_skill)
    return [as_observation(t) for t in tools]


async def run(args) -> dict:
    work = Path(args.work)
    instruction, skills = compose_instruction(Path(args.harness), work)
    log: list[dict] = []
    agent = LlmAgent(
        name="hpb_agent",
        model=LiteLlm(model=args.model, think=False),  # qwen3: the /no_think tag is not honoured via LiteLLM
        instruction=lambda _ctx: instruction,  # provider form: no {state} templating
        tools=make_tools(work, skills, log),
    )
    svc = InMemorySessionService()
    runner = Runner(agent=agent, app_name="hpb", session_service=svc)
    session = await svc.create_session(app_name="hpb", user_id="u")
    text = Path(args.prompt_file).read_text()
    calls, err, tok_in, tok_out, llm_calls, blocks = 0, "", 0, 0, 0, 0
    traj = (Path(args.out) / "trajectory.jsonl").open("w")
    def emit(e):  # written as it happens, so a timeout still leaves evidence
        log.append(e)
        traj.write(json.dumps(e) + "\n")
        traj.flush()
    try:
        while True:  # one pass per user turn; a blocking Stop hook adds a turn
            msg = types.Content(role="user", parts=[types.Part.from_text(text=text)])
            cfg = RunConfig(max_llm_calls=args.max_calls - llm_calls)  # one budget for all turns
            async for ev in runner.run_async(user_id="u", session_id=session.id, new_message=msg,
                                             run_config=cfg):
                um = getattr(ev, "usage_metadata", None)
                if um:
                    tok_in += um.prompt_token_count or 0
                    tok_out += um.candidates_token_count or 0
                llm_calls += bool(ev.content and ev.content.role == "model")
                for part in (ev.content.parts if ev.content and ev.content.parts else []):
                    if part.function_call:
                        calls += 1
                        emit({"type": "action", "tool": part.function_call.name,
                                    "input": dict(part.function_call.args or {})})
                    elif part.function_response:
                        emit({"type": "observation",
                                    "text": str((part.function_response.response or {}).get("result",
                                                part.function_response.response))[:OUT_CAP]})
                    elif part.text and not getattr(part, "thought", False):
                        emit({"type": "assistant", "text": part.text[:OUT_CAP]})
            text = stop_hook(Path(args.harness), work)
            if text is None or blocks >= MAX_STOP_BLOCKS or llm_calls >= args.max_calls:
                break
            blocks += 1
            emit({"type": "hook", "text": text})
    except Exception as exc:  # call-limit, model or tool failure: record, never crash
        err = f"{type(exc).__name__}: {exc}"[:500]
        emit({"type": "error", "text": err})
    traj.close()
    return {"tool_calls": calls, "error": err, "tokens_in": tok_in, "tokens_out": tok_out,
            "instruction_chars": len(instruction), "llm_calls": llm_calls, "stop_blocks": blocks}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--harness", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="ollama_chat/qwen3:8b")
    ap.add_argument("--max-calls", type=int, default=40)
    args = ap.parse_args()
    t0 = time.time()
    res = asyncio.run(run(args))
    out = Path(args.out)
    res["secs"] = round(time.time() - t0, 1)
    (out / "meta.json").write_text(json.dumps(res, indent=2))


def _selfcheck() -> None:
    """The output/-exists Stop hook blocks with its message until output/ has a file."""
    with tempfile.TemporaryDirectory() as td:
        h, w = Path(td, "h"), Path(td, "w")
        (w / "output").mkdir(parents=True)
        h.mkdir()
        assert stop_hook(h, w) is None  # no hooks.json
        cmd = ('[ -n "$(ls -A output)" ] || { echo "Write output/answer.json before '
               'finishing." >&2; exit 2; }')
        (h / "hooks.json").write_text(json.dumps(
            {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": cmd}]}]}}))
        assert stop_hook(h, w) == "Write output/answer.json before finishing."
        (w / "output/answer.json").write_text("{}")
        assert stop_hook(h, w) is None
        (h / "hooks.json").write_text("not json")
        assert stop_hook(h, w) is None
    print("stop_hook self-check ok")


if __name__ == "__main__":
    _selfcheck() if sys.argv[1:] == ["--selfcheck"] else main()
