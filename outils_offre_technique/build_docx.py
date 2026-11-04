# -*- coding: utf-8 -*-
"""Génération du DOCX « OFFRE_TECHNIQUE_VERSION_MODIFIABLE.docx ».

Le document reprend exactement le même contenu, la même grille (marges, corps,
interlignes) et les mêmes sauts de page que le PDF produit par build_pdf.py.
"""
import copy
import json
import os
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.shared import Pt, Twips, Emu, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
from design import (PAGE_W, PAGE_H, MARGIN_L, MARGIN_R, CONTENT_W, BODY_TOP,
                    BODY_BOTTOM, BG, BROWN, BROWN_LIGHT, BEIGE, INK, GREY_TEXT,
                    BODY_SIZE, BODY_LEADING, H1_SIZE_TITLE, H1_SIZE_NUM,
                    H1_TITLE_X, BADGE_SIZE, BADGE_H, BADGE_PAD, SUB_SIZE,
                    SUB_TRACK, FOOTER_SIZE, NBSP)

HERE = os.path.dirname(os.path.abspath(__file__))
COVER_DISC = os.path.join(HERE, "assets", "couverture_disque.png")

F_POLICE = "Glacial Indifference"
F_SERIF = "Glacial Indifference"          # (pas de serif dans la charte)
F_TITRE = "League Spartan"
F_SCRIPT = "Distillery Script"

PARA_GAP_DOCX = 9.0       # légèrement plus serré que le PDF (10,8) pour absorber
                          # les écarts d'arrondi de Word et éviter tout débordement

# ---------------------------------------------------------------------------
# utilitaires XML (insertion dans l'ordre du schéma OOXML)
# ---------------------------------------------------------------------------
from docx.oxml.ns import qn as _qn

PPR = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
       "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
       "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE",
       "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind",
       "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc", "textDirection",
       "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr",
       "sectPr", "pPrChange"]
RPR = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike",
       "dstrike", "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid",
       "vanish", "webHidden", "color", "spacing", "w", "kern", "position", "sz",
       "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign",
       "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath"]
TBLPR = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
         "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders",
         "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption", "tblDescription"]
TCPR = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd",
        "noWrap", "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark"]
TRPR = ["cnfStyle", "divId", "gridBefore", "gridAfter", "wBefore", "wAfter",
        "cantSplit", "trHeight", "tblHeader", "tblCellSpacing", "jc", "hidden"]
TCB = ["top", "left", "bottom", "right", "insideH", "insideV", "tl2br", "tr2bl"]
TCM = ["top", "left", "bottom", "right"]


def _local(el):
    return el.tag.split("}")[-1]


def put(parent, child, order):
    """Insère (ou remplace) un enfant à sa position dans l'ordre du schéma."""
    tag = _local(child)
    for existing in list(parent):
        if _local(existing) == tag:
            parent.remove(existing)
    if tag in order:
        idx = order.index(tag)
        for existing in parent:
            et = _local(existing)
            if et in order and order.index(et) > idx:
                existing.addprevious(child)
                return child
    parent.append(child)
    return child


DESC = {}          # descente (fraction de la taille) par famille
LEAD = {}          # interligne naturel


def descent(family, size):
    frac = {F_POLICE: 0.271, F_TITRE: 0.35, F_SCRIPT: 0.30}.get(family, 0.271)
    return frac * size


def tw(pt):
    return int(round(pt * 20))


def set_run_font(run, family, size=None, bold=False, color=None, track=None,
                 caps=False):
    run.font.name = family
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        put(rpr, rfonts, RPR)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), family)
    if bold:
        run.font.bold = True
    if color:
        run.font.color.rgb = RGBColor(*[int(round(c * 255)) for c in color])
    if caps:
        run.font.all_caps = True
    if track:
        sp = OxmlElement("w:spacing")
        sp.set(qn("w:val"), str(int(round(track * 20 * (size or 12)))))
        put(rpr, sp, RPR)
    if size:
        run.font.size = Pt(size)


def para_fmt(p, before=0, after=0, line_exact=None, line_rule="exact",
             align=None, left=0, right=0, keep_next=False, keep_together=False,
             widow=True):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.left_indent = Pt(left)
    pf.right_indent = Pt(right)
    if line_exact:
        pPr = p._element.get_or_add_pPr()
        sp = pPr.find(qn("w:spacing"))
        if sp is None:
            sp = put(pPr, OxmlElement("w:spacing"), PPR)
        sp.set(qn("w:line"), str(tw(line_exact)))
        sp.set(qn("w:lineRule"), line_rule)
    if align is not None:
        p.alignment = align
    if keep_next:
        pf.keep_with_next = True
    if keep_together:
        pf.keep_together = True
    pf.widow_control = widow
    return p


def add_tab_stop(p, pos_pt, align=WD_TAB_ALIGNMENT.LEFT):
    pPr = p._element.get_or_add_pPr()
    tabs = pPr.find(qn("w:tabs"))
    if tabs is None:
        tabs = put(pPr, OxmlElement("w:tabs"), PPR)
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "left" if align == WD_TAB_ALIGNMENT.LEFT else "right")
    tab.set(qn("w:pos"), str(tw(pos_pt)))
    tabs.append(tab)


def shade(cell_or_p, hex_color):
    el = cell_or_p._element
    if _local(el) == "tc":
        pr, order = el.get_or_add_tcPr(), TCPR
    else:
        pr, order = el.get_or_add_pPr(), PPR
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hex_color)
    put(pr, sh, order)


def cell_borders(cell, color="5E4032", size=6, edges=("top", "left", "bottom", "right")):
    tcPr = cell._element.get_or_add_tcPr()
    borders = tcPr.find(qn("w:tcBorders"))
    if borders is None:
        borders = put(tcPr, OxmlElement("w:tcBorders"), TCPR)
    for edge in edges:
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(size))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        # ordre imposé dans tcBorders
        idx = TCB.index(edge)
        placed = False
        for existing in borders:
            if TCB.index(_local(existing)) > idx:
                existing.addprevious(e)
                placed = True
                break
        if not placed:
            borders.append(e)


def cell_margins(cell, top=0, bottom=0, left=6.5, right=6.5):
    tcPr = cell._element.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for name, val in (("top", top), ("left", left), ("bottom", bottom),
                      ("right", right)):
        e = OxmlElement(f"w:{name}")
        e.set(qn("w:w"), str(tw(val)))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    put(tcPr, mar, TCPR)


def set_table_width(table, pt):
    """Largeur explicite du tableau (dxa) : indispensable en mise en page fixe."""
    tblPr = table._tbl.tblPr
    w = OxmlElement("w:tblW")
    w.set(qn("w:w"), str(tw(pt)))
    w.set(qn("w:type"), "dxa")
    put(tblPr, w, TBLPR)
    table.autofit = False


def fixed_layout(table):
    tblPr = table._tbl.tblPr
    if tblPr.find(qn("w:tblLayout")) is None:
        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "fixed")
        put(tblPr, layout, TBLPR)


def row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn("w:cantSplit")) is None:
        put(trPr, OxmlElement("w:cantSplit"), TRPR)


def row_height(row, pt, exact=False):
    trPr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), str(tw(pt)))
    h.set(qn("w:hRule"), "exact" if exact else "atLeast")
    put(trPr, h, TRPR)


def keep_row_with_next(row):
    trPr = row._tr.get_or_add_trPr()
    put(trPr, OxmlElement("w:tblHeader"), TRPR)


def add_page_break_before(p):
    p.paragraph_format.page_break_before = True


# ---------------------------------------------------------------------------
# Fond de page (image pleine page derrière le texte) + pied de page
# ---------------------------------------------------------------------------
def build_footer(section):
    """Pied de page : texte + numéro de page, puis filet 0 -> 204 pt."""
    footer = section.footer
    p1 = footer.paragraphs[0]
    p1.text = ""
    para_fmt(p1, before=0, after=0, line_exact=13.0, align=WD_ALIGN_PARAGRAPH.LEFT)
    add_tab_stop(p1, CONTENT_W, WD_TAB_ALIGNMENT.RIGHT)
    r = p1.add_run("Offre technique et méthodologique")
    set_run_font(r, F_POLICE, FOOTER_SIZE)
    r = p1.add_run("\t")
    set_run_font(r, F_TITRE, 9.5, bold=True)
    _page_field(p1)

    p2 = footer.add_paragraph()
    para_fmt(p2, before=0, after=0, line_exact=2,
             left=-(MARGIN_L - 0.0), right=CONTENT_W - 204.0 + (MARGIN_L - 0.0))
    pPr = p2._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    pBdr.append(bottom)
    put(pPr, pBdr, PPR)


