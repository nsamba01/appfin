# -*- coding: utf-8 -*-
"""Composition du PDF « OFFRE_TECHNIQUE_VERSION_FINALE.pdf ».

Moteur de mise en page maison : chaque bloc du contenu est converti en éléments
mesurés (lignes), puis placé page par page.  Les mêmes mesures servent à la
génération du DOCX (build_docx.py) afin que les deux livrables soient identiques.
"""
import json
import os
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
from design import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
COVER_DISC = os.path.join(ASSETS, "couverture_disque.png")

CAP_RATIO_LS = 0.72
ASC_LS = 0.8
ASC_BODY = 0.95

TITLE_SIZE = 47.0
TITLE_LEAD = TITLE_SIZE * 1.1


def cap_height(size):
    return size * CAP_RATIO_LS


# ---------------------------------------------------------------------------
# Écriture de texte (toujours via un objet texte : évite toute fuite d'état)
# ---------------------------------------------------------------------------
def T(c, x, y, s, font, size, track=0.0, align="left"):
    to = c.beginText()
    to.setCharSpace(track * size)
    to.setFont(font, size)
    if align == "right":
        x = x - strw(s, font, size, track)
    elif align == "center":
        x = x - strw(s, font, size, track) / 2
    to.setTextOrigin(x, y)
    to.textOut(s)
    c.drawText(to)


# ---------------------------------------------------------------------------
# Découpage en lignes
# ---------------------------------------------------------------------------
def break_lines(text, font, size, width, track=0.0):
    words = text.split(" ")
    space_w = strw(" ", font, size, track)
    lines, cur, cur_w = [], [], 0.0
    for w in words:
        ww = strw(w, font, size, track)
        add = ww if not cur else space_w + ww
        if cur_w + add <= width + 0.05 or not cur:
            cur.append(w)
            cur_w += add
        else:
            lines.append((cur, cur_w, width))
            cur, cur_w = [w], ww
    if cur:
        lines.append((cur, cur_w, width))
    return lines


class Line:
    __slots__ = ("words", "natural", "avail", "font", "size", "track", "x",
                 "bullet", "last", "leading")

    def __init__(self, words, natural, avail, font, size, track, x, bullet,
                 last, leading):
        self.words, self.natural, self.avail = words, natural, avail
        self.font, self.size, self.track = font, size, track
        self.x, self.bullet, self.last, self.leading = x, bullet, last, leading


def measure_paragraph(text, font, size, width, track=0.0, leading=BODY_LEADING,
                      x=0.0, bullet=None):
    raw = break_lines(text, font, size, width, track)
    out = []
    for i, (words, natural, avail) in enumerate(raw):
        out.append(Line(words, natural, avail, font, size, track, x,
                        bullet if i == 0 else None, i == len(raw) - 1, leading))
    return out


def draw_line(c, line, x_origin, y_top, justify=True):
    baseline = PAGE_H - (y_top + ASC_BODY * line.size)
    if line.bullet:
        if line.bullet[0]:
            T(c, x_origin + BULLET_X, baseline - 2.0, line.bullet[0],
              "GlacialIndifference", 15.0)
        if line.bullet[1]:
            T(c, x_origin + BULLET_INDENT - 3.2, baseline, line.bullet[1],
              "GlacialIndifference", line.size, align="right")
    x = x_origin + line.x
    text = " ".join(line.words)
    if justify and not line.last and not line.bullet and len(line.words) > 1:
        gaps = len(line.words) - 1
        extra = line.avail - line.natural
        if 0 <= extra <= 90:
            step = strw(" ", line.font, line.size, line.track) + extra / gaps
            cx = x
            for w in line.words:
                T(c, cx, baseline, w, line.font, line.size, line.track)
                cx += strw(w, line.font, line.size, line.track) + step
            return
    T(c, x, baseline, text, line.font, line.size, line.track)


# ---------------------------------------------------------------------------
# Éléments
# ---------------------------------------------------------------------------
class Element:
    def __init__(self, kind, height, draw, split=None, min_height=None,
                 keep_next=False, data=None, split_fn=None):
        self.kind = kind
        self.height = height
        self.draw = draw
        self.split = split
        self.split_fn = split_fn
        self.min_height = min_height if min_height is not None else height
        self.keep_next = keep_next
        self.data = data or {}


