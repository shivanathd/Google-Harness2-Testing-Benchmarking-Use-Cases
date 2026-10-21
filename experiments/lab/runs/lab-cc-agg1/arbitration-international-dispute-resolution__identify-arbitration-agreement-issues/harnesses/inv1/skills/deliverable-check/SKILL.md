---
name: deliverable-check
description: Reopen and check each finished deliverable file (.docx, .xlsx, .pptx) before the final message. Covers exact filenames, a full readback, counts and cross-references, and making the final message match the saved file.
---

# Deliverable check

A successful write or build does not show that a deliverable is usable. Run every step below on each file in `output/` before you write the final message.

1. **Names.** Run `ls -la output/`. Every filename the assignment names must be there, with that exact spelling, and non-empty. Drafts and build sources stay outside `output/`.

2. **Full readback.** Convert each file with `python3 scripts/read_doc.py output/<name>.docx > /tmp/check_<name>.txt`, then read the whole text, in parts if it is long. A head and a tail are not enough. Confirm:
   - the title and every section the assignment asks for are present, in the requested order;
   - every table has its header row and all of its rows, and the text does not stop partway through a table;
   - the last section is complete.
   Anything the text readback cannot show (column widths, fonts, page layout) goes into the final message as not checked.

3. **Counts.** Every total the file states (for example "N issues" or "4 Critical") must equal the count of the matching rows or items in the file itself. Count from the readback text, not from memory. For ID-keyed tables, for example:
   `grep -oE '^ *[A-Za-z]+-[0-9]+' /tmp/check_<name>.txt | sed 's/-.*//; s/ //g' | sort | uniq -c`
   If a total and the count disagree, correct the file, then repeat step 2 for that file.

4. **Cross-references.** For each section, clause, or exhibit number cited in the bottom line or the summary table, extract the source the same way (`read_doc.py` into `/tmp`) and confirm the number exists and says what the file says it says. Correct the file where it does not. Record any cite you could not confirm as an open item.

5. **Final message.** Take every count, date, and amount in the final message from steps 2 to 4, not from your working notes. Say which checks you ran and which you did not.