def _page_field(p, size="9.5", bold=True, family=None):
    run = p.add_run()
    rpr = OxmlElement("w:rPr")
    rf = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rf.set(qn(attr), family or F_TITRE)
    rpr.append(rf)
    b = OxmlElement("w:b")
    if bold:
        rpr.append(b)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(round(float(size) * 2))))
    rpr.append(sz)
    el = run._element
    el.append(copy.deepcopy(rpr))
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), " PAGE ")
    inner = OxmlElement("w:r")
    inner.append(copy.deepcopy(rpr))
    t = OxmlElement("w:t")
    t.text = "1"
    inner.append(t)
    fld.append(inner)
    el.append(fld)


# ---------------------------------------------------------------------------
# Blocs
# ---------------------------------------------------------------------------
class Writer:
    def __init__(self, doc):
        self.doc = doc
        self.y = 42.0

    def place(self, text, family=F_POLICE, size=BODY_SIZE, baseline=0.0,
              align=WD_ALIGN_PARAGRAPH.LEFT, lead=None, left=0, right=0,
              track=None, caps=False, bold=False, color=INK, lines=1,
              page_break=False):
        """Place un texte à une ligne de base donnée (couverture, sommaire)."""
        lead = lead or round(size * 1.2, 2)
        top = baseline - (lead - descent(family, size))
        p = self.doc.add_paragraph()
        para_fmt(p, before=max(top - self.y, 0), after=0, line_exact=lead,
                 align=align, left=left, right=right,
                 keep_together=True)
        if page_break:
            add_page_break_before(p)
        if text:
            r = p.add_run(text)
            set_run_font(r, family, size, bold, color, track, caps)
        self.y = top + lead * lines
        return p

    def p(self, text="", font=F_POLICE, size=BODY_SIZE, bold=False, color=INK,
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=0, line=BODY_LEADING,
          left=0, right=0, keep_next=False, track=None, caps=False,
          page_break=False):
        p = self.doc.add_paragraph()
        para_fmt(p, before=before, after=after, line_exact=line, align=align,
                 left=left, right=right, keep_next=keep_next)
        if page_break:
            add_page_break_before(p)
        if text:
            r = p.add_run(text)
            set_run_font(r, font, size, bold, color, track, caps)
        return p

    def h1(self, num, title, page_break=False):
        """Grand titre : numéro Distillery 31 pt + titre League Spartan 22 pt."""
        from build_pdf import break_lines
        from design import H1_SIZE_NUM, H1_SIZE_TITLE, H1_TITLE_X, PAGE_W, MARGIN_R
        avail = PAGE_W - MARGIN_R - H1_TITLE_X
        parts = break_lines(title, "LeagueSpartan-Bold", H1_SIZE_TITLE, avail)
        nlines = len(parts)
        line = round(16.9 + max(descent(F_TITRE, H1_SIZE_TITLE),
                                descent(F_SCRIPT, H1_SIZE_NUM)), 2)
        block = 58.0 if nlines == 1 else 84.0
        p = self.doc.add_paragraph()
        para_fmt(p, before=0, after=(block - line) if nlines == 1 else 0.4,
                 line_exact=line, align=WD_ALIGN_PARAGRAPH.LEFT, keep_next=True)
        if page_break:
            add_page_break_before(p)
        add_tab_stop(p, H1_TITLE_X - MARGIN_L)
        r1 = p.add_run(num)
        set_run_font(r1, F_SCRIPT, H1_SIZE_NUM)
        r2 = p.add_run("\t" + " ".join(parts[0][0]))
        set_run_font(r2, F_TITRE, H1_SIZE_TITLE)
        if nlines > 1:
            p2 = self.doc.add_paragraph()
            para_fmt(p2, before=0, after=block - 2 * line - 0.4, line_exact=line,
                     align=WD_ALIGN_PARAGRAPH.LEFT, left=H1_TITLE_X - MARGIN_L,
                     keep_next=True)
            r3 = p2.add_run(" ".join(parts[1][0]))
            set_run_font(r3, F_TITRE, H1_SIZE_TITLE)
            return [p, p2]
        return [p]

    def badge(self, text, page_break=False):
        """Pastille : tableau 1x1 à fond brun, hauteur exacte BADGE_H."""
        from design import strw as _strw
        width = _strw(text, "LeagueSpartan-Bold", BADGE_SIZE) + 2 * BADGE_PAD + 3.0
        self.spacer(13, page_break=page_break)
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.autofit = False
        fixed_layout(tbl)
        tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
        row = tbl.rows[0]
        row_height(row, BADGE_H, exact=True)
        row_cant_split(row)
        cell = row.cells[0]
        cell.width = Pt(width)
        tbl.columns[0].width = Pt(width)
        set_table_width(tbl, width)
        shade(cell, "5E4032")
        cell_margins(cell, top=0, bottom=0, left=BADGE_PAD, right=BADGE_PAD)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        para_fmt(p, before=0, after=0, line_exact=15,
                 align=WD_ALIGN_PARAGRAPH.LEFT)
        r = p.add_run(text)
        set_run_font(r, F_TITRE, BADGE_SIZE, bold=True, color=(1, 1, 1))
        self.spacer(16)
        return tbl

    def sub(self, text, page_break=False):
        p = self.doc.add_paragraph()
        para_fmt(p, before=13, after=6, line_exact=16,
                 align=WD_ALIGN_PARAGRAPH.LEFT, keep_next=True)
        if page_break:
            add_page_break_before(p)
        r = p.add_run(text.upper())
        set_run_font(r, F_POLICE, SUB_SIZE, track=SUB_TRACK)
        return p

    def note(self, text, page_break=False):
        p = self.doc.add_paragraph()
        if page_break:
            add_page_break_before(p)
        para_fmt(p, before=9, after=6, line_exact=13.5,
                 align=WD_ALIGN_PARAGRAPH.LEFT)
        r = p.add_run(text)
        set_run_font(r, F_POLICE, 10.5, color=(0.35, 0.33, 0.32))
        r.font.italic = True
        return p

    def bullets(self, items, numbered=False, page_break=False, break_item=None):
        first = True
        n = len(items)
        for k, it in enumerate(items):
            txt = _fr(it).rstrip(" ;.")
            txt += (NBSP + ";") if k < n - 1 else "."
            p = self.doc.add_paragraph()
            para_fmt(p, before=0, after=(9.0 if k == n - 1 else 0.0),
                     line_exact=BODY_LEADING, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                     left=20.5)
            if (first and page_break) or (break_item == k):
                add_page_break_before(p)
            first = False
            pPr = p._element.get_or_add_pPr()
            ind = pPr.find(qn("w:ind"))
            if ind is None:
                ind = put(pPr, OxmlElement("w:ind"), PPR)
            ind.set(qn("w:hanging"), str(tw(11.8)))
            if numbered:
                r = p.add_run(f"{k + 1}.\t")
                set_run_font(r, F_POLICE, BODY_SIZE)
                add_tab_stop(p, 20.5)
            r = p.add_run("\u2022\t" if not numbered else "")
            if not numbered:
                set_run_font(r, F_POLICE, 15)
                add_tab_stop(p, 20.5)
            r = p.add_run(txt)
            set_run_font(r, F_POLICE, BODY_SIZE)

    def box(self, title, items):
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.autofit = False
        fixed_layout(tbl)
        tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
        cell = tbl.cell(0, 0)
        cell.width = Pt(CONTENT_W)
        tbl.columns[0].width = Pt(CONTENT_W)
        set_table_width(tbl, CONTENT_W)
        for edge in ("top", "left", "bottom", "right"):
            cell_borders(cell, "000000", 9, (edge,))
        cell_margins(cell, top=14, bottom=14, left=16, right=16)
        p0 = cell.paragraphs[0]
        p0.text = ""
        para_fmt(p0, before=0, after=6, line_exact=15, align=WD_ALIGN_PARAGRAPH.LEFT)
        r = p0.add_run(title.upper())
        set_run_font(r, F_TITRE, 11, bold=True, track=0.10)
        for it in items:
            p = cell.add_paragraph()
            para_fmt(p, before=0, after=0, line_exact=15.8,
                     align=WD_ALIGN_PARAGRAPH.JUSTIFY, left=20.5)
            pPr = p._element.get_or_add_pPr()
            ind = OxmlElement("w:ind")
            ind.set(qn("w:left"), str(tw(20.5)))
            ind.set(qn("w:hanging"), str(tw(11.8)))
            put(pPr, ind, PPR)
            add_tab_stop(p, 20.5)
            r = p.add_run("\u2022\t")
            set_run_font(r, F_POLICE, 15)
            r = p.add_run(_fr(it))
            set_run_font(r, F_POLICE, BODY_SIZE)
        # espace après l'encadré
        sp = self.doc.add_paragraph()
        para_fmt(sp, before=0, after=0, line_exact=10)
        return tbl

    def table_risks(self):
        col = [148.0, CONTENT_W - 148.0]
        tbl = self.doc.add_table(rows=1 + len(C.RISKS), cols=2)
        tbl.autofit = False
        fixed_layout(tbl)
        for j, w in enumerate(col):
            tbl.columns[j].width = Pt(w)
        head = tbl.rows[0]
        row_height(head, 24)
        row_cant_split(head)
        keep_row_with_next(head)
        for j, label in enumerate(("RISQUES", "MESURES D\u2019ATTÉNUATION")):
            c = head.cells[j]
            c.width = Pt(col[j])
            shade(c, "5E4032")
            cell_margins(c, top=5, bottom=5, left=6.2, right=6.2)
            p = c.paragraphs[0]
            para_fmt(p, before=0, after=0, line_exact=13, align=WD_ALIGN_PARAGRAPH.LEFT)
            r = p.add_run(label)
            set_run_font(r, F_TITRE, 10.5, bold=True, color=(1, 1, 1))
        for i, (risk, measure) in enumerate(C.RISKS):
            row = tbl.rows[i + 1]
            row_cant_split(row)
            for j, txt in enumerate((risk, measure)):
                c = row.cells[j]
                c.width = Pt(col[j])
                cell_borders(c, "5E4032", 6)
                cell_margins(c, top=5, bottom=5, left=6.2, right=6.2)
                if i % 2 == 1:
                    shade(c, "F8F6F5")
                p = c.paragraphs[0]
                para_fmt(p, before=0, after=0, line_exact=13.4,
                         align=WD_ALIGN_PARAGRAPH.LEFT)
                r = p.add_run(_fr(txt))
                set_run_font(r, F_POLICE, 10.5)
        # filets d'en-tête (le tableau n'a pas de bordure globale)
        for j in range(2):
            cell_borders(tbl.rows[0].cells[j], "5E4032", 6)
        return tbl

    def table_gantt(self):
        phase_w = 132.0
        week_w = (CONTENT_W - phase_w) / 6.0
        tbl = self.doc.add_table(rows=2 + len(C.GANTT_ROWS), cols=7)
        tbl.autofit = False
        fixed_layout(tbl)
        tbl.columns[0].width = Pt(phase_w)
        set_table_width(tbl, CONTENT_W)
        for j in range(1, 7):
            tbl.columns[j].width = Pt(week_w)
        # en-tête
        r0 = tbl.rows[0]
        r1 = tbl.rows[1]
        row_height(r0, 24)
        row_height(r1, 22)
        for rr in (r0, r1):
            row_cant_split(rr)
            keep_row_with_next(rr)
        a = r0.cells[0]
        b = r1.cells[0]
        merged = a.merge(b)
        merged.width = Pt(phase_w)
        shade(merged, "5E4032")
        cell_borders(merged, "5E4032", 6)
        cell_margins(merged, top=5, bottom=5, left=9, right=9)
        p = merged.paragraphs[0]
        para_fmt(p, before=0, after=0, line_exact=14, align=WD_ALIGN_PARAGRAPH.LEFT)
        r = p.add_run("PHASE")
        set_run_font(r, F_TITRE, 10, bold=True, color=(1, 1, 1))
        per = r0.cells[1].merge(r0.cells[6])
        shade(per, "5E4032")
        cell_borders(per, "5E4032", 6)
        cell_margins(per, top=5, bottom=5, left=9, right=9)
        p = per.paragraphs[0]
        para_fmt(p, before=0, after=0, line_exact=14, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run("PÉRIODE")
        set_run_font(r, F_TITRE, 10, bold=True, color=(1, 1, 1))
        for j, wk in enumerate(C.GANTT_WEEKS):
            c = r1.cells[j + 1]
            c.width = Pt(week_w)
            shade(c, "8B6B5A")
            cell_borders(c, "5E4032", 6)
            cell_margins(c, top=4, bottom=4, left=2, right=2)
            p = c.paragraphs[0]
            para_fmt(p, before=0, after=0, line_exact=12.5,
                     align=WD_ALIGN_PARAGRAPH.CENTER)
            r = p.add_run(wk.upper())
            set_run_font(r, F_TITRE, 8.2, bold=True, color=(1, 1, 1))
        # corps
        for i, (label, weeks) in enumerate(C.GANTT_ROWS):
            row = tbl.rows[i + 2]
            row_height(row, 30)
            row_cant_split(row)
            c = row.cells[0]
            c.width = Pt(phase_w)
            cell_borders(c, "5E4032", 6)
            cell_margins(c, top=4, bottom=4, left=9, right=9)
            if i % 2 == 1:
                shade(c, "F8F6F5")
            p = c.paragraphs[0]
            para_fmt(p, before=0, after=0, line_exact=13, align=WD_ALIGN_PARAGRAPH.LEFT)
            r = p.add_run(_fr(label))
            set_run_font(r, F_POLICE, 10)
            for j in range(6):
                cc = row.cells[j + 1]
                cc.width = Pt(week_w)
                cell_borders(cc, "5E4032", 6)
                cell_margins(cc, top=4, bottom=4, left=2, right=2)
                p = cc.paragraphs[0]
                para_fmt(p, before=0, after=0, line_exact=13,
                         align=WD_ALIGN_PARAGRAPH.CENTER)
                if (j + 1) in weeks:
                    shade(cc, "DACEC3")
                    r = p.add_run("X")
                    set_run_font(r, F_TITRE, 9.5, bold=True, color=BROWN)
                else:
                    shade(cc, "FFFFFF")
        return tbl

    def spacer(self, pt, page_break=False):
        p = self.doc.add_paragraph()
        para_fmt(p, before=0, after=0, line_exact=max(pt, 1))
        if page_break:
            add_page_break_before(p)
        return p


def _fr(text):
    from design import fr
    return fr(text)


# ---------------------------------------------------------------------------
# Couverture / sommaire
# ---------------------------------------------------------------------------
def build_cover(w):
    """Couverture : disque ancré + textes placés à la ligne de base."""
    doc = w.doc
    from design import strw
    # disque
    p = doc.add_paragraph()
    para_fmt(p, before=0, after=0, line_exact=1)
    run = p.add_run()
    run.add_picture(COVER_DISC, width=Pt(286), height=Pt(286))
    _float_background(run, x=154.75, y=42.7, w=286, h=286, behind=True)
    w.y = 42.0

    # titre, aligné à droite, lignes 51,7 pt
    for line_txt, base in (("OFFRE", 374.8), ("TECHNIQUE ET", 426.5),
                           ("MÉTHODOLOGIQUE", 478.2)):
        w.place(line_txt, F_TITRE, 47, base, align=WD_ALIGN_PARAGRAPH.RIGHT,
                lead=51.7, bold=True)
    # sous-titre centré, 3 lignes de 16,63 pt
    w.place(C.SUBTITLE, F_POLICE, 15, 527.6, align=WD_ALIGN_PARAGRAPH.CENTER,
            lead=16.63, lines=3)
    w.place(C.CONSULTANT, F_POLICE, 15, 609.6, align=WD_ALIGN_PARAGRAPH.CENTER,
            lead=18.0)
    w.place(C.REFERENCE, F_POLICE, 14, 652.0, align=WD_ALIGN_PARAGRAPH.LEFT,
            lead=16.8, left=-11.4)
    # filet 0 -> 280,5 pt à y = 665
    pl = doc.add_paragraph()
    before = 663.0 - w.y
    para_fmt(pl, before=max(before, 0), after=47.0, line_exact=2,
             left=-MARGIN_L, right=CONTENT_W + MARGIN_L - 280.5)
    pPr = pl._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "0")
    bottom.set(qn("w:color"), "000000")
    pBdr.append(bottom)
    put(pPr, pBdr, PPR)
    w.y = 665.0

    # pastille de date
    pw = strw(C.DATE, "GlacialIndifference", 18) + 52
    tbl = doc.add_table(rows=1, cols=1)
    tbl.autofit = False
    fixed_layout(tbl)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    row = tbl.rows[0]
    row_height(row, 40, exact=True)
    row_cant_split(row)
    cell = row.cells[0]
    cell.width = Pt(pw)
    tbl.columns[0].width = Pt(pw)
    set_table_width(tbl, pw)
    for edge in ("top", "left", "bottom", "right"):
        cell_borders(cell, "000000", 9, (edge,))
    cell_margins(cell, top=0, bottom=0, left=10, right=10)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    pp = cell.paragraphs[0]
    para_fmt(pp, before=0, after=0, line_exact=22, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = pp.add_run(C.DATE)
    set_run_font(r, F_POLICE, 18)


def build_toc(w, toc_pages):
    """Sommaire : titre 65 pt, sous-titre script, puis lignes de 53,3 pt."""
    doc = w.doc
    from build_pdf import break_lines
    w.y = BODY_TOP
    w.place("Sommaire.", F_TITRE, 65, 139.6, align=WD_ALIGN_PARAGRAPH.LEFT,
            lead=78.0, left=10.8, bold=True)
    w.place(C.TOC_SUBTITLE, F_SCRIPT, 22, 187.8, align=WD_ALIGN_PARAGRAPH.LEFT,
            lead=30.0, left=10.8, track=0.036)
    base = 284.7
    titles = [(b[1], b[2]) for b in C.BODY if b[0] == "h1"]
    for k, (num, title) in enumerate(titles):
        target = base + k * 53.3
        parts = break_lines(title, "LeagueSpartan-Bold", 20, 536.0 - 174.0)
        row = doc.add_paragraph()
        lead = 21.0
        before = target - (lead - descent(F_SCRIPT, 27)) - w.y
        para_fmt(row, before=max(before, 0), after=0, line_exact=lead,
                 align=WD_ALIGN_PARAGRAPH.LEFT, keep_together=True,
                 left=174.0 - MARGIN_L)
        _ind = row._element.get_or_add_pPr().find(qn("w:ind"))
        _ind.set(qn("w:hanging"), str(tw(174.0 - MARGIN_L)))
        add_tab_stop(row, 120.5 - MARGIN_L, WD_TAB_ALIGNMENT.LEFT)
        add_tab_stop(row, 174.0 - MARGIN_L, WD_TAB_ALIGNMENT.LEFT)
        add_tab_stop(row, CONTENT_W, WD_TAB_ALIGNMENT.RIGHT)
        r = row.add_run("\t" + num)
        set_run_font(r, F_SCRIPT, 27)
        r = row.add_run("\t")
        set_run_font(r, F_TITRE, 20)
        r = row.add_run(title)
        set_run_font(r, F_TITRE, 20, bold=True)
        r = row.add_run("\t" + str(toc_pages.get(num, "")))
        set_run_font(r, F_POLICE, 12)
        w.y = target - (lead - descent(F_SCRIPT, 27)) + lead * len(parts)


def build_body(w, pages_first_block, item_breaks=None):
    item_breaks = dict(item_breaks or {})
    for i, b in enumerate(C.BODY):
        kind = b[0]
        brk = i in pages_first_block and i != 0
        brk_item = item_breaks.get(i)
        if kind == "h1":
            w.h1(b[1], b[2], page_break=brk)
        elif kind == "badge":
            w.badge(b[1], page_break=brk)
        elif kind == "sub":
            w.sub(b[1], page_break=brk)
        elif kind in ("p", "lead"):
            w.p(_fr(b[1]), page_break=brk, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                after=PARA_GAP_DOCX)
        elif kind == "ul":
            w.bullets(b[1], page_break=brk, break_item=brk_item)
        elif kind == "ol":
            w.bullets(b[1], numbered=True, page_break=brk, break_item=brk_item)
        elif kind == "box":
            w.spacer(4, page_break=brk)
            w.box(b[1], b[2])
        elif kind == "table":
            w.spacer(4, page_break=brk)
            if b[1] == "risks":
                w.table_risks()
            else:
                w.table_gantt()
            w.spacer(14)
        elif kind == "note":
            w.note(_fr(b[1]), page_break=brk)


def main(out_path, toc_pages=None, pages_first_block=None, item_breaks=None):
    doc = Document()
    cp = doc.core_properties
    cp.title = "Offre technique et méthodologique — UNICEF Burundi"
    cp.subject = ("Appui à la mise en œuvre de la première phase du plan de passage "
                  "à l'échelle de la SNSC 2025-2029")
    cp.author = "Dr Gullit Lufiauluisu, PhD"
    cp.category = "Offre technique"
    cp.comments = ("Document reconstruit à partir de l'offre technique ; charte "
                   "graphique du modèle « Rapport de stage ».")
    cp.language = "fr-FR"
    # styles par défaut
    st = doc.styles["Normal"]
    st.font.name = F_POLICE
    st.font.size = Pt(BODY_SIZE)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), F_POLICE)

    sec = doc.sections[0]
    sec.page_width = Twips(11906)
    sec.page_height = Twips(16838)
    sec.left_margin = Pt(MARGIN_L)
    sec.right_margin = Pt(MARGIN_R)
    sec.top_margin = Pt(BODY_TOP)
    sec.bottom_margin = Pt(PAGE_H - BODY_BOTTOM)
    sec.header_distance = Pt(0)
    sec.footer_distance = Pt(PAGE_H - 782.6 - 2)

    # image de fond pleine page dans l'en-tête
    header = sec.header
    hp = header.paragraphs[0]
    hp.text = ""
    para_fmt(hp, before=0, after=0, line_exact=1)
    run = hp.add_run()
    run.add_picture(os.path.join(HERE, "assets", "_fond.png"), width=Emu(1), height=Emu(1))
    _float_background(run)

    build_footer(sec)

    w = Writer(doc)
    build_cover(w)
    doc.add_page_break()
    build_toc(w, toc_pages or {})
    doc.add_page_break()
    first_blocks = set(pages_first_block or ())
    items = {int(k): int(v) for k, v in (item_breaks or {}).items()}
    for src in items:                     # la coupure d'items remplace le saut suivant
        first_blocks.discard(src + 1)
    build_body(w, first_blocks, items)
    doc.save(out_path)
    return out_path


