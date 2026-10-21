I made four changes. All of them address the one failure in base1, which computed an answer and never wrote the file.

- **Evidence behind all of them:** base1 explored the logs well. It found the cache-warm and traceback look-alike lines and checked the data for consistency. Its last action printed `failed: 19, users: 8, E401 ×7`, then the run ended. `deliverables/base1.md` says "no deliverable produced", and `output/` stayed empty. The ops-e library entry describes the same failure: an ad-hoc parser that only prints, then finishing with nothing written.
- **`scripts/request_failures.py` (new):**
  - It reads the log directory as one stream, including the gzip file.
  - It groups attempts by `req` across files and takes the last attempt by attempt number, checking that against time order.
  - It converts offsets to UTC and applies the half-open window to that last attempt.
  - It counts failed requests, distinct users and the top code over those last attempts only.
  - It prints every failed request, and `--write` emits `{"failed","users","top_code"}`. It exits 1 and writes nothing on a tie or when there are no failures.
  - I ran it on `source/logs` for 2026-10-06 08:00 to 12:00 UTC. It gave 19 failed, 8 users and E401, the same as base1's hand-rolled numbers.
  - One command now both computes and writes, which base1 never did.
- **`scripts/check_output.py` and `hooks.json` (new):** a Stop hook blocks finishing while `output/` is empty or holds an empty or invalid JSON file. It is aimed at the exact failure in base1. I checked that it exits 2 on an empty `output/` and 0 on the file I wrote. I have not seen the hook fire in a real run.
- **`systemprompt.md`:**
  - It points to the script.
  - It records workspace facts that base1 had to discover: req-less INFO lines quote "ERROR code=…", indented traceback lines carry look-alike ERROR text, and the window applies to the last attempt.
  - It says that computing and printing without writing is not finishing.
  - It gives one tie/no-match fallback: re-check the window, then state the tie in the final reply.
  - No skill was added.