# -*- coding: utf-8 -*-
"""Aperçu du DOCX : reconstitue la mise en page Word avec les métriques réelles.

Ce rendu n'est pas Word, mais il applique le même modèle de composition
(interlignes exacts, retraits, tabulations, hauteurs de lignes de tableau,
fond de paragraphe et de cellule, filets) afin de contrôler visuellement le
fichier livré.
"""
import os
import sys

import pymupdf as fitz  # noqa: F401  (vérifie la présence de PyMuPDF)
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design as D
from design import (BG, BROWN, CONTENT_W, FRAME_H, MARGIN_L, PAGE_H, PAGE_W,
                    BODY_TOP, BODY_BOTTOM)

HERE = os.path.dirname(os.path.abspath(__file__))
DESC = {D.F_POLICE if hasattr(D, "F_POLICE") else "GlacialIndifference": 0.271}
DESC = {"Glacial Indifference": 0.271, "League Spartan": 0.35,
        "Distillery Script": 0.30}
PDFNAME = {"Glacial Indifference": "GlacialIndifference",
           "League Spartan": "LeagueSpartan-Bold",
           "Distillery Script": "DistilleryScript"}


def _lines(text, font, size, width, track=0.0):
    words = text.split(" ")
    space = pdfmetrics.stringWidth(" ", font, size) + track * size
    out, cur, cur_w = [], [], 0.0
    for w in words:
        ww = pdfmetrics.stringWidth(w, font, size) + track * size * len(w)
        add = ww if not cur else space + ww
        if cur_w + add <= width + 0.05 or not cur:
            cur.append(w)
            cur_w += add
        else:
            out.append(cur)
            cur = [w]
            cur_w = ww
    if cur:
        out.append(cur)
    return out


def _spacing(p):
    pPr = p._element.find(qn("w:pPr"))
    sp = pPr.find(qn("w:spacing")) if pPr is not None else None
    before = after = 0.0
    line, rule = None, "auto"
    if sp is not None:
        before = int(sp.get(qn("w:before"), 0)) / 20.0
        after = int(sp.get(qn("w:after"), 0)) / 20.0
        ln = sp.get(qn("w:line"))
        rule = sp.get(qn("w:lineRule"), "auto")
        if ln:
            line = int(ln) / 20.0
            if rule == "auto":
                line = line / 12.0 if False else line
    ind = pPr.find(qn("w:ind")) if pPr is not None else None
    left = int(ind.get(qn("w:left"), 0)) / 20.0 if ind is not None else 0.0
    right = int(ind.get(qn("w:right"), 0)) / 20.0 if ind is not None else 0.0
    return before, after, line, rule, left, right


def _tabs(p):
    pPr = p._element.find(qn("w:pPr"))
    out = []
    if pPr is None:
        return out
    tabs = pPr.find(qn("w:tabs"))
    if tabs is None:
        return out
    for t in tabs:
        out.append((int(t.get(qn("w:pos"), 0)) / 20.0, t.get(qn("w:val"))))
    return sorted(out)


def _shd(el):
    pr = el.find(qn("w:pPr")) if el.tag.endswith("}p") else el.find(qn("w:tcPr"))
    if pr is None:
        return None
    sh = pr.find(qn("w:shd"))
    return sh.get(qn("w:fill")) if sh is not None else None


def _cell_shd(tc):
    tcPr = tc.find(qn("w:tcPr"))
    if tcPr is None:
        return None
    sh = tcPr.find(qn("w:shd"))
    return sh.get(qn("w:fill")) if sh is not None else None


def _cell_mar(tc):
    tcPr = tc.find(qn("w:tcPr"))
    out = {"top": 0, "left": 6.5, "bottom": 0, "right": 6.5}
    if tcPr is None:
        return out
    mar = tcPr.find(qn("w:tcMar"))
    if mar is None:
        return out
    for e in mar:
        tag = e.tag.split("}")[-1]
        if tag in out:
            out[tag] = int(e.get(qn("w:w"), "0")) / 20.0
    return out


def _row_h(row):
    trPr = row._tr.find(qn("w:trPr"))
    if trPr is None:
        return None, None
    h = trPr.find(qn("w:trHeight"))
    if h is None:
        return None, None
    return int(h.get(qn("w:val"), 0)) / 20.0, h.get(qn("w:hRule"), "atLeast")


