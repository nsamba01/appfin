# -*- coding: utf-8 -*-
"""Charte graphique commune (relevée sur le rapport de stage) + outils typographiques.

Toutes les valeurs sont exprimées en points PostScript (1 pt = 1/72 pouce).
Le document de référence est au format A4 (595,5 x 842,25 pt).
"""
import os
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
pdfmetrics.registerFont(TTFont("GlacialIndifference", f"{FONT_DIR}/GlacialIndifference-Regular.ttf"))
pdfmetrics.registerFont(TTFont("GlacialIndifference-Bold", f"{FONT_DIR}/GlacialIndifference-Bold.ttf"))
pdfmetrics.registerFont(TTFont("GlacialIndifference-Italic", f"{FONT_DIR}/GlacialIndifference-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LeagueSpartan-Bold", f"{FONT_DIR}/LeagueSpartan-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DistilleryScript", f"{FONT_DIR}/DistilleryScript-Regular.ttf"))

# ---------------------------------------------------------------- page
PAGE_W, PAGE_H = 595.5, 842.25
MARGIN_L = 59.5
MARGIN_R = 59.5
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R          # 476,5 pt (template : 476,39)
BODY_TOP = 42.0                                   # haut du texte courant (depuis le haut)
BODY_BOTTOM = 752.0                               # limite basse du texte courant
FRAME_H = BODY_BOTTOM - BODY_TOP

# ---------------------------------------------------------------- couleurs
BG = (232 / 255, 232 / 255, 231 / 255)            # #E8E8E7
BROWN = (0.3686, 0.2510, 0.1961)                  # #5E4032 marron-gris des encadrés
BROWN_LIGHT = (0.545, 0.420, 0.353)
BEIGE = (0.855, 0.808, 0.769)                     # cellules marquées du calendrier
INK = (0.0, 0.0, 0.0)
GREY_TEXT = (0.35, 0.33, 0.32)
RULE = (0.0, 0.0, 0.0)

# ---------------------------------------------------------------- typographie
BODY_SIZE = 12.0
BODY_LEADING = 16.63                              # interligne du template (16,63 pt)
PARA_GAP = 10.8
BULLET_GAP = 6.0
BULLET_INDENT = 20.5
BULLET_X = 8.7
H1_SIZE_TITLE = 22.0
H1_SIZE_NUM = 31.0
H1_NUM_X = 59.5
H1_TITLE_X = 111.7
BADGE_SIZE = 12.0
BADGE_H = 29.5
BADGE_PAD = 6.5
SUB_SIZE = 12.0
SUB_TRACK = 0.085        # interlettrage des intertitres (em)
FOOTER_SIZE = 10.0

# ---------------------------------------------------------------- typographie française
NBSP = "\u202f"          # espace fine insécable
APOS = "\u2019"


def fr(text):
    """Typographie française : apostrophes courbes, espaces insécables avant ; : ! ?"""
    t = text.replace("'", APOS)
    t = re.sub(r"\s+([;:!?])", NBSP + r"\1", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def strw(text, font, size, track=0.0):
    """Largeur d'une chaîne, interlettrage optionnel en em."""
    if track:
        return pdfmetrics.stringWidth(text, font, size) + track * size * len(text)
    return pdfmetrics.stringWidth(text, font, size)


def ascent_offset(font, size):
    """Distance entre le haut de la ligne et la ligne de base."""
    face = pdfmetrics.getFont(font).face
    asc = getattr(face, "ascent", 0.8)
    desc = abs(getattr(face, "descent", 0.2))
    return size * asc / (asc + desc)


def text_tracked(c, x, y, text, font, size, track=0.0, align="left"):
    """Écrit une chaîne avec interlettrage via un objet texte."""
    to = c.beginText()
    if track:
        to.setCharSpace(track * size)
    to.setFont(font, size)
    if align == "right":
        to.setTextOrigin(x - strw(text, font, size, track), y)
    elif align == "center":
        to.setTextOrigin(x - strw(text, font, size, track) / 2, y)
    else:
        to.setTextOrigin(x, y)
    to.textOut(text)
    c.drawText(to)