def _float_background(run, x=0, y=0, w=None, h=None, behind=True):
    """Transforme l'image en objet ancré, positionné en absolu sur la page."""
    drawing = run._element.find(qn("w:drawing"))
    inline = drawing.find(qn("wp:inline"))
    cx, cy = inline.find(qn("wp:extent")).get("cx"), inline.find(qn("wp:extent")).get("cy")
    xml = (
        '<wp:anchor %s distT="0" distB="0" distL="0" distR="0" simplePos="0" '
        'relativeHeight="1" behindDoc="1" locked="0" layoutInCell="1" allowOverlap="1">'
        '<wp:simplePos x="0" y="0"/>'
        '<wp:positionH relativeFrom="page"><wp:posOffset>%d</wp:posOffset></wp:positionH>'
        '<wp:positionV relativeFrom="page"><wp:posOffset>%d</wp:posOffset></wp:positionV>'
        '<wp:extent cx="%d" cy="%d"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:wrapNone/>'
        '</wp:anchor>'
    ) % (nsdecls("wp"), int(Pt(x).emu), int(Pt(y).emu),
         int(Pt(w if w else PAGE_W).emu), int(Pt(h if h else PAGE_H).emu))
    from docx.oxml import parse_xml
    anchor = parse_xml(xml)
    # reprendre docPr + graphic de l'inline
    for tag in ("wp:docPr", "a:graphic"):
        el = inline.find(qn(tag))
        if el is not None:
            anchor.append(copy.deepcopy(el))
    # ordre attendu : docPr puis graphic
    drawing.remove(inline)
    drawing.append(anchor)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/offre.docx"
    from design import strw
    main(out)
    print("DOCX écrit :", out)
