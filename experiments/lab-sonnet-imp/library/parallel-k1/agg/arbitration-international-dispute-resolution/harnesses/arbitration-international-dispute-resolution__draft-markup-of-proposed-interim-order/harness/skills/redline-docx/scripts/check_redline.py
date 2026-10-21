#!/usr/bin/env python3
"""Check a tracked-changes .docx against the original it was built from.

usage: python3 check_redline.py <original.docx> <redline.docx> [--grep TERM ...] [--accepted out.txt]

Checks (exit 1 on any FAIL): zip + document.xml well-formed; mc:Ignorable prefixes declared;
unique revision ids; REJECT-ALL text == original text (paragraph by paragraph);
at least one w:ins/w:del; prints counts. --grep lists accepted-view paragraphs that still
contain each TERM (e.g. old institution/seat/governing law) so leftovers can be judged.
--accepted writes the accepted-view text (one paragraph per line) for proofreading.
Pure standard library; does not need pandoc or Word.
"""
import re, sys, zipfile
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def views(path):
    z = zipfile.ZipFile(path)
    raw = z.read('word/document.xml').decode('utf-8')
    root = ET.fromstring(raw)
    rej, acc = [], []
    for p in root.iter(W + 'p'):
        ppr = p.find(W + 'pPr')
        mark = ppr.find(W + 'rPr') if ppr is not None else None
        pins = mark is not None and mark.find(W + 'ins') is not None
        pdel = mark is not None and mark.find(W + 'del') is not None
        r_txt, a_txt = [], []

        def walk(el, in_ins, in_del):
            for ch in el:
                if ch.tag == W + 'ins': walk(ch, True, in_del)
                elif ch.tag == W + 'del': walk(ch, in_ins, True)
                elif ch.tag in (W + 'r',): walk(ch, in_ins, in_del)
                elif ch.tag == W + 't':
                    if not in_ins: r_txt.append(ch.text or '')
                    if not in_del: a_txt.append(ch.text or '')
                elif ch.tag == W + 'delText':
                    r_txt.append(ch.text or '')
                else: walk(ch, in_ins, in_del)
        walk(p, False, False)
        if not pins: rej.append(''.join(r_txt))
        if not pdel or ''.join(a_txt): acc.append(''.join(a_txt))
    return raw, root, rej, acc


def main():
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    orig, red = a[0], a[1]
    greps = []; acc_out = None; i = 2
    while i < len(a):
        if a[i] == '--grep':
            i += 1
            while i < len(a) and not a[i].startswith('--'): greps.append(a[i]); i += 1
        elif a[i] == '--accepted': acc_out = a[i + 1]; i += 2
        else: i += 1
    bad = 0
    def fail(msg):
        nonlocal bad; bad += 1; print('FAIL:', msg)
    try:
        raw, root, rej, acc = views(red)
    except Exception as e:
        sys.exit('FAIL: cannot open/parse %s: %s' % (red, e))
    _, _, orig_paras, _ = views(orig)
    m = re.search(r'mc:Ignorable="([^"]*)"', raw)
    if m:
        for pre in m.group(1).split():
            if 'xmlns:%s=' % pre not in raw: fail('mc:Ignorable prefix %s not declared (Word will refuse to open)' % pre)
    ids = re.findall(r'<w:(?:ins|del) w:id="(\d+)"', raw)
    if len(ids) != len(set(ids)): fail('duplicate revision ids')
    n_ins, n_del = raw.count('<w:ins '), raw.count('<w:del ')
    print('revisions: %d insertions, %d deletions' % (n_ins, n_del))
    if n_ins + n_del == 0: fail('no tracked changes present')
    if n_ins + n_del > 4000: fail('implausible revision count -- likely per-character runs; check grouping')
    o = [t for t in orig_paras if t.strip()]; r = [t for t in rej if t.strip()]
    if o != r:
        fail('reject-all text differs from the original')
        for k, (x, y) in enumerate(zip(o, r)):
            if x != y: print('  first difference at para %d:\n   orig: %r\n   rej : %r' % (k, x[:150], y[:150])); break
        if len(o) != len(r): print('  paragraph counts: orig %d, reject-all %d' % (len(o), len(r)))
    else:
        print('OK: reject-all text == original (%d paragraphs)' % len(o))
    for t in greps:
        hits = [x for x in acc if t.lower() in x.lower()]
        print('accepted view contains %r in %d paragraph(s)' % (t, len(hits)))
        for x in hits: print('   -', x[:140])
    if acc_out: open(acc_out, 'w', encoding='utf-8').write('\n'.join(acc) + '\n'); print('accepted view ->', acc_out)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
