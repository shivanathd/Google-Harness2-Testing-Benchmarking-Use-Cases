#!/usr/bin/env python3
"""Print the text of a document: python3 scripts/read_doc.py <path>"""
import subprocess, sys
from pathlib import Path
p = Path(sys.argv[1])
if p.suffix.lower() == ".docx":
    r = subprocess.run(["pandoc", str(p), "-t", "markdown", "--wrap=none",
                        "--track-changes=all"], capture_output=True, text=True)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr); sys.exit(r.returncode)
sys.stdout.write(p.read_text(errors="replace"))
