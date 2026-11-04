# -*- coding: utf-8 -*-
"""Incorporation des polices dans le DOCX (ObfuscatedFont, ECMA-376 §17.8.1)."""
import os
import re
import shutil
import sys
import uuid
import zipfile

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

FONTS = {
    # nom Word : (fichier, style)
    "Glacial Indifference": [
        ("GlacialIndifference-Regular.ttf", "embedRegular"),
        ("GlacialIndifference-Italic.ttf", "embedItalic"),
    ],
    "League Spartan": [
        ("LeagueSpartan-Bold.ttf", "embedBold"),
    ],
    "Distillery Script": [
        ("DistilleryScript-Regular.ttf", "embedRegular"),
    ],
}


def obfuscate(data, key_bytes):
    """XOR des 32 premiers octets avec la clé (ordre inverse, deux fois)."""
    out = bytearray(data)
    for i in range(min(32, len(out))):
        out[i] ^= key_bytes[15 - (i % 16)]
    return bytes(out)


def deobfuscate(data, key_bytes):
    return obfuscate(data, key_bytes)


def embed(docx_in, docx_out):
    zin = zipfile.ZipFile(docx_in)
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()

    rels = items["word/_rels/document.xml.rels"].decode("utf-8")
    font_table = items["word/fontTable.xml"].decode("utf-8")
    settings = items["word/settings.xml"].decode("utf-8")
    types = items["[Content_Types].xml"].decode("utf-8")

    used_ids = set(re.findall(r'Id="rId(\d+)"', rels))
    next_id = max(int(i) for i in used_ids) + 1 if used_ids else 1

    new_rels, n = [], 1
    for family, styles in FONTS.items():
        block = '  <w:font w:name="%s">\n' % family
        for fname, tag in styles:
            path = os.path.join(FONT_DIR, fname)
            if not os.path.exists(path):
                continue
            data = open(path, "rb").read()
            uid = uuid.uuid4()
            key = uid.bytes_le                      # octets de la clé
            blob = obfuscate(data, key)
            part = "word/fonts/font%d.odttf" % n
            items[part] = blob
            rid = "rId%d" % next_id
            next_id += 1
            new_rels.append(
                '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/'
                'officeDocument/2006/relationships/font" Target="fonts/font%d.odttf"/>'
                % (rid, n))
            block += ('    <w:%s r:id="%s" w:fontKey="{%s}" w:subsetted="0"/>\n'
                      % (tag, rid, str(uid).upper()))
            n += 1
        block += "  </w:font>\n"
        font_table = font_table.replace("</w:fonts>", block + "</w:fonts>")

    # relations
    rels = rels.replace("</Relationships>", "".join(new_rels) + "</Relationships>")
    # type de contenu
    if "odttf" not in types:
        types = types.replace(
            "<Types ", "<Types ", 1)
        types = re.sub(r"(<Types[^>]*>)",
                       r'\1<Default Extension="odttf" ContentType="application/'
                       r'vnd.openxmlformats-officedocument.obfuscatedFont"/>',
                       types, count=1)
    # réglages
    if "embedTrueTypeFonts" not in settings:
        ins = '<w:embedTrueTypeFonts/><w:saveSubsetFonts w:val="false"/>'
        # position imposée par le schéma : après zoom/…, avant proofState
        for anchor in ("<w:proofState", "<w:defaultTabStop", "<w:compat"):
            if anchor in settings:
                settings = settings.replace(anchor, ins + anchor, 1)
                break
        else:
            settings = settings.replace("</w:settings>", ins + "</w:settings>")

    items["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    items["word/fontTable.xml"] = font_table.encode("utf-8")
    items["word/settings.xml"] = settings.encode("utf-8")
    items["[Content_Types].xml"] = types.encode("utf-8")

    tmp = docx_out + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in items.items():
            zout.writestr(name, data)
    shutil.move(tmp, docx_out)
    return docx_out


def verify(docx_path):
    """Contrôle : les polices incorporées se déchiffrent bien à l'identique."""
    z = zipfile.ZipFile(docx_path)
    ft = z.read("word/fontTable.xml").decode("utf-8")
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
    ok = []
    for m in re.finditer(r'<w:font w:name="([^"]+)">(.*?)</w:font>', ft, re.S):
        family, body = m.group(1), m.group(2)
        for e in re.finditer(r'<w:(embed\w+) r:id="(rId\d+)" w:fontKey="\{([^}]+)\}"', body):
            tag, rid, key = e.group(1), e.group(2), e.group(3)
            target = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels).group(1)
            blob = z.read("word/" + target)
            raw = deobfuscate(blob, uuid.UUID(key).bytes_le)
            size = 0
            for fname in os.listdir(FONT_DIR):
                ref = open(os.path.join(FONT_DIR, fname), "rb").read()
                if ref == raw:
                    size = len(ref)
            ok.append((family, tag, target, len(blob), "OK" if size else "ÉCHEC"))
    return ok


if __name__ == "__main__":
    embed(sys.argv[1], sys.argv[2])
    for row in verify(sys.argv[2]):
        print("  ", row)