def el_paragraph(lines, space_after=PARA_GAP, justify=True, space_before=0.0):
    leading = lines[0].leading
    h = space_before + len(lines) * leading + space_after

    def draw(c, y_top, n=None):
        for i, ln in enumerate(lines[:n] if n else lines):
            draw_line(c, ln, MARGIN_L, y_top + space_before + i * leading, justify)

    def split(n):
        return el_paragraph(lines[n:], space_after, justify, space_before=0.0)

    min_h = space_before + min(len(lines), 2) * leading + space_after
    return Element("p", h, draw, split=split, min_height=min_h,
                   data={"lines": lines})


def el_badge(text):
    w = strw(text, "LeagueSpartan-Bold", BADGE_SIZE) + 2 * BADGE_PAD
    pad_top = 13.0
    h = pad_top + BADGE_H + 17.0
    base = pad_top + BADGE_H / 2 + BADGE_SIZE * CAP_RATIO_LS / 2

    def draw(c, y_top, n=None):
        y = y_top + pad_top
        c.setFillColorRGB(*BROWN)
        c.rect(MARGIN_L, PAGE_H - y - BADGE_H, w, BADGE_H, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1)
        T(c, MARGIN_L + BADGE_PAD, PAGE_H - (y_top + base), text,
          "LeagueSpartan-Bold", BADGE_SIZE)
        c.setFillColorRGB(*INK)

    return Element("badge", h, draw, keep_next=True, data={"text": text})


def el_sub(text):
    label = text.upper()
    lead = 16.0
    pad_top = 13.0
    h = pad_top + lead + 6.0
    natural = strw(label, "GlacialIndifference", SUB_SIZE, SUB_TRACK)

    def draw(c, y_top, n=None):
        T(c, MARGIN_L, PAGE_H - (y_top + pad_top + ASC_LS * SUB_SIZE), label,
          "GlacialIndifference", SUB_SIZE, SUB_TRACK)

    return Element("sub", h, draw, keep_next=True,
                   data={"text": label, "track": SUB_TRACK, "width": natural})


def el_heading(num, title):
    """Grand titre : numéro Distillery Script 31 pt + titre League Spartan 22 pt."""
    max_w = PAGE_W - MARGIN_R - H1_TITLE_X
    parts = break_lines(title, "LeagueSpartan-Bold", H1_SIZE_TITLE, max_w)
    nlines = len(parts)
    h = 58.0 if nlines == 1 else 84.0

    def draw(c, y_top, n=None):
        c.setFillColorRGB(*INK)
        T(c, H1_NUM_X, PAGE_H - (y_top + 18.1), num, "DistilleryScript", H1_SIZE_NUM)
        y = y_top + 16.9
        for words, nat, avail in parts:
            T(c, H1_TITLE_X, PAGE_H - y, " ".join(words),
              "LeagueSpartan-Bold", H1_SIZE_TITLE)
            y += 25.0

    return Element("h1", h, draw, keep_next=True,
                   data={"num": num, "title": title, "lines": len(parts)})


def el_note(text):
    lead = 13.5
    lines = measure_paragraph(text, "GlacialIndifference-Italic", 10.5, CONTENT_W,
                              leading=lead)
    h = 9.0 + len(lines) * lead + 6.0

    def draw(c, y_top, n=None):
        c.setFillColorRGB(*GREY_TEXT)
        for i, ln in enumerate(lines):
            draw_line(c, ln, MARGIN_L, y_top + 9.0 + i * lead, False)
        c.setFillColorRGB(*INK)

    return Element("note", h, draw)


def el_box(title, items):
    lead = 15.8
    pad = 16.0
    title_lead = 15.0
    item_lines = []
    for it in items:
        ls = measure_paragraph(fr(it), "GlacialIndifference", BODY_SIZE,
                               CONTENT_W - 2 * pad - BULLET_INDENT, leading=lead,
                               x=BULLET_INDENT, bullet=("\u2022", None))
        item_lines.extend(ls)
    inner_h = title_lead + 8.0 + len(item_lines) * lead
    h = inner_h + 2 * pad + 8.0

    def draw(c, y_top, n=None):
        top = y_top + 4.0
        box_h = inner_h + 2 * pad - 6
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1.2)
        c.rect(MARGIN_L, PAGE_H - top - box_h, CONTENT_W, box_h, stroke=1, fill=0)
        y = top + pad - 2
        T(c, MARGIN_L + pad, PAGE_H - (y + ASC_LS * 11), title.upper(),
          "LeagueSpartan-Bold", 11.0, 0.10)
        y += title_lead + 8.0 - 6.0
        for ln in item_lines:
            draw_line(c, ln, MARGIN_L + pad, y, True)
            y += lead

    return Element("box", h, draw, data={"title": title, "items": items})


