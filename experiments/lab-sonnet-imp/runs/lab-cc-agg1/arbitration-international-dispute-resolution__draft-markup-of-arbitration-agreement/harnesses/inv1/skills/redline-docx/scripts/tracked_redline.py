#!/usr/bin/env python3
"""Apply paragraph edits to a .docx as real Word tracked changes (w:ins / w:del).

usage: python3 tracked_redline.py <original.docx> <spec.json> <output.docx>

spec.json:
{
  "author": "Firm LLP",                      # optional
  "date": "2025-01-11T09:00:00Z",            # optional
  "banner": "text for a tracked italic note inserted before the first paragraph",  # optional
  "edits":   [{"match": "Section 3.1", "new": "full replacement paragraph text",
               "note": "[NOTE -- comment text]"}],     # note optional: tracked italic paragraph after
  "inserts": [{"after": "Section 5.3", "text": "**Section 5.4 -- Title.** body", "note": "..."}],
  "deletes": [{"match": "Section 6.1", "note": "..."}],   # whole paragraph struck
  "notes":   [{"after": "Section 3.2", "note": "[NOTE -- no change]"}]  # comment only
}
- "match"/"after" = unique start of the paragraph's text (leading text, case-sensitive),
  or "#N" for the Nth paragraph (0-based, as listed by --list).
- "new"/"text" use **bold** markers for inserted bold; unchanged text keeps its original
  formatting. Diff is word-level, so keep unchanged wording identical to the original.
- Inserts/notes after the same anchor keep spec order. Fails loudly on a missing or
  ambiguous match (lists candidates) -- nothing is written in that case.
Operates on the document.xml string, so namespaces/headers/footers are untouched.
Also: --list prints "index<TAB>text-start" for every paragraph.
"""
import difflib, json, re, sys, zipfile
from xml.sax.saxutils import escape, unescape

P_RE = re.compile(r'<w:p(?: [^>]*)?>.*?</w:p>', re.S)
R_RE = re.compile(r'<w:r(?: [^>]*)?>(.*?)</w:r>', re.S)
T_RE = re.compile(r'<w:t(?: [^>]*)?>(.*?)</w:t>', re.S)


def para_info(px):
    ppr = re.search(r'<w:pPr>.*?</w:pPr>', px, re.S)
    ppr = ppr.group(0) if ppr else ''
    chars = []  # (char, rpr_xml)
    for rm in R_RE.finditer(px):
        body = rm.group(1)
        rpr = re.search(r'<w:rPr>.*?</w:rPr>', body, re.S)
        rpr = rpr.group(0) if rpr else ''
        for tm in T_RE.finditer(body):
            for c in unescape(tm.group(1)):
                chars.append((c, rpr))
    return ppr, chars


def is_bold(rpr): return '<w:b/>' in rpr or '<w:b ' in rpr


def strip_fmt(rpr, bold=False, italic=False, color=None):
    rpr = re.sub(r'<w:(b|i|u|color)(?: [^>]*)?/>', '', rpr)
    add = ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '')
    if color: add += '<w:color w:val="%s"/>' % color
    if not rpr: return '<w:rPr>%s</w:rPr>' % add if add else ''
    return rpr.replace('</w:rPr>', add + '</w:rPr>')


class Ctx:
    def __init__(self, author, date):
        self.author, self.date, self.n = escape(author), date, 1000

    def attrs(self):
        self.n += 1
        return 'w:id="%d" w:author="%s" w:date="%s"' % (self.n, self.author, self.date)


def run(rpr, text, deleted=False):
    tag = 'w:delText' if deleted else 'w:t'
    return '<w:r>%s<%s xml:space="preserve">%s</%s></w:r>' % (rpr, tag, escape(text), tag)


def parse_markup(s):
    out, bold = [], False
    for part in re.split(r'(\*\*)', s):
        if part == '**': bold = not bold
        else: out.extend((c, bold) for c in part)
    return out


def group(items, key):
    segs = []
    for it in items:
        k = key(it)
        if segs and segs[-1][0] == k: segs[-1][1].append(it)
        else: segs.append((k, [it]))
    return segs


def tokens(chars_text):
    return re.findall(r'\s+|\w+|[^\w\s]', chars_text)


def edit_paragraph(px, new_markup, ctx):
    ppr, ochars = para_info(px)
    new = parse_markup(new_markup)
    otext, ntext = ''.join(c for c, _ in ochars), ''.join(c for c, _ in new)
    ot, nt = tokens(otext), tokens(ntext)
    base = next((r for c, r in ochars if not is_bold(r)), ochars[0][1] if ochars else '')
    base = strip_fmt(base)
    out, oi, ni = [], 0, 0
    sm = difflib.SequenceMatcher(None, ot, nt, autojunk=False)

    def emit_orig(a, b, deleted):
        for rpr, grp in group(ochars[a:b], lambda x: x[1]):
            txt = ''.join(c for c, _ in grp)
            out.append('<w:del %s>%s</w:del>' % (ctx.attrs(), run(rpr, txt, True)) if deleted else run(rpr, txt))

    def emit_new(a, b):
        for bold, grp in group(new[a:b], lambda x: x[1]):
            txt = ''.join(c for c, _ in grp)
            rpr = strip_fmt(base, bold=bold)
            out.append('<w:ins %s>%s</w:ins>' % (ctx.attrs(), run(rpr, txt)))

    opos = [0]; [opos.append(opos[-1] + len(t)) for t in ot]
    npos = [0]; [npos.append(npos[-1] + len(t)) for t in nt]
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': emit_orig(opos[i1], opos[i2], False)
        else:
            if i2 > i1: emit_orig(opos[i1], opos[i2], True)
            if j2 > j1: emit_new(npos[j1], npos[j2])
    return '<w:p>%s%s</w:p>' % (ppr, ''.join(out))


