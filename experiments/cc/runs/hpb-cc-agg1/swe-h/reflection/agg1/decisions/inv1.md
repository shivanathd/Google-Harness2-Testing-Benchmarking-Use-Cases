KEEP_BASE. I made no edits to the harness.

I read the task, the ISSUE and source files, the one rollout (base1) and its deliverables. The base run worked cleanly:
- **Sequencing:** it read all the files first. It stated a plan with a check for each step, then edited the three modules.
- **Verification:** it ran a throwaway script outside the workspace that covered the missing and empty file cases, each error path (file unchanged, exit 1, `error:` on stderr) and `--low` ordering. It also called the existing test directly.
- **Deliverable:** it wrote `output/CHANGES.md`. The file is complete. It matches the final summary and says plainly that pytest could not run.

The only friction was in the pytest step. At `[ACTION] Bash python -m pytest tests -q` the sandbox raised PermissionError on parent and home paths such as `~/.aws`. The agent retried once with a pinned rootdir, then fell back to calling `test_add_then_file` directly with a temp path. That cost two commands and ended in a sound fallback. Prose would not have changed the outcome, and this is a single environmental quirk, not a recurring failure.

I did not add a skill, script, plugin or always-on text. Each would cost context and change no behaviour that the trajectory shows needs changing. The CHANGES.md shape was not constrained beyond "short summary", and the agent met it.