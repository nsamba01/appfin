# -*- coding: utf-8 -*-
"""Contrôle qualité : cohérence PDF / DOCX, intégrité du contenu, pagination."""
import json
import os
import re
import sys
import zipfile

import pymupdf as fitz
from docx import Document
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
from design import (CONTENT_W, FRAME_H, BODY_LEADING, MARGIN_L, MARGIN_R, PAGE_W,
                    strw, BODY_TOP, BODY_BOTTOM)


def norm(t):
    t = t.replace("\u00a0", " ").replace("\u202f", " ").replace("\u2019", "'")
    t = t.replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", t).strip().lower()


# ---------------------------------------------------------------------------
def docx_blocks(path):
    """Liste des paragraphes du DOCX dans l'ordre, avec leur mise en forme."""
    doc = Document(path)
    out = []
    body = doc.element.body
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            out.append(("p", Paragraph(child, doc)))
        elif child.tag == qn("w:tbl"):
            out.append(("t", Table(child, doc)))
    return out


def para_info(p):
    pPr = p._element.find(qn("w:pPr"))
    spacing = pPr.find(qn("w:spacing")) if pPr is not None else None
    before = after = line = None
    rule = "auto"
    if spacing is not None:
        before = int(spacing.get(qn("w:before"), 0)) / 20
        after = int(spacing.get(qn("w:after"), 0)) / 20
        line = spacing.get(qn("w:line"))
        line = int(line) / 20 if line else None
        rule = spacing.get(qn("w:lineRule"), "auto")
    ind = pPr.find(qn("w:ind")) if pPr is not None else None
    left = int(ind.get(qn("w:left"), 0)) / 20 if ind is not None else 0
    right = int(ind.get(qn("w:right"), 0)) / 20 if ind is not None else 0
    brk = pPr is not None and pPr.find(qn("w:pageBreakBefore")) is not None
    for br in p._element.iter(qn("w:br")):
        if br.get(qn("w:type")) == "page":
            brk = True
    for br in p._element.iter(qn("w:lastRenderedPageBreak")):
        brk = brk
    sizes, fonts, text = [], [], []
    for r in p.runs:
        t = r.text
        if t:
            text.append(t)
            if r.font.size:
                sizes.append(r.font.size.pt)
            fonts.append(r.font.name)
    return {"before": before or 0, "after": after or 0, "line": line, "rule": rule,
            "left": left, "right": right, "break": brk,
            "size": max(sizes) if sizes else 12, "font": fonts[0] if fonts else None,
            "text": "".join(text)}


def simulate_docx(path, verbose=False):
    """Reconstitue la pagination Word à partir des métriques des polices."""
    pages, cur = [], 0.0
    for kind, obj in docx_blocks(path):
        if kind == "t":
            h = 0.0
            for row in obj.rows:
                hh = 0.0
                for cell in row.cells:
                    ch = 0.0
                    for p in cell.paragraphs:
                        info = para_info(p)
                        w = CONTENT_W / max(1, len(row.cells)) - 20
                        lines = max(1, len(_wrap(info["text"], info["size"], w)))
                        ch += lines * (info["line"] or info["size"] * 1.2)
                    hh = max(hh, ch + 10)
                h += hh
            pages.append(cur)
            cur = h
            continue
        info = para_info(obj)
        if info["break"]:
            pages.append(cur)
            cur = 0.0
        if not info["text"].strip():
            cur += (info["line"] or 2) + info["before"] + info["after"]
            continue
        w = CONTENT_W - info["left"] - info["right"]
        nlines = len(_wrap(info["text"], info["size"], max(w, 50)))
        lh = info["line"] or info["size"] * 1.2
        cur += info["before"] + nlines * lh + info["after"]
    pages.append(cur)
    return pages


def _wrap(text, size, width):
    """Découpage approximatif aux métriques Glacial Indifference."""
    words = text.split(" ")
    lines, cur = [], 0.0
    for w in words:
        ww = strw(w, "GlacialIndifference", size)
        add = ww if cur == 0 else strw(" ", "GlacialIndifference", size) + ww
        if cur + add <= width or cur == 0:
            cur += add
        else:
            lines.append(cur)
            cur = ww
    lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
def check_pdf(path):
    """Contrôle de cadre : rien hors marges dans le corps, rien sous le pied."""
    doc = fitz.open(path)
    issues = []
    fonts = set()
    for i, page in enumerate(doc):
        for f in page.get_fonts(full=True):
            fonts.add((f[3], f[1]))
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if not s["text"].strip():
                        continue
                    x0, y0, x1, y1 = s["bbox"]
                    if y1 > 760:            # pied de page : hors contrôle de marge
                        continue
                    tol_l = 12 if i == 0 else 3   # couverture : texte en saillie assumé
                    tol_r = 6                     # badge long du livrable 1
                    if x0 < MARGIN_L - tol_l or x1 > PAGE_W - MARGIN_R + tol_r:
                        issues.append(f"p{i + 1} hors marges: {s['text'][:40]!r} "
                                      f"x0={x0:.1f} x1={x1:.1f}")
    return doc.page_count, sorted(fonts), issues


def docx_pages(docx_path):
    """Pagination du DOCX : rendu par docx_preview avec les métriques réelles."""
    import tempfile
    import docx_preview
    tmp = os.path.join(tempfile.gettempdir(), "_qa_docx_preview.pdf")
    n = docx_preview.render(docx_path, tmp)
    d = fitz.open(tmp)
    out = []
    for p in d:
        ys = []
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                if "".join(s["text"] for s in l["spans"]).strip() and l["bbox"][3] < 760:
                    ys.append(l["bbox"][3])
        out.append(round(max(ys), 1) if ys else 0.0)
    d.close()
    return n, out


def pdf_text(path):
    doc = fitz.open(path)
    txt = []
    for p in doc:
        txt.append(p.get_text("text"))
    return "\n".join(txt)


def main(pdf_path, docx_path):
    print("=" * 78)
    print("CONTRÔLE QUALITÉ —", os.path.basename(pdf_path), "/", os.path.basename(docx_path))
    print("=" * 78)

    npages, fonts, issues = check_pdf(pdf_path)
    print(f"\n[PDF] {npages} pages")
    print("[PDF] polices incorporées :")
    for name, ext in fonts:
        print(f"        - {name}  ({ext})")
    print(f"[PDF] débordements détectés : {len(issues)}")
    for i in issues[:12]:
        print("        !", i)

    # --- intégrité du contenu source
    ptxt = norm(pdf_text(pdf_path))
    d = Document(docx_path)
    dtxt = norm("\n".join(p.text for p in d.paragraphs) + "\n" +
                "\n".join(c.text for t in d.tables for r in t.rows for c in r.cells))
    manquants = []
    for kind, *rest in C.BODY:
        if kind in ("p", "lead"):
            frag = norm(rest[0])[:90]
        elif kind in ("h1",):
            frag = norm(rest[1])
        elif kind == "badge":
            frag = norm(rest[0])
        elif kind == "sub":
            frag = norm(rest[0])
        elif kind in ("ul", "ol"):
            frag = norm(rest[0][0])[:60]
        elif kind == "box":
            frag = norm(rest[0])
        else:
            continue
        if frag and frag not in ptxt:
            manquants.append(("PDF", frag[:70]))
        if frag and frag not in dtxt:
            manquants.append(("DOCX", frag[:70]))
    # notes et tableaux
    for row in C.RISKS:
        for cell in row:
            if norm(cell)[:60] not in ptxt:
                manquants.append(("PDF", norm(cell)[:60]))
            if norm(cell)[:60] not in dtxt:
                manquants.append(("DOCX", norm(cell)[:60]))
    for label, weeks in C.GANTT_ROWS:
        if norm(label) not in ptxt:
            manquants.append(("PDF", norm(label)))
        if norm(label) not in dtxt:
            manquants.append(("DOCX", norm(label)))

    print(f"\n[CONTENU] blocs vérifiés : {len(C.BODY)} — manquants : {len(manquants)}")
    for m in manquants[:15]:
        print("        !", m)

    # --- pagination du DOCX (rendu avec les métriques des polices)
    ndocx, pages = docx_pages(docx_path)
    print(f"\n[DOCX] pagination : {ndocx} pages (PDF : {npages})")
    over = [(i + 1, h) for i, h in enumerate(pages) if h > BODY_BOTTOM]
    print(f"[DOCX] pages dépassant la zone de texte : {len(over)}")
    for i, h in over[:10]:
        print(f"        ! page {i} : bas du texte à {h:.0f} pt (limite {BODY_BOTTOM})")
    print("[DOCX] bas du texte par page (pt) :", ", ".join(f"{h:.0f}" for h in pages))

    # --- respect de la charte typographique
    print("\n[CHARTE] tailles utilisées dans le DOCX :")
    sizes = {}
    for p in d.paragraphs:
        for r in p.runs:
            if r.font.size:
                sizes[round(r.font.size.pt, 1)] = sizes.get(round(r.font.size.pt, 1), 0) + 1
    print("        ", dict(sorted(sizes.items())))
    fam = {}
    for p in d.paragraphs:
        for r in p.runs:
            if r.font.name:
                fam[r.font.name] = fam.get(r.font.name, 0) + 1
    print("[CHARTE] polices du DOCX :", fam)
    return manquants, issues, over


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