def _runs(p):
    out = []
    for r in p.runs:
        if not r.text:
            continue
        fam = r.font.name or "Glacial Indifference"
        size = r.font.size.pt if r.font.size else D.BODY_SIZE
        bold = bool(r.font.bold)
        color = (0, 0, 0)
        try:
            if r.font.color and r.font.color.rgb:
                c = r.font.color.rgb
                color = (c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
        except Exception:
            pass
        track = 0.0
        rPr = r._element.find(qn("w:rPr"))
        if rPr is not None:
            sp = rPr.find(qn("w:spacing"))
            if sp is not None:
                track = int(sp.get(qn("w:val"), 0)) / 20.0 / size
        out.append((r.text, fam, size, bold, color, track))
    return out


def _font(fam, bold):
    if fam == "League Spartan":
        return "LeagueSpartan-Bold"
    if fam == "Distillery Script":
        return "DistilleryScript"
    return "GlacialIndifference"


def _tokenise(runs):
    toks = []
    for text, fam, size, bold, color, track in runs:
        buf = ""
        for ch in text:
            if ch == "\t" or ch == " ":
                if buf:
                    toks.append(("w", buf, fam, size, color, track))
                    buf = ""
                toks.append(("t" if ch == "\t" else "s", ch, fam, size, color, track))
            elif ch == "\n":
                if buf:
                    toks.append(("w", buf, fam, size, color, track))
                    buf = ""
                toks.append(("b", "", fam, size, color, track))
            else:
                buf += ch
        if buf:
            toks.append(("w", buf, fam, size, color, track))
    return toks


def _kw(tok):
    return pdfmetrics.stringWidth(tok[1], _font(tok[2], False), tok[3]) + tok[5] * tok[3] * len(tok[1])


def _layout(p, width_eff, tabs, hanging=0.0, left=0.0):
    """Rend un paragraphe en lignes positionnées."""
    runs = _runs(p)
    if not runs:
        return [], 0, 0
    toks = _tokenise(runs)
    lines, cur, x = [], [], 0.0
    x = left - hanging
    pending = False
    for idx, tok in enumerate(toks):
        kind = tok[0]
        if kind == "s":
            if cur:
                cur.append((x, " ", tok[2], tok[3], tok[4], tok[5]))
                x += pdfmetrics.stringWidth(" ", _font(tok[2], False), tok[3])
            continue
        if kind == "b":
            lines.append(cur)
            cur, x = [], 0.0
            continue
        if kind == "t":
            stop = None
            for pos, al in tabs:
                if pos > x + 0.01:
                    stop = (pos, al)
                    break
            if stop is None:
                x += 20.0
            elif stop[1] == "right":
                rem = 0.0
                for nxt in toks[idx + 1:]:
                    if nxt[0] == "t":
                        break
                    if nxt[0] == "w":
                        rem += _kw(nxt)
                    elif nxt[0] == "s":
                        rem += pdfmetrics.stringWidth(" ", _font(nxt[2], False), nxt[3])
                x = stop[0] - rem
            else:
                x = stop[0]
            continue
        kw = _kw(tok)
        avail = width_eff + (hanging if not lines else 0.0)
        if x + kw > avail + 0.05 and cur:
            # retour à la ligne (on retire l'espace final)
            while cur and cur[-1][1] == " ":
                cur.pop()
            lines.append(cur)
            cur, x = [], left
        cur.append((x, tok[1], tok[2], tok[3], tok[4], tok[5]))
        x += kw
    if cur:
        lines.append(cur)
    return lines, runs, 0


def draw_paragraph(c, p, x_left, y_top, width, debug=None):
    before, after, line, rule, left, right = _spacing(p)
    runs = _runs(p)
    text = "".join(r[0] for r in runs)
    width_eff = width - left - right
    if not text.strip():
        h = (line or 2) + before + after
        _border(c, p, x_left + left, y_top + before, width_eff, line or 2)
        return h
    size = max(r[2] for r in runs)
    lh = line or size * 1.2
    tabs = _tabs(p)
    hanging = 0.0
    pPr = p._element.find(qn("w:pPr"))
    if pPr is not None:
        _i = pPr.find(qn("w:ind"))
        if _i is not None and _i.get(qn("w:hanging")):
            hanging = int(_i.get(qn("w:hanging"))) / 20.0
    lines, _, _ = _layout(p, width_eff, tabs, hanging, left)
    jc = str(p.alignment or "LEFT")
    for i, ln in enumerate(lines):
        natural = 0.0
        for seg in ln:
            natural = max(natural, seg[0] + pdfmetrics.stringWidth(seg[1], _font(seg[2], False), seg[3]))
        dx = 0.0
        if "CENTER" in jc:
            dx = (width_eff - natural) / 2
        elif "RIGHT" in jc:
            dx = width_eff - natural
        elif "JUSTIFY" in jc and i < len(lines) - 1 and len(ln) > 1:
            dx = 0.0
        base = y_top + before + (i + 1) * lh
        desc_line = max(DESC[seg[2]] * seg[3] for seg in ln)
        for seg in ln:
            if not seg[1].strip():
                continue
            c.setFillColor(Color(*seg[4]))
            c.setFont(_font(seg[2], False), seg[3])
            c.drawString(x_left + dx + seg[0], PAGE_H - (base - desc_line), seg[1])
    _border(c, p, x_left + left, y_top + before, width_eff, len(lines) * lh)
    return before + len(lines) * lh + after


def _border(c, p, x, y_top, width, height):
    pPr = p._element.find(qn("w:pPr"))
    if pPr is None:
        return
    bdr = pPr.find(qn("w:pBdr"))
    if bdr is None:
        return
    for e in bdr:
        edge = e.tag.split("}")[-1]
        sz = int(e.get(qn("w:sz"), 4)) / 8.0
        c.setStrokeColor(Color(0, 0, 0))
        c.setLineWidth(max(sz, 0.5))
        if edge == "bottom":
            c.line(x, PAGE_H - (y_top + height), x + width, PAGE_H - (y_top + height))


def draw_table(c, tbl, x_left, y_top, width, debug=None):
    from docx.table import _Cell
    widths = []
    for col in tbl.columns:
        try:
            widths.append(col.width.pt if col.width else 0)
        except Exception:
            widths.append(0)
    if not any(widths):
        widths = [width / len(tbl.columns)] * len(tbl.columns)
    try:
        from docx.enum.table import WD_TABLE_ALIGNMENT
        if tbl.alignment is not None and "CENTER" in str(tbl.alignment):
            x_left = x_left + (width - sum(widths)) / 2
    except Exception:
        pass
    y = y_top
    for row in tbl.rows:
        exact_h, hrule = _row_h(row)
        tcs = row._tr.findall(qn("w:tc"))
        heights, spans, kinds = [], [], []
        jj = 0
        for tc in tcs:
            tcPr = tc.find(qn("w:tcPr"))
            span, vm = 1, None
            if tcPr is not None:
                g = tcPr.find(qn("w:gridSpan"))
                if g is not None:
                    span = int(g.get(qn("w:val")))
                v = tcPr.find(qn("w:vMerge"))
                if v is not None:
                    vm = v.get(qn("w:val"), "cont")
            cell = _Cell(tc, tbl)
            spans.append(span)
            kinds.append(vm)
            mar = _cell_mar(tc)
            cw_cell = sum(widths[jj:jj + span])
            ch = mar["top"] + mar["bottom"]
            for pp in cell.paragraphs:
                ch += _para_h(pp, cw_cell - mar["left"] - mar["right"])
            heights.append(ch)
            jj += span
        h = max(heights) if heights else 12
        if exact_h and hrule in ("exact", "atLeast"):
            h = exact_h if hrule == "exact" else max(h, exact_h)
        x = x_left
        j = 0
        for k, tc in enumerate(tcs):
            wcell = sum(widths[j:j + spans[k]])
            cell = _Cell(tc, tbl)
            if kinds[k] != "cont":
                fill = _cell_shd(tc)
                if fill:
                    c.setFillColor(HexColor("#" + fill.upper()))
                    c.rect(x, PAGE_H - (y + h), wcell, h, stroke=0, fill=1)
                tcPr = tc.find(qn("w:tcPr"))
                bd = tcPr.find(qn("w:tcBorders")) if tcPr is not None else None
                if bd is not None:
                    c.setStrokeColor(BROWN)
                    c.setLineWidth(0.6)
                    for e in bd:
                        edge = e.tag.split("}")[-1]
                        if edge == "top":
                            c.line(x, PAGE_H - y, x + wcell, PAGE_H - y)
                        elif edge == "bottom":
                            c.line(x, PAGE_H - (y + h), x + wcell, PAGE_H - (y + h))
                        elif edge == "left":
                            c.line(x, PAGE_H - y, x, PAGE_H - (y + h))
                        elif edge == "right":
                            c.line(x + wcell, PAGE_H - y, x + wcell, PAGE_H - (y + h))
                mar = _cell_mar(tc)
                cy = y + mar["top"]
                try:
                    if cell.vertical_alignment is not None and "CENTER" in str(cell.vertical_alignment):
                        content = sum(_para_h(pp, wcell - mar["left"] - mar["right"])
                                      for pp in cell.paragraphs)
                        cy = y + max((h - content) / 2, 0)
                except Exception:
                    pass
                for pp in cell.paragraphs:
                    cy += draw_table_para(c, pp, x + mar["left"], cy,
                                          wcell - mar["left"] - mar["right"])
            x += wcell
            j += spans[k]
        y += h
    return y - y_top


def _para_h(p, width):
    before, after, line, rule, left, right = _spacing(p)
    runs = _runs(p)
    txt = "".join(r[0] for r in runs)
    if not txt.strip():
        return (line or 2) + before + after
    size = max(r[2] for r in runs)
    lh = line or size * 1.2
    lines, _, _ = _layout(p, max(width - left - right, 20), [], 0.0, left)
    return before + len(lines) * lh + after


def draw_table_para(c, p, x, y_top, width):
    before, after, line, rule, left, right = _spacing(p)
    runs = _runs(p)
    txt = "".join(r[0] for r in runs)
    if not txt.strip():
        return (line or 2) + before + after
    size = max(r[2] for r in runs)
    lh = line or size * 1.2
    cw = width - left - right
    lines, _, _ = _layout(p, max(cw, 20), [], 0.0, left)
    jc = str(p.alignment or "LEFT")
    for i, ln in enumerate(lines):
        natural = 0.0
        for seg in ln:
            natural = max(natural, seg[0] + pdfmetrics.stringWidth(seg[1], _font(seg[2], False), seg[3]))
        dx = 0.0
        if "CENTER" in jc:
            dx = (cw - natural) / 2
        elif "RIGHT" in jc:
            dx = cw - natural
        desc_line = max(DESC[seg[2]] * seg[3] for seg in ln)
        for seg in ln:
            if not seg[1].strip():
                continue
            c.setFillColor(Color(*seg[4]))
            c.setFont(_font(seg[2], False), seg[3])
            c.drawString(x + dx + seg[0],
                         PAGE_H - (y_top + before + (i + 1) * lh - desc_line),
                         seg[1])
    return before + len(lines) * lh + after


def render(docx_path, out_pdf):
    doc = Document(docx_path)
    c = canvas.Canvas(out_pdf, pagesize=(PAGE_W, PAGE_H))
    page = 1
    y = BODY_TOP

    def new_page():
        nonlocal page, y
        footer(c, page)
        c.showPage()
        page += 1
        y = BODY_TOP
        c.setFillColor(Color(*BG))
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    c.setFillColor(Color(*BG))
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    body = doc.element.body
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            p = Paragraph(child, doc)
            pPr = child.find(qn("w:pPr"))
            brk = pPr is not None and pPr.find(qn("w:pageBreakBefore")) is not None
            for br in child.iter(qn("w:br")):
                if br.get(qn("w:type")) == "page":
                    brk = True
            if brk and (y > BODY_TOP + 1 or True):
                new_page()
            # image ancrée ?
            for dr in child.iter(qn("w:drawing")):
                anchor = dr.find(qn("wp:anchor"))
                if anchor is not None:
                    ext = anchor.find(qn("wp:extent"))
                    cx = int(ext.get("cx")) / 12700.0
                    cy = int(ext.get("cy")) / 12700.0
                    offH = anchor.find(qn("wp:positionH")).find(qn("wp:posOffset"))
                    offV = anchor.find(qn("wp:positionV")).find(qn("wp:posOffset"))
                    ax = int(offH.text) / 12700.0
                    ay = int(offV.text) / 12700.0
                    blip = dr.find(".//" + qn("a:blip"))
                    rid = blip.get(qn("r:embed")) if blip is not None else None
                    if rid:
                        part = doc.part.related_parts[rid]
                        tmp = "/tmp/_img_%s" % os.path.basename(part.partname)
                        with open(tmp, "wb") as fh:
                            fh.write(part.blob)
                        if cx > 400:      # fond de page
                            c.setFillColor(Color(*BG))
                            c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
                        else:
                            c.drawImage(tmp, ax, PAGE_H - ay - cy, cx, cy,
                                        mask="auto")
            fill = _shd(child)
            if fill:
                before, after, line, rule, left, right = _spacing(p)
                c.setFillColor(HexColor("#" + fill.upper()))
                c.rect(MARGIN_L + left, PAGE_H - (y + before + (line or 0)),
                       CONTENT_W - left - right, (line or 0), stroke=0, fill=1)
            y += draw_paragraph(c, p, MARGIN_L, y, CONTENT_W)
        elif child.tag == qn("w:tbl"):
            t = Table(child, doc)
            y += draw_table(c, t, MARGIN_L, y, CONTENT_W)
    footer(c, page)
    c.showPage()
    c.save()
    return page


def footer(c, page):
    if page == 1:
        return
    c.setFillColor(Color(0, 0, 0))
    c.setFont("GlacialIndifference", 10)
    c.drawString(48.6, PAGE_H - 776.4, "Offre technique et méthodologique")
    c.setFont("LeagueSpartan-Bold", 9.5)
    num = str(page)
    c.drawString(PAGE_W - MARGIN_L - pdfmetrics.stringWidth(num, "LeagueSpartan-Bold", 9.5),
                 PAGE_H - 776.4, num)
    c.setLineWidth(1.5)
    c.line(0, PAGE_H - 782.6, 204, PAGE_H - 782.6)


if __name__ == "__main__":
    n = render(sys.argv[1], sys.argv[2])
    print("aperçu :", sys.argv[2], "pages :", n)