def el_table_risks(rows_data=None):
    """Tableau des risques ; découpable entre deux lignes avec report d'en-tête."""
    col_w = [148.0, CONTENT_W - 148.0]
    fs, lead, pad = 10.5, 13.4, 6.2
    data_rows = rows_data if rows_data is not None else C.RISKS
    rows = []
    for a, b in data_rows:
        la = break_lines(fr(a), "GlacialIndifference", fs, col_w[0] - 2 * pad)
        lb = break_lines(fr(b), "GlacialIndifference", fs, col_w[1] - 2 * pad)
        rows.append((la, lb))
    head_h = 24.0
    heights = [head_h] + [max(len(a), len(b)) * lead + 2 * pad - 2 for a, b in rows]
    h = sum(heights) + 6

    def draw(c, y_top, n=None):
        y, x = y_top, MARGIN_L
        c.setFillColorRGB(*BROWN)
        c.rect(x, PAGE_H - y - head_h, CONTENT_W, head_h, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1)
        T(c, x + pad, PAGE_H - (y + head_h - 9), "RISQUES",
          "LeagueSpartan-Bold", 10.5)
        T(c, x + col_w[0] + pad, PAGE_H - (y + head_h - 9),
          "MESURES D\u2019ATTÉNUATION", "LeagueSpartan-Bold", 10.5)
        c.setFillColorRGB(*INK)
        y += head_h
        for i, ((la, lb), hh) in enumerate(zip(rows, heights[1:])):
            if i % 2 == 1:
                c.setFillColorRGB(0.973, 0.966, 0.961)
                c.rect(x, PAGE_H - y - hh, CONTENT_W, hh, stroke=0, fill=1)
                c.setFillColorRGB(*INK)
            for lines, cx in ((la, x), (lb, x + col_w[0])):
                ty = y + (hh - len(lines) * lead) / 2 + 2.0
                for ln in lines:
                    T(c, cx + pad, PAGE_H - (ty + lead - 4.0), " ".join(ln[0]),
                      "GlacialIndifference", fs)
                    ty += lead
            y += hh
        c.setStrokeColorRGB(*BROWN)
        c.setLineWidth(0.6)
        yy = y_top
        c.line(x, PAGE_H - yy, x + CONTENT_W, PAGE_H - yy)
        for hh in heights:
            yy += hh
            c.line(x, PAGE_H - yy, x + CONTENT_W, PAGE_H - yy)
        for cx in (x, x + col_w[0], x + CONTENT_W):
            c.line(cx, PAGE_H - y_top, cx, PAGE_H - yy)
        c.setStrokeColorRGB(*INK)

    def split_fn(avail):
        acc = head_h
        k = 0
        for hh in heights[1:]:
            if acc + hh + 6 > avail - 4:
                break
            acc += hh
            k += 1
        if k < 2 or len(rows) - k < 2:
            return None
        return (el_table_risks(data_rows[:k]), el_table_risks(data_rows[k:]))

    return Element("table", h, draw, data={"kind": "risks"}, split_fn=split_fn)


