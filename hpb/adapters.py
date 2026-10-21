"""Harness² adapters for HPB with two executors: Claude Code (`claude -p`) and an ADK agent.

Harness² core is used unmodified; only the BenchmarkAdapter seam and the improver's process
launch are supplied here. Every model-driven process (executor rollouts and improver
sessions) runs with an allow-listed environment inside a macOS sandbox-exec profile that
denies reads of the grader code, other experiment runs and credential stores, and denies
writes outside its own workspace.
"""

from __future__ import annotations

import dataclasses
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path

from harness2.core import tree as HT
from harness2.core.proposer import Proposer, _parse_json
from harness2.core.spec import BenchPrompts, BenchSpec, ChannelSpec
from harness2.substrate.opencode import OPENCODE_SURFACE

import bench

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPERIMENTS = ROOT / "experiments"
ADK_PY = ROOT / "adk-venv/bin/python"
EMPTY_MCP = ROOT / "tools" / "empty_mcp.json"  # outside the sandbox-denied hpb/
EXECUTOR_MODEL = {"cc": "claude-haiku-5-5", "adk": "ollama_chat/qwen3:8b"}
IMPROVER_MODEL = os.environ.get("HPB_IMPROVER", "claude-sonnet-5-5")
CC_MAX_TURNS = int(os.environ.get("HPB_CC_MAX_TURNS", "40"))  # ablation: lower it for headroom
HOME = Path.home()

# OpenCode's surface minus subagents. c8 is a Claude Code style Stop hook in hooks.json, which
# both executors honour (CC natively; adk_agent.py re-prompts the model). harness2 core only
# knows plugins as plugin/<name>.ts, so plugin_dir stays on the surface and validate_tree turns a
# .ts plugin into retry feedback pointing at hooks.json. The name must stay "opencode":
# harness2's prompt builder keys on it.
HOOKS_FILE = "hooks.json"
C8_HELP = (
    "c8 in this rig: OpenCode plugins (plugin/<name>.ts) are NOT run by either executor. Enforce "
    f"in-loop behaviour with {HOOKS_FILE} at the harness root, in Claude Code hooks format with "
    'the Stop event only, e.g. {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": '
    '"python3 scripts/check_output.py"}]}]}}. When the agent tries to finish, each command runs '
    "in the workspace; exit 2 blocks finishing and its stderr is sent to the agent as its next "
    "instruction (at most 3 times); any other exit lets it finish."
)
SURFACE = dataclasses.replace(
    OPENCODE_SURFACE,
    hooks_file=HOOKS_FILE,
    hook_events=frozenset({"Stop"}),
    stubs=tuple(s for s in OPENCODE_SURFACE.stubs if s[0] in ("scripts/README.md",
                                                              "skills/README.md"))
    + (("plugin/README.md", f"<!-- {C8_HELP} -->\n"),),
)

# A block that records this instance's computed results ("Workspace facts (verified here): ...").
FACT_RX = re.compile(r"(?i)workspace facts?\b|task instance|reference check for this workspace"
                     r"|verified (?:here|in this workspace|on the files)")
_CUR = threading.local()  # the task the current proposing thread is building evidence for

BASE_SYSTEM = (
    "You are an assistant that completes tasks inside a workspace directory. Read the task, "
    "do the work, and write the requested deliverables under output/.\n"
)

DOMAIN_PROMPTS = {
    "data": BenchPrompts(work="reconcile payment and finance exports into revenue figures",
                         domain_word="data domain"),
    "ops": BenchPrompts(work="analyse service logs into incident and traffic statistics",
                        domain_word="ops domain"),
    "swe": BenchPrompts(work="resolve issues in small Python codebases without breaking them",
                        domain_word="software domain"),
}

_ENV_KEEP = ("PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL", "TERM", "TMPDIR")


def base_env() -> dict[str, str]:
    """Allow-list: no tokens, keys or agent sockets reach model-driven processes."""
    env = {k: os.environ[k] for k in _ENV_KEEP if k in os.environ}
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    return env


