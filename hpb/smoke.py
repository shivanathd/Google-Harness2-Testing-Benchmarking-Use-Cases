"""Smoke-test the hardened stack: one rollout per executor and one improver session."""
import json, sys, tempfile
from pathlib import Path
from adapters import HPBAdapter, LocalClaudeProposer
which = sys.argv[1]
root = Path(__file__).resolve().parent.parent / "experiments" / ("smoke-" + which)
if which in ("cc", "adk"):
    ad = HPBAdapter(which, root)
    rd = ad.execute("data-e", None, "smoke/data-e")
    print(which, json.loads((rd / "meta.json").read_text()), ad.score(rd, "data-e")["partial"])
    print(ad.trajectory(rd, obs_trunc=200)[:1500])
else:
    ad = HPBAdapter("cc", root)
    prop = LocalClaudeProposer(ad.spec.channels["proposer"], audit_dir=root / "audit")
    ctx = Path(tempfile.mkdtemp()); (ctx / "harness").mkdir(); (ctx / "harness" / "systemprompt.md").write_text("hi\n")
    r = prop.call(f"Append the line 'Check your work.' to context/harness/systemprompt.md, then try to `ls {Path(__file__).resolve().parent}` and reply <notes>result of ls</notes>.", ctx, "smoke.1", harvest="context/harness")
    print("improver:", r.ok, round(r.cost_usd, 4), r.text[-300:]); print((r.workspace / "systemprompt.md").read_text())
