Checks to re-derive on every small-repo fix (procedure, not facts about any one repo):
- Trace the entry point's order of operations (load, dispatch, mutate, save, print). Put validation before the first mutation or save, and return the error status there, so a rejected command leaves files unchanged.
- For each numeric rule in the issue, decide the boundary explicitly: is exactly zero or exact equality valid, and is a comparison strict or inclusive? Test the value on each side of the boundary.
- When the issue changes ordering or filtering of one mode, confirm the other modes keep their old order and output format.