def sandboxed(cmd: list[str], *, read_ok=(), write_ok=()) -> list[str]:
    """Wrap cmd in a sandbox-exec profile (macOS Seatbelt)."""
    q = lambda p: '"' + str(p).replace('"', '') + '"'
    deny_read = [HERE, EXPERIMENTS, ROOT / ".git", HOME / ".ssh", HOME / ".config/gcloud", HOME / ".aws",
                 HOME / ".config/gh", HOME / ".docker", HOME / ".gnupg",
                 # reviewer recompute scripts and this operator session's transcripts
                 Path("/private/tmp/hpb_review"),
                 Path("/private/tmp/claude-502/-Users-me-GoogleHarness2")]
    profile = "\n".join([
        "(version 1)", "(allow default)",
        "(deny file-read* " + " ".join(f"(subpath {q(d)})" for d in deny_read)
        + f" (literal {q(HOME / '.netrc')}) (literal {q(HOME / '.git-credentials')}))",
        *(f"(allow file-read* (subpath {q(r)}))" for r in read_ok),
        # stat() of the ancestors only: CC refuses project settings whose path it cannot vet
        *(f"(allow file-read-metadata (literal {q(a)}))" for r in read_ok for a in Path(r).parents),
        "(deny file-write*)",
        "(allow file-write* " + " ".join(f"(subpath {q(w)})" for w in write_ok)
        + f' (subpath "/private/tmp") (subpath "/private/var/folders")'
        + f" (subpath {q(HOME / '.claude')}) (subpath {q(HOME / 'Library/Caches')})"
        + f' (regex #"^{HOME}/\\.claude\\.json") (literal "/dev/null")'
        + ' (regex #"^/dev/(tty|fd/)"))',
    ])
    return ["sandbox-exec", "-p", profile, *cmd]


def isolated_claude(model: str) -> list[str]:
    """`claude -p` without the operator's settings, hooks, plugins, MCP servers, web tools
    or persisted sessions."""
    if not EMPTY_MCP.exists():
        EMPTY_MCP.write_text('{"mcpServers": {}}\n')
    return [shutil.which("claude") or "claude", "-p", "--model", model,
            "--setting-sources", "project", "--strict-mcp-config",
            "--mcp-config", str(EMPTY_MCP), "--dangerously-skip-permissions",
            "--no-session-persistence", "--disallowedTools", "WebFetch", "WebSearch"]


AUTH_FAIL = ("Not logged in", "Please run /login", "Invalid API key", "OAuth token has expired",
             "Failed to authenticate", "OAuth session expired", "could not be refreshed")


def _auth_failed(text: str) -> bool:
    return any(k in (text or "") for k in AUTH_FAIL)


def _stream_result(stdout: str) -> dict:
    for line in reversed(stdout.splitlines()):
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "result":
            return ev
    return {}


class LocalClaudeProposer(Proposer):
    """harness2's claude_cli channel on the local CLI login, sandboxed, with every session's
    tool calls kept (stream-json) for the leak audit."""

    def env(self) -> dict[str, str]:
        return base_env()

    def _claude_cli(self, cwd: Path, mission: str, system: str, wall: int):
        cmd = isolated_claude(self.spec.model) + ["--output-format", "stream-json", "--verbose",
                                                  "--effort", self.spec.effort]
        if system:
            cmd += ["--append-system-prompt", system]
        for attempt in range(5):  # concurrent CLIs can race on the OAuth refresh
            with _CLAUDE_SLOTS:
                p = subprocess.run(sandboxed(cmd, write_ok=[cwd]), input=mission, cwd=cwd,
                                   env=self.env(), text=True, capture_output=True, timeout=wall)
            if not _auth_failed(str(_stream_result(p.stdout).get("result"))):
                break
            time.sleep(20 * (attempt + 1))
        if self.audit_dir:
            d = Path(self.audit_dir) / "streams"
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{time.time_ns()}.jsonl").write_text(p.stdout)
        payload = _stream_result(p.stdout) or _parse_json(p.stdout)
        text = str(payload.get("result") or "")
        err = ""
        if _auth_failed(text):
            err, text = f"CLI auth failure: {text[:80]}", ""
        elif payload.get("is_error") or payload.get("subtype") not in (None, "success"):
            err, text = f"CLI error: {payload.get('subtype')} {text[:200]}", ""
        elif p.returncode != 0 and not text.strip():
            err = f"rc={p.returncode}: {(p.stderr or '')[-300:]}"
        return text, float(payload.get("total_cost_usd") or 0.0), err


