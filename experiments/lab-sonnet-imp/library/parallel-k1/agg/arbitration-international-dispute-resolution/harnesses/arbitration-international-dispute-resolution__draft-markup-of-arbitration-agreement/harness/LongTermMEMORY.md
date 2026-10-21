# Method notes for arbitration-document review and markup tasks

- Establish the baseline (the draft or form under review) and the controlling instructions before reading anything
  else; note any agreement the documents refer to that is not in the data room, and mark its terms unverifiable
  rather than assumed.
- Identify which side we act for and who drafted the form; calibrate every comment to that side.
- If the playbook's priority tiers differ from the client's or partner's stated priorities, reconcile explicitly using
  the source hierarchy. Where the assignment asks for more than one labelling axis (e.g. tiers and per-comment
  labels), keep the axes distinct and apply them consistently in the markup and the memo.
- Dates, names, firm details and section references that differ between documents are reported in the memo, not
  silently corrected.
- Test the playbook's own positions against each other when drafting replacement language (for example, whether
  procedural sub-deadlines in an expedited track fit inside the overall time limit) and flag tensions.
- Tool environment: check what is installed before relying on it (python-docx, LibreOffice and `timeout` may be
  unavailable); prefer pandoc and the provided scripts, and use one bounded fallback rather than repeating a failing
  command.