def el_table_gantt():
    phase_w = 132.0
    week_w = (CONTENT_W - phase_w) / 6.0
    head_h, week_h, row_h = 24.0, 22.0, 30.0
    rows = C.GANTT_ROWS
    h = head_h + week_h + len(rows) * row_h + 6

    def draw(c, y_top, n=None):
        x0, y = MARGIN_L, y_top
        c.setFillColorRGB(*BROWN)
        c.rect(x0, PAGE_H - y - head_h, CONTENT_W, head_h, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1)
        T(c, x0 + 9, PAGE_H - (y + head_h - 9), "PHASE", "LeagueSpartan-Bold", 10)
        T(c, x0 + phase_w + (CONTENT_W - phase_w) / 2, PAGE_H - (y + head_h - 9),
          "PÉRIODE", "LeagueSpartan-Bold", 10, align="center")
        y += head_h
        c.setFillColorRGB(*BROWN_LIGHT)
        c.rect(x0, PAGE_H - y - week_h, CONTENT_W, week_h, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1)
        for i, wk in enumerate(C.GANTT_WEEKS):
            T(c, x0 + phase_w + i * week_w + week_w / 2,
              PAGE_H - (y + week_h - 8), wk.upper(), "LeagueSpartan-Bold", 8.2,
              align="center")
        c.setFillColorRGB(*INK)
        y += week_h
        for k, (label, weeks) in enumerate(rows):
            if k % 2 == 1:
                c.setFillColorRGB(0.973, 0.966, 0.961)
                c.rect(x0, PAGE_H - y - row_h, CONTENT_W, row_h, stroke=0, fill=1)
                c.setFillColorRGB(*INK)
            lines = break_lines(fr(label), "GlacialIndifference", 10, phase_w - 18)
            ty = y + (row_h - len(lines) * 13) / 2 + 2.0
            for ln in lines:
                T(c, x0 + 9, PAGE_H - (ty + 10.4), " ".join(ln[0]),
                  "GlacialIndifference", 10)
                ty += 13
            for wk in weeks:
                cx = x0 + phase_w + (wk - 1) * week_w
                c.setFillColorRGB(*BEIGE)
                c.rect(cx, PAGE_H - y - row_h, week_w, row_h, stroke=0, fill=1)
                c.setFillColorRGB(*BROWN)
                T(c, cx + week_w / 2, PAGE_H - (y + row_h / 2 + 3.4), "X",
                  "LeagueSpartan-Bold", 9.5, align="center")
                c.setFillColorRGB(*INK)
            y += row_h
        c.setStrokeColorRGB(*BROWN)
        c.setLineWidth(0.6)
        yy = y_top
        c.line(x0, PAGE_H - yy, x0 + CONTENT_W, PAGE_H - yy)
        for hh in [head_h, week_h] + [row_h] * len(rows):
            yy += hh
            c.line(x0, PAGE_H - yy, x0 + CONTENT_W, PAGE_H - yy)
        for i in range(7):
            xx = x0 + phase_w + i * week_w
            c.line(xx, PAGE_H - y_top, xx, PAGE_H - yy)
        for cx in (x0, x0 + CONTENT_W):
            c.line(cx, PAGE_H - y_top, cx, PAGE_H - yy)
        c.setStrokeColorRGB(*INK)

    return Element("table", h, draw, data={"kind": "gantt"})


def el_spacer(h, keep=False):
    return Element("spacer", h, lambda c, y, n=None: None, keep_next=keep)


# ---------------------------------------------------------------------------
# Séquence d'éléments
# ---------------------------------------------------------------------------
def build_elements():
    els = []
    for i, b in enumerate(C.BODY):
        first = len(els)
        kind = b[0]
        nxt = C.BODY[i + 1][0] if i + 1 < len(C.BODY) else None
        if kind == "h1":
            els.append(el_heading(b[1], b[2]))
        elif kind == "badge":
            els.append(el_badge(b[1]))
        elif kind == "sub":
            els.append(el_sub(b[1]))
        elif kind in ("p", "lead"):
            lines = measure_paragraph(fr(b[1]), "GlacialIndifference", BODY_SIZE,
                                      CONTENT_W)
            el = el_paragraph(lines)
            if nxt in ("table", "box"):
                el.keep_next = True
            els.append(el)
        elif kind in ("ul", "ol"):
            items = b[1]
            all_lines, n = [], len(items)
            starts = []
            for k, it in enumerate(items):
                txt = fr(it).rstrip(" ;.")
                txt += (NBSP + ";" if k < n - 1 else ".") if n > 1 else ""
                if kind == "ul":
                    lines = measure_paragraph(txt, "GlacialIndifference", BODY_SIZE,
                                              CONTENT_W - BULLET_INDENT,
                                              x=BULLET_INDENT,
                                              bullet=("\u2022", None))
                else:
                    lines = measure_paragraph(txt, "GlacialIndifference", BODY_SIZE,
                                              CONTENT_W - BULLET_INDENT,
                                              x=BULLET_INDENT,
                                              bullet=("", f"{k + 1}."))
                for j in range(1, len(lines)):
                    lines[j].bullet = None
                starts.append(len(all_lines))
                all_lines.extend(lines)
                all_lines[-1].last = True
            el = el_paragraph(all_lines, space_after=9.0)
            el.data["item_starts"] = starts
            if nxt in ("table", "box"):
                el.keep_next = True
            els.append(el)
        elif kind == "box":
            els.append(el_spacer(4.0, keep=True))
            els.append(el_box(b[1], b[2]))
            els.append(el_spacer(10.0))
        elif kind == "table":
            els.append(el_spacer(4.0, keep=True))
            els.append(el_table_risks() if b[1] == "risks" else el_table_gantt())
            els.append(el_spacer(14.0))
        elif kind == "note":
            els.append(el_note(fr(b[1])))
        if len(els) > first:
            els[first].data.setdefault("src", i)
    return els


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_decor(c, page_no, with_footer=True):
    c.setFillColorRGB(*BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    if with_footer:
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1.5)
        c.line(0, PAGE_H - 782.6, 204.0, PAGE_H - 782.6)
        c.setFillColorRGB(*INK)
        T(c, 48.6, PAGE_H - 776.4, "Offre technique et méthodologique",
          "GlacialIndifference", FOOTER_SIZE)
        T(c, PAGE_W - MARGIN_R, PAGE_H - 776.4, str(page_no),
          "LeagueSpartan-Bold", 9.5, align="right")


