#!/usr/bin/env bash
# Set up the Harness² field-test rig on macOS.
#   scripts/setup.sh              Claude Code executor (the default arm)
#   scripts/setup.sh --with-adk   also the Google ADK + local qwen3:8b executor (needs Ollama)
#   scripts/setup.sh --with-lab   also Google's LAB legal tasks (harveyai/harvey-labs)
set -euo pipefail
cd "$(dirname "$0")/.."

H2_COMMIT=1cfe254e8d25b15f37048c3730134686abe60335   # google-research/harness2, the commit we tested
LAB_COMMIT=b58a28ae9fde5ee4b810e53b4fd0a1915325a35d  # harveyai/harvey-labs, as pinned by harness2
WITH_ADK=0; WITH_LAB=0
for a in "$@"; do
  case "$a" in
    --with-adk) WITH_ADK=1 ;;
    --with-lab) WITH_LAB=1 ;;
    *) echo "unknown option: $a (use --with-adk, --with-lab)"; exit 2 ;;
  esac
done

say() { printf '\n== %s\n' "$1"; }
need() { command -v "$1" >/dev/null || { echo "missing: $1. $2"; exit 1; }; }
fetch() {  # fetch <dir> <url> <commit>: shallow checkout of one commit; never overwrite another revision
  local dir=$1 url=$2 commit=$3
  if [ -d "$dir/.git" ]; then
    local at; at=$(git -C "$dir" rev-parse HEAD)
    [ "$at" = "$commit" ] || { echo "$dir is at $at, expected $commit. Move it aside and re-run."; exit 1; }
    echo "$dir already at ${commit:0:7}"
  else
    git init -q "$dir"
    git -C "$dir" remote add origin "$url"
    git -C "$dir" fetch -q --depth 1 origin "$commit"
    git -C "$dir" checkout -q FETCH_HEAD
    echo "$dir checked out at ${commit:0:7}"
  fi
}

say "Prerequisites"
[ "$(uname)" = Darwin ] || { echo "The rig isolates every agent with macOS sandbox-exec, so it runs on macOS only."; exit 1; }
need sandbox-exec "It ships with macOS."
need git "Install the Xcode command line tools: xcode-select --install"
need uv "Install it: brew install uv"
need claude "Install Claude Code (https://docs.claude.com/en/docs/claude-code), then run: claude auth login"
if claude auth status 2>/dev/null | grep -q '"loggedIn": true'; then echo "claude: logged in"
else echo "claude: NOT logged in. Run 'claude auth login' before any experiment (setup continues)."; fi

say "Harness² (google-research/harness2 @ ${H2_COMMIT:0:7})"
fetch repo https://github.com/google-research/harness2.git "$H2_COMMIT"
[ -x repo/.venv/bin/python ] || uv venv -q --python 3.12 repo/.venv
uv pip install -q --python repo/.venv/bin/python -e repo pytest
mkdir -p tools
echo '{"mcpServers": {}}' > tools/empty_mcp.json   # executors start with no MCP servers

if [ "$WITH_LAB" = 1 ]; then
  say "LAB legal tasks (harveyai/harvey-labs @ ${LAB_COMMIT:0:7})"
  fetch repo/dependencies/harvey-labs https://github.com/harveyai/harvey-labs.git "$LAB_COMMIT"
fi

if [ "$WITH_ADK" = 1 ]; then
  say "Google ADK executor (qwen3:8b via Ollama)"
  need ollama "Install it: brew install ollama"
  [ -x adk-venv/bin/python ] || uv venv -q --python 3.12 adk-venv
  uv pip install -q --python adk-venv/bin/python google-adk==2.12.0 litellm==1.106.0
  if ollama list >/dev/null 2>&1; then
    ollama list | grep -q '^qwen3:8b' || ollama pull qwen3:8b
  else
    echo "Ollama server is not running. Start it (ollama serve) and run: ollama pull qwen3:8b"
  fi
fi

say "Self-checks (no model calls, no cost)"
PY=repo/.venv/bin/python
(cd hpb && ../$PY bench.py)       # every task: about 0 untouched, 1.0 on its reference solution
(cd hpb && ../$PY leakguard.py)   # the answer-leak detector catches known leaks, allows policy constants
(cd hpb && ../$PY adapters.py)    # the adoption-time guard rejects a leaky harness
if [ "$WITH_LAB" = 1 ]; then (cd hpb && ../$PY lab.py selfcheck); fi

say "Ready. Next: docs/GETTING_STARTED.md"