class Substrate:
    def __init__(self, name: str):
        self.name = name

    def surface(self):
        return SURFACE


def always_on_text(harness: Path) -> str:
    parts = []
    for rel in SURFACE.always_on:
        f = harness / rel
        if f.is_file() and f.read_text().strip():
            parts.append(f"## {rel}\n\n{f.read_text().strip()}")
    return "\n\n".join(parts)


def harness_fingerprint(harness: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(p for p in Path(harness).rglob("*") if p.is_file()):
        h.update(str(f.relative_to(harness)).encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()[:16]


class _Slots:
    """Cross-process cap on concurrent local-model rollouts (one lock file per slot), so
    queueing inside Ollama never turns into agent timeouts."""

    def __init__(self, n: int, d: Path):
        self.files = [d / f"slot{i}.lock" for i in range(n)]
        d.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        while True:
            for f in self.files:
                fh = open(f, "a")
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    _HELD.h = fh
                    return self
                except BlockingIOError:
                    fh.close()
            time.sleep(2)

    def __exit__(self, *exc):
        fcntl.flock(_HELD.h, fcntl.LOCK_UN)
        _HELD.h.close()


_HELD = threading.local()
_ADK_SLOTS = _Slots(int(os.environ.get("HPB_ADK_SLOTS", "8")), ROOT / "tools" / "slots")
# every `claude -p` (executor rollouts and improver sessions), across processes: the host is shared
_CLAUDE_SLOTS = _Slots(int(os.environ.get("HPB_CLAUDE_SLOTS", "4")), ROOT / "tools" / "claude-slots")


class HPBAdapter:
    """BenchmarkAdapter for HPB; `executor` is "cc" (Claude Code) or "adk"."""

    def __init__(self, executor: str, root: Path, rollout_timeout: int | None = None):
        assert executor in EXECUTOR_MODEL
        self.executor = executor
        self.root = Path(root)
        self.exec_root = self.root / "exec"
        self.rollout_timeout = rollout_timeout or (900 if executor == "cc" else 1500)
        self.max_turns = CC_MAX_TURNS if executor == "cc" else 40  # ADK: adk_agent --max-calls 40
        self.substrate = Substrate(executor)
        channel = ChannelSpec("claude_cli", IMPROVER_MODEL, effort="high", timeout=1800)
        self.spec = BenchSpec(
            name="hpb",
            runs_root=self.root / "runs",
            install_mode="workspace_config",
            prompts=DOMAIN_PROMPTS["data"],
            channels={"proposer": channel, "selector": channel},
        )
        if not (self.base_harness() / "systemprompt.md").is_file():  # concurrent processes share it
            base = {name: "" for name in SURFACE.always_on}
            base["systemprompt.md"] = BASE_SYSTEM
            HT.write_tree(SURFACE, base, self.base_harness(), stubs=False)
        stamp = self.root / "sources.hash"
        if not stamp.is_file() or stamp.read_text() != bench.TASK_HASH:
            shutil.rmtree(self.root / "sources", ignore_errors=True)
            for tid in bench.TASKS:
                bench.write_task_files(tid, self.task_files(tid))
            stamp.write_text(bench.TASK_HASH)

    # ---- task description
    def tasks(self, split: str = "all") -> list[str]:
        return [t for t, v in bench.TASKS.items() if not v["variant"]]

    def domain_of(self, task_id: str) -> str:
        return bench.TASKS[task_id]["domain"]

    def prompts_for(self, task_id: str) -> BenchPrompts:
        return DOMAIN_PROMPTS[self.domain_of(task_id)]

    def task_prompt(self, task_id: str) -> str:
        # harness2 calls this from context.build, in the same thread and just before that
        # stage's proposal reaches validate_tree; that is how validate_tree knows its task.
        _CUR.task = task_id
        return bench.TASKS[task_id]["prompt"]

    def task_files(self, task_id: str) -> Path:
        return self.root / "sources" / task_id

    def base_harness(self) -> Path:
        return self.root / "base_harness"

    def validate_tree(self, tree: dict[str, str]) -> None:
        """Reject OpenCode plugins (not run here) and answer leaks: the current task's own
        expected values or instance ids (the PREREG leak rule, bench.leaked) and "workspace
        fact" blocks. harness2 retries the proposal once with this message, then falls back."""
        task = getattr(_CUR, "task", None)
        errs = []
        for rel, src in sorted(tree.items()):
            if rel.startswith("plugin/"):
                errs.append(f"{rel}: {C8_HELP}")
            for t in [task] if task else self.tasks():
                hits = bench.leaked(src, t)
                if hits:
                    ctx = [m.group(0) for x in hits[:6] for m in [re.search(
                        rf".{{0,30}}(?<![\w.]){re.escape(x)}(?![\w]).{{0,30}}", src)] if m]
                    errs.append(f"{rel} contains values or ids of this task's own data "
                                f"({', '.join(hits[:15])}), e.g. {' / '.join(map(repr, ctx))}. "
                                "A harness must teach the method, never record this instance's "
                                "results, ids, counts or time windows; remove them.")
            facts = sorted({m.group(0) for m in FACT_RX.finditer(src)})
            if facts:
                errs.append(f"{rel} has a workspace-fact block ({', '.join(facts)}): drop facts "
                            "about this instance's files; keep only checks the agent re-derives.")
        if task and os.environ.get("HPB_LEAKGUARD") == "2":  # second layer: hpb/leakguard.py
            import leakguard
            found = leakguard.scan_tree(tree, leakguard._hpb_instance(self.root, task))
            if found:
                errs.append(leakguard.message(found))
        if errs:
            raise ValueError(" | ".join(errs))

    # ---- execution
    def execute(self, task_id: str, harness_dir: Path | None, run_id: str, *,
                timeout: int | None = None) -> Path:
        """Idempotent by (run_id, harness, task data); infrastructure failures are retried."""
        run_dir = self.exec_root / run_id
        harness = Path(harness_dir or self.base_harness())
        fp = harness_fingerprint(harness)
        meta_f = run_dir / "meta.json"
        if meta_f.is_file():
            old = json.loads(meta_f.read_text())
            if old.get("harness_fp") == fp and old.get("task_hash") == bench.TASK_HASH \
                    and old.get("max_turns", 40) == self.max_turns \
                    and not old.get("infra_error") and not self._is_infra(old, run_dir):
                return run_dir
        for attempt in range(1, 4):
            shutil.rmtree(run_dir, ignore_errors=True)
            work = run_dir / "work"
            shutil.copytree(self.task_files(task_id), work)
            t0 = time.time()
            run = self._run_cc if self.executor == "cc" else self._run_adk
            run(harness, work, run_dir, self.task_prompt(task_id), timeout or self.rollout_timeout)
            meta = json.loads(meta_f.read_text()) if meta_f.is_file() else {"error": "no meta"}
            meta.update(task=task_id, harness=str(harness), harness_fp=fp,
                        task_hash=bench.TASK_HASH, max_turns=self.max_turns, wall_s=round(time.time() - t0, 1),
                        attempt=attempt, infra_error=self._is_infra(meta, run_dir))
            meta_f.write_text(json.dumps(meta, indent=2))
            if not meta["infra_error"]:
                break
            time.sleep(20 * attempt)
        return run_dir

    def _is_infra(self, meta: dict, run_dir: Path | None = None) -> bool:
        """Errors of the plumbing, not the agent. Timeouts and turn limits are agent failures."""
        if self.executor == "cc":
            text = meta.get("result_text")
            if text is None and run_dir is not None and (Path(run_dir) / "stream.jsonl").is_file():
                text = str(_stream_result((Path(run_dir) / "stream.jsonl").read_text()).get("result"))
            if _auth_failed(text or ""):
                return True
        err = str(meta.get("error") or "")
        if not err or err == "timeout" or "LlmCallsLimitExceeded" in err:
            return False
        if self.executor == "cc":
            return not meta.get("subtype")  # the CLI never produced a result event
        return any(k in err for k in ("APIConnectionError", "ServiceUnavailable", "Connection",
                                      "InternalServerError", "no meta", "Timeout"))

    def _run_cc(self, harness: Path, work: Path, run_dir: Path, prompt: str, timeout: int):
        (work / "CLAUDE.md").write_text(always_on_text(harness) + "\n")
        if (harness / HOOKS_FILE).is_file():  # c8: the same document is CC's hooks setting
            (work / ".claude").mkdir(exist_ok=True)
            shutil.copy(harness / HOOKS_FILE, work / ".claude/settings.json")
        for sk in (harness / "skills").glob("*/SKILL.md"):
            shutil.copytree(sk.parent, work / ".claude/skills" / sk.parent.name, dirs_exist_ok=True)
        scripts = list((harness / "scripts").glob("*.py"))
        if scripts:
            (work / "scripts").mkdir(exist_ok=True)
            for s in scripts:
                shutil.copy(s, work / "scripts" / s.name)
        cmd = isolated_claude(EXECUTOR_MODEL["cc"]) + ["--output-format", "stream-json",
                                                       "--verbose", "--max-turns", str(self.max_turns)]
        meta = {"error": ""}
        try:
            with _CLAUDE_SLOTS:
                p = subprocess.run(sandboxed(cmd, read_ok=[work], write_ok=[work]), input=prompt,
                                   cwd=work, env=base_env(), text=True, capture_output=True,
                                   timeout=timeout)
            (run_dir / "stream.jsonl").write_text(p.stdout)
            ev = _stream_result(p.stdout)
            if ev:
                u = ev.get("usage") or {}
                meta.update(cost_usd=ev.get("total_cost_usd"), turns=ev.get("num_turns"),
                            subtype=ev.get("subtype"), result_text=str(ev.get("result"))[:200],
                            tokens_in=sum(u.get(k) or 0 for k in ("input_tokens",
                                          "cache_read_input_tokens", "cache_creation_input_tokens")),
                            tokens_out=u.get("output_tokens"))
                if ev.get("subtype") != "success":
                    meta["error"] = str(ev.get("subtype"))
            elif p.returncode:
                meta["error"] = (p.stderr or "")[-400:] or f"rc={p.returncode}"
        except subprocess.TimeoutExpired:
            meta["error"] = "timeout"
        (run_dir / "meta.json").write_text(json.dumps(meta))

    def _run_adk(self, harness: Path, work: Path, run_dir: Path, prompt: str, timeout: int):
        (run_dir / "prompt.txt").write_text(prompt)
        cmd = [str(ADK_PY), str(HERE / "adk_agent.py"), "--harness", str(harness),
               "--work", str(work), "--prompt-file", str(run_dir / "prompt.txt"),
               "--out", str(run_dir), "--model", EXECUTOR_MODEL["adk"]]
        env = base_env() | {"OLLAMA_API_BASE": "http://127.0.0.1:11434"}
        cmd = sandboxed(cmd, read_ok=[HERE / "adk_agent.py", harness, run_dir],
                        write_ok=[run_dir])
        with _ADK_SLOTS:
            try:
                p = subprocess.run(cmd, env=env, text=True, capture_output=True, timeout=timeout)
                if not (run_dir / "meta.json").is_file():
                    (run_dir / "meta.json").write_text(json.dumps({"error": "no meta: " + p.stderr[-600:]}))
            except subprocess.TimeoutExpired:
                (run_dir / "meta.json").write_text(json.dumps({"error": "timeout"}))

    # ---- observation
    def delivered(self, run_dir: Path) -> bool:
        out = Path(run_dir) / "work/output"
        return out.is_dir() and any(p.is_file() for p in out.rglob("*"))

    def _events(self, run_dir: Path) -> list[dict]:
        run_dir = Path(run_dir)
        if (run_dir / "trajectory.jsonl").is_file():
            return [json.loads(x) for x in (run_dir / "trajectory.jsonl").read_text().splitlines()]
        events = []
        for line in (run_dir / "stream.jsonl").read_text().splitlines() if (run_dir / "stream.jsonl").is_file() else []:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            for c in (ev.get("message") or {}).get("content") or []:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use":
                    events.append({"type": "action", "tool": c.get("name"), "input": c.get("input")})
                elif c.get("type") == "tool_result":
                    body = c.get("content")
                    if isinstance(body, list):
                        body = "\n".join(b.get("text", "") for b in body if isinstance(b, dict))
                    events.append({"type": "observation", "text": str(body)})
                elif c.get("type") == "text" and ev.get("type") == "assistant":
                    events.append({"type": "assistant", "text": c.get("text", "")})
        return events

    def _sanitize(self, text: str, run_dir: Path) -> str:
        return (text.replace(str(Path(run_dir) / "work"), ".")
                .replace(str(self.root), "<runs>").replace(str(ROOT), "<root>"))

    def trajectory(self, run_dir: Path, *, obs_trunc: int) -> str:
        return self._sanitize(self._trajectory(run_dir, obs_trunc=obs_trunc), run_dir)

    def _trajectory(self, run_dir: Path, *, obs_trunc: int) -> str:
        out = []
        for e in self._events(run_dir):
            if e["type"] == "action":
                out.append(f"[ACTION] {e['tool']} {json.dumps(e['input'])[:1500]}")
            elif e["type"] == "observation":
                out.append(f"[OBSERVATION]\n{e['text'][:obs_trunc]}")
            elif e["type"] == "error":
                out.append(f"[ERROR] {e['text']}")
            elif e["type"] == "hook":
                out.append(f"[STOP HOOK BLOCKED FINISHING] {e['text'][:obs_trunc]}")
            else:
                out.append(f"[ASSISTANT] {e['text'][:4000]}")
        return "\n".join(out) or "[ERROR] no trajectory recorded"

    def deliverable_files(self, run_dir: Path) -> dict[str, str]:
        """output/* plus, for code tasks, every source file the agent changed."""
        work = Path(run_dir) / "work"
        files = {}
        out = work / "output"
        for p in sorted(out.rglob("*")) if out.is_dir() else []:
            if p.is_file():
                files[str(p.relative_to(work))] = p.read_text(errors="replace")[:20000]
        task = json.loads((Path(run_dir) / "meta.json").read_text()).get("task", "")
        if task and bench.TASKS[task]["pkg"]:
            for rel, orig in bench.TASKS[task]["files"].items():
                p = work / rel
                if rel.endswith(".py") and p.is_file() and p.read_text(errors="replace") != orig:
                    files[rel] = p.read_text(errors="replace")[:20000]
        return files

    def deliverable_text(self, run_dir: Path) -> str:
        return "\n\n".join(f"### {k}\n{v}" for k, v in self.deliverable_files(run_dir).items())

    def score(self, run_dir: Path, task_id: str) -> dict | None:
        return bench.grade(Path(run_dir) / "work", task_id)


def _selfcheck() -> None:
    """validate_tree rejects study-1 style leaks for the current task only, and .ts plugins."""
    import tempfile
    ad = HPBAdapter("adk", Path(tempfile.mkdtemp()))
    ok = {"systemprompt.md": "Recount errors per request.",
          HOOKS_FILE: '{"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "ls output"}]}]}}'}

    def rejected(tree, task):
        ad.task_prompt(task)  # what harness2's context.build does before validating
        try:
            ad.validate_tree(tree)
        except ValueError as exc:
            return str(exc)
        return ""
    fact = "- Workspace fact (this app.log): errors=15, users=6, top_code=E500"
    assert not rejected(ok, "ops-e")
    assert "E500" in rejected(ok | {"skills/x/SKILL.md": "top_code=E500"}, "ops-e")
    assert "workspace-fact" in rejected(ok | {"guardrails.md": "Workspace facts: recount."}, "ops-e")
    assert rejected(ok | {"guardrails.md": fact}, "ops-e")
    assert "T11007" in rejected(ok | {"LongTermMEMORY.md": "dupes: T11007"}, "data-e")
    assert not rejected(ok | {"LongTermMEMORY.md": "dupes: T11007"}, "ops-e")  # other task's id
    assert "hooks.json" in rejected(ok | {"plugin/stop.ts": "export const P = 1"}, "ops-e")
    print("validate_tree self-check ok")


if __name__ == "__main__":
    _selfcheck()