# ---------------------------------------------------------------------------
# Couverture
# ---------------------------------------------------------------------------
def draw_cover(c):
    c.setFillColorRGB(*BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    D = 286.0
    cx = (PAGE_W - D) / 2
    c.drawImage(ImageReader(COVER_DISC), cx, PAGE_H - (42.7 + D), D, D, mask="auto")
    lines = ["OFFRE", "TECHNIQUE ET", "MÉTHODOLOGIQUE"]
    y = 340.0
    c.setFillColorRGB(*INK)
    for t in lines:
        T(c, PAGE_W / 2, PAGE_H - (y + cap_height(TITLE_SIZE) + 1.0), t,
          "LeagueSpartan-Bold", TITLE_SIZE, align="center")
        y += TITLE_LEAD
    y = 516.0
    for ln in break_lines(C.SUBTITLE, "GlacialIndifference", 15.0, CONTENT_W - 20):
        T(c, PAGE_W / 2, PAGE_H - (y + 11.6), " ".join(ln[0]),
          "GlacialIndifference", 15.0, align="center")
        y += 16.6
    T(c, PAGE_W / 2, PAGE_H - (598.0 + 11.6), C.CONSULTANT,
      "GlacialIndifference", 15.0, align="center")
    T(c, 48.1, PAGE_H - (641.0 + 11.0), C.REFERENCE, "GlacialIndifference", 14.0,
      align="left")
    c.setLineWidth(1.5)
    c.setStrokeColorRGB(0, 0, 0)
    c.line(0, PAGE_H - 665.0, 280.5, PAGE_H - 665.0)
    # pastille de date
    tw = strw(C.DATE, "GlacialIndifference", 18)
    pw = tw + 52
    x0 = (PAGE_W - pw) / 2
    y0, y1 = 712.0, 752.0
    c.setLineWidth(1.5)
    c.roundRect(x0, PAGE_H - y1, pw, y1 - y0, 20, stroke=1, fill=0)
    T(c, PAGE_W / 2, PAGE_H - (y0 + 27.5), C.DATE, "GlacialIndifference", 18,
      align="center")


# ---------------------------------------------------------------------------
# Sommaire
# ---------------------------------------------------------------------------
def draw_toc(c, toc_entries, page_no):
    page_decor(c, page_no, with_footer=True)
    c.setFillColorRGB(*INK)
    T(c, 70.3, PAGE_H - (90.8 + 65 * CAP_RATIO_LS + 2), "Sommaire.",
      "LeagueSpartan-Bold", 65)
    T(c, 70.3, PAGE_H - (168.8 + 19.0), C.TOC_SUBTITLE, "DistilleryScript", 22,
      0.036)
    y = 264.2
    pitch = 53.3
    for num, title, target in toc_entries:
        T(c, 133.0, PAGE_H - (y + 20.5), num, "DistilleryScript", 27,
          align="center")
        ty = y + 8.0
        for ln in break_lines(title, "LeagueSpartan-Bold", 20,
                              PAGE_W - MARGIN_R - 174)[:2]:
            T(c, 174, PAGE_H - (ty + 14.4), " ".join(ln[0]), "LeagueSpartan-Bold", 20)
            ty += 21.0
        T(c, PAGE_W - MARGIN_R, PAGE_H - (y + 20.0), str(target),
          "GlacialIndifference", 12, align="right")
        y += pitch


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
def required(els, i):
    """Hauteur nécessaire pour poser els[i] sans orphelin (chaîne keep_next)."""
    h = els[i].height
    j = i
    while els[j].keep_next and j + 1 < len(els):
        j += 1
        nxt = els[j]
        h += (nxt.height if not nxt.split else min(nxt.height, 3 * BODY_LEADING + 20))
        if not nxt.keep_next:
            break
    return h


SPLIT_MARKS = []


def paginate(els):
    SPLIT_MARKS.clear()
    pages, cur = [], {"elements": [], "height": 0.0}
    i = 0
    while i < len(els):
        el = els[i]
        remaining = FRAME_H - cur["height"]
        if required(els, i) <= remaining + 0.01:
            cur["elements"].append(el)
            cur["height"] += el.height
            i += 1
            continue
        if el.split and remaining > el.min_height and not cur["elements"] is None:
            leading = el.data["lines"][0].leading
            space_after = el.height - len(el.data["lines"]) * leading
            n = int((remaining - space_after) // leading)
            n = max(1, min(n, len(el.data["lines"]) - 1))
            if n >= 2:
                marks = el.data.get("item_starts")
                if marks and el.data.get("src") is not None:
                    item = max(i for i, st in enumerate(marks) if st <= n)
                    if marks[item] < n:
                        item += 1
                    if item < len(marks):
                        SPLIT_MARKS.append([el.data["src"], item])
                head = el.data["lines"][:n]
                tail = el.data["lines"][n:]
                cur["elements"].append(el_paragraph(head, space_after))
                cur["height"] += len(head) * leading + space_after
                els[i] = el_paragraph(tail, space_after)
                pages.append(cur)
                cur = {"elements": [], "height": 0.0}
                continue
        if el.split_fn:
            parts = el.split_fn(remaining)
            if parts:
                cur["elements"].append(parts[0])
                cur["height"] += parts[0].height
                els[i] = parts[1]
                pages.append(cur)
                cur = {"elements": [], "height": 0.0}
                continue
        if cur["elements"]:
            pages.append(cur)
            cur = {"elements": [], "height": 0.0}
            continue
        cur["elements"].append(el)
        cur["height"] += el.height
        i += 1
    if cur["elements"]:
        pages.append(cur)
    return pages


def page_starts(pages):
    """Indices des blocs de C.BODY qui commencent une nouvelle page."""
    out = []
    for page in pages:
        for el in page["elements"]:
            src = el.data.get("src")
            if src is not None:
                out.append(src)
                break
    return out


def collect_sections(pages):
    """Numéro de page de chaque grande section (pour le sommaire)."""
    out = {}
    for idx, page in enumerate(pages):
        for el in page["elements"]:
            if el.kind == "h1":
                out[el.data["num"]] = idx + 3
    return out


def compose(path, toc_pages=None):
    els = build_elements()
    titles = [(e.data["num"], e.data["title"]) for e in els if e.kind == "h1"]
    toc_entries = [(num, title, (toc_pages or {}).get(num, "\u2013"))
                   for num, title in titles]
    pages = paginate(els)
    c = canvas.Canvas(path, pagesize=(PAGE_W, PAGE_H),
                      initialFontName="GlacialIndifference", initialFontSize=12)
    c.setTitle("Offre technique et méthodologique — UNICEF Burundi")
    c.setAuthor("Dr Gullit Lufiauluisu, PhD")
    c.setSubject("Appui à la mise en œuvre de la première phase du plan de passage à "
                 "l'échelle de la SNSC 2025-2029 au Burundi")
    c.setKeywords("UNICEF, Burundi, SNSC 2025-2029, offre technique, santé communautaire")
    draw_cover(c)
    c.showPage()
    draw_toc(c, toc_entries, 2)
    c.showPage()
    for idx, page in enumerate(pages):
        page_decor(c, idx + 3, with_footer=True)
        y = BODY_TOP
        for el in page["elements"]:
            el.draw(c, y)
            y += el.height
        c.showPage()
    c.save()
    return len(pages) + 2, collect_sections(pages), pages


def main(out_path):
    total, toc_map, _ = compose(out_path)
    total, toc_map, pages = compose(out_path, toc_pages=toc_map)
    meta = {
        "total_pages": total,
        "toc": {k: v for k, v in toc_map.items()},
        "body_pages": len(pages),
        "page_starts": page_starts(pages),
        "item_breaks": SPLIT_MARKS,
        "page_map": [[el.kind for el in p["elements"]] for p in pages],
    }
    json.dump(meta, open(os.path.join(HERE, "build_meta.json"), "w"),
              indent=2, ensure_ascii=False)
    print("PDF écrit :", out_path, "| pages :", total, "| sommaire :", toc_map)
    return meta


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/offre.pdf")