def ins_paragraph(ref_ppr, markup, ctx, base_rpr, italic=False, color=None):
    mark = '<w:rPr><w:ins %s/></w:rPr>' % ctx.attrs()
    ppr = ref_ppr.replace('</w:pPr>', mark + '</w:pPr>') if ref_ppr else '<w:pPr>%s</w:pPr>' % mark
    ppr = re.sub(r'<w:keepNext/>', '', ppr)
    runs = []
    for bold, grp in group(parse_markup(markup), lambda x: x[1]):
        rpr = strip_fmt(base_rpr, bold=bold, italic=italic, color=color)
        runs.append('<w:ins %s>%s</w:ins>' % (ctx.attrs(), run(rpr, ''.join(c for c, _ in grp))))
    return '<w:p>%s%s</w:p>' % (ppr, ''.join(runs))


def delete_paragraph(px, ctx):
    ppr, ochars = para_info(px)
    mark = '<w:rPr><w:del %s/></w:rPr>' % ctx.attrs()
    ppr = ppr.replace('</w:pPr>', mark + '</w:pPr>') if ppr else '<w:pPr>%s</w:pPr>' % mark
    runs = ['<w:del %s>%s</w:del>' % (ctx.attrs(), run(r, ''.join(c for c, _ in g), True))
            for r, g in group(ochars, lambda x: x[1])]
    return '<w:p>%s%s</w:p>' % (ppr, ''.join(runs))


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '--list':
        x = zipfile.ZipFile(args[1]).read('word/document.xml').decode('utf-8')
        for i, m in enumerate(P_RE.finditer(x)):
            t = ''.join(c for c, _ in para_info(m.group(0))[1])
            print('%d\t%s' % (i, t[:100]))
        return
    if len(args) != 3: sys.exit(__doc__)
    src, specf, dst = args
    spec = json.load(open(specf, encoding='utf-8'))
    zin = zipfile.ZipFile(src)
    xml = zin.read('word/document.xml').decode('utf-8')
    ctx = Ctx(spec.get('author', 'Reviewer'), spec.get('date', '2025-01-01T00:00:00Z'))
    paras = [m.group(0) for m in P_RE.finditer(xml)]
    texts = [''.join(c for c, _ in para_info(p)[1]) for p in paras]

    def find(key):
        if key.startswith('#'): return int(key[1:])
        hits = [i for i, t in enumerate(texts) if t.startswith(key)]
        if len(hits) != 1:
            sys.exit('match %r hit %d paragraphs: %s' % (key, len(hits), [(i, texts[i][:60]) for i in hits]))
        return hits[0]

    NOTE_COLOR = spec.get('note_color', '1F4E79')
    after = {}  # idx -> [new paragraph xml]
    repl = {}   # idx -> replacement xml
    def base_of(i):
        ch = para_info(paras[i])[1]
        return next((r for c, r in ch if not is_bold(r)), ch[0][1] if ch else '')
    def add_note(i, note):
        if note: after.setdefault(i, []).append(ins_paragraph(para_info(paras[i])[0], note, ctx, base_of(i), True, NOTE_COLOR))
    for e in spec.get('edits', []):
        i = find(e['match'])
        if '<w:br' in paras[i]: sys.exit('paragraph %d contains a break; edit it by inserts/deletes instead' % i)
        repl[i] = edit_paragraph(paras[i], e['new'], ctx); add_note(i, e.get('note'))
    for d in spec.get('deletes', []):
        i = find(d['match']); repl[i] = delete_paragraph(paras[i], ctx); add_note(i, d.get('note'))
    for n in spec.get('inserts', []):
        i = find(n['after'])
        after.setdefault(i, []).append(ins_paragraph(para_info(paras[i])[0], n['text'], ctx, base_of(i)))
        add_note(i, n.get('note'))
    for n in spec.get('notes', []):
        add_note(find(n['after']), n['note'])

    out, pos = [], 0
    for i, m in enumerate(P_RE.finditer(xml)):
        out.append(xml[pos:m.start()])
        if i == 0 and spec.get('banner'):
            out.append(ins_paragraph(para_info(paras[0])[0], spec['banner'], ctx, base_of(0), True, NOTE_COLOR))
        out.append(repl.get(i, paras[i])); out.extend(after.get(i, []))
        pos = m.end()
    out.append(xml[pos:])
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == 'word/document.xml': data = ''.join(out).encode('utf-8')
            zout.writestr(it, data)
    print('wrote %s: %d edits, %d deletes, %d inserts, %d notes, %d revision marks' % (
        dst, len(spec.get('edits', [])), len(spec.get('deletes', [])), len(spec.get('inserts', [])),
        sum(len(v) for v in after.values()), ctx.n - 1000))


if __name__ == '__main__':
    main()
