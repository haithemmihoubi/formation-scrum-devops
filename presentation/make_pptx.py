#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère un fichier PowerPoint (.pptx) éditable SANS dépendance externe
(uniquement la bibliothèque standard). Un .pptx est un ZIP de fichiers OOXML.

Charte Solid Wall : bleu #0B3D62, jaune #F5B301.
Slides 16:9 (13.333 x 7.5 pouces).

Le contenu des slides est dans slides_content.py.
"""
import os
import struct
import zipfile
from xml.sax.saxutils import escape

from slides_content import TITLE, SUBTITLE, AUTHOR, SLIDES
from chapter7_scrum import CH7_SLIDES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "Formation-Agile-DevOps-Securite.pptx")
IMGDIR = os.path.join(HERE, "img")

# Dimensions 16:9 en EMU (1 pouce = 914400 EMU)
EMU_W = 12192000
EMU_H = 6858000

BLUE = "0B3D62"
YELLOW = "F5B301"
DARKBLUE2 = "14507A"
GREY = "5B6770"
WHITE = "FFFFFF"


# ----------------------------------------------------------------------------
# Parties statiques du paquet OOXML
# ----------------------------------------------------------------------------

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>
<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
{slide_overrides}
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

RELS_ROOT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

CORE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{title}</dc:title>
<dc:creator>{author}</dc:creator>
<cp:lastModifiedBy>{author}</cp:lastModifiedBy>
</cp:coreProperties>"""

APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Solid Wall PPTX Generator</Application>
<Company>Solid Wall Consulting</Company>
</Properties>"""

PRESPROPS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentationPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>"""

THEME = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Solid Wall">
<a:themeElements>
<a:clrScheme name="Solid Wall">
<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
<a:dk2><a:srgbClr val="0B3D62"/></a:dk2>
<a:lt2><a:srgbClr val="F4F7FA"/></a:lt2>
<a:accent1><a:srgbClr val="0B3D62"/></a:accent1>
<a:accent2><a:srgbClr val="F5B301"/></a:accent2>
<a:accent3><a:srgbClr val="14507A"/></a:accent3>
<a:accent4><a:srgbClr val="1E9E5A"/></a:accent4>
<a:accent5><a:srgbClr val="C0392B"/></a:accent5>
<a:accent6><a:srgbClr val="6C3FB5"/></a:accent6>
<a:hlink><a:srgbClr val="14507A"/></a:hlink>
<a:folHlink><a:srgbClr val="6C3FB5"/></a:folHlink>
</a:clrScheme>
<a:fontScheme name="Solid Wall">
<a:majorFont><a:latin typeface="DejaVu Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
<a:minorFont><a:latin typeface="DejaVu Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
</a:fontScheme>
<a:fmtScheme name="Office">
<a:fillStyleLst>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:schemeClr val="phClr"><a:tint val="50000"/><a:satMod val="300000"/></a:schemeClr></a:gs><a:gs pos="35000"><a:schemeClr val="phClr"><a:tint val="37000"/><a:satMod val="300000"/></a:schemeClr></a:gs><a:gs pos="100000"><a:schemeClr val="phClr"><a:tint val="15000"/><a:satMod val="350000"/></a:schemeClr></a:gs></a:gsLst><a:lin ang="16200000" scaled="1"/></a:gradFill>
<a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:schemeClr val="phClr"><a:shade val="51000"/><a:satMod val="130000"/></a:schemeClr></a:gs><a:gs pos="80000"><a:schemeClr val="phClr"><a:shade val="93000"/><a:satMod val="130000"/></a:schemeClr></a:gs><a:gs pos="100000"><a:schemeClr val="phClr"><a:shade val="94000"/><a:satMod val="135000"/></a:schemeClr></a:gs></a:gsLst><a:lin ang="16200000" scaled="0"/></a:gradFill>
</a:fillStyleLst>
<a:lnStyleLst>
<a:ln w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
<a:ln w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
<a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
</a:lnStyleLst>
<a:effectStyleLst>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
</a:effectStyleLst>
<a:bgFillStyleLst>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"><a:tint val="95000"/></a:schemeClr></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"><a:shade val="63000"/></a:schemeClr></a:solidFill>
</a:bgFillStyleLst>
</a:fmtScheme>
</a:themeElements>
</a:theme>"""

SLIDE_MASTER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld>
<p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
<p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree>
</p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
</p:sldMaster>"""

SLIDE_MASTER_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""

SLIDE_LAYOUT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
<p:cSld name="Vierge">
<p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree>
</p:cSld>
<p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr>
</p:sldLayout>"""

SLIDE_LAYOUT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""

SLIDE_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""


# ----------------------------------------------------------------------------
# Construction des formes (shapes) DrawingML
# ----------------------------------------------------------------------------

def _rect(sp_id, name, x, y, cx, cy, fill_hex):
    return f"""<p:sp>
<p:nvSpPr><p:cNvPr id="{sp_id}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="{fill_hex}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
</p:sp>"""


def _para(text, size, color, bold=False, bullet=False, level=0, align="l"):
    b = ' b="1"' if bold else ''
    run = f'<a:rPr lang="fr-FR" sz="{size}"{b}><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr>'
    if bullet:
        buChar = '<a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>'
        pPr = f'<a:pPr marL="{285750}" indent="-285750" lvl="{level}" algn="{align}">{buChar}</a:pPr>'
    else:
        pPr = f'<a:pPr lvl="{level}" algn="{align}"><a:buNone/></a:pPr>'
    return f'<a:p>{pPr}<a:r>{run}<a:t>{escape(text)}</a:t></a:r></a:p>'


def _textbox(sp_id, name, x, y, cx, cy, paragraphs_xml, anchor="t"):
    return f"""<p:sp>
<p:nvSpPr><p:cNvPr id="{sp_id}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
<p:txBody><a:bodyPr wrap="square" anchor="{anchor}"><a:normAutofit/></a:bodyPr><a:lstStyle/>{paragraphs_xml}</p:txBody>
</p:sp>"""


def _pic(sp_id, name, x, y, cx, cy, rid):
    return f"""<p:pic>
<p:nvPicPr><p:cNvPr id="{sp_id}" name="{name}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
</p:pic>"""


def png_size(path):
    """Largeur, hauteur en pixels lues dans l'entete IHDR du PNG."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def fit_box(px, py, max_w, max_h, img_w, img_h):
    """Place une image dans (max_w x max_h) en gardant le ratio, centree."""
    aspect = img_w / img_h
    if max_w / aspect <= max_h:
        w, h = max_w, int(max_w / aspect)
    else:
        w, h = int(max_h * aspect), max_h
    x = px + (max_w - w) // 2
    y = py + (max_h - h) // 2
    return x, y, w, h


def slide_xml(shapes_xml):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
{shapes_xml}
</p:spTree></p:cSld>
<p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr>
</p:sld>"""


# ----------------------------------------------------------------------------
# Mise en page des trois types de slides
# ----------------------------------------------------------------------------

def build_title_slide(title, subtitle, author):
    shapes = []
    sid = 2
    # bandeau jaune en haut
    shapes.append(_rect(sid, "bandeau", 0, 0, EMU_W, 160000, YELLOW)); sid += 1
    # marque
    shapes.append(_textbox(sid, "brand", 700000, 1500000, 10800000, 600000,
        _para("SOLID WALL CONSULTING", 1600, YELLOW, bold=True), anchor="t")); sid += 1
    # titre
    shapes.append(_textbox(sid, "title", 700000, 2400000, 10800000, 1800000,
        _para(title, 4400, BLUE, bold=True), anchor="t")); sid += 1
    # sous-titre
    shapes.append(_textbox(sid, "subtitle", 700000, 4100000, 10800000, 800000,
        _para(subtitle, 2200, DARKBLUE2), anchor="t")); sid += 1
    # formateur
    shapes.append(_textbox(sid, "author", 700000, 5600000, 10800000, 600000,
        _para("Formateur : " + author, 1500, GREY), anchor="t")); sid += 1
    # bandeau jaune en bas
    shapes.append(_rect(sid, "bandeau bas", 0, EMU_H - 90000, EMU_W, 90000, YELLOW)); sid += 1
    return slide_xml("\n".join(shapes))


def build_section_slide(title, subtitle, note=""):
    shapes = []
    sid = 2
    # fond bleu plein
    shapes.append(_rect(sid, "fond", 0, 0, EMU_W, EMU_H, BLUE)); sid += 1
    # barre jaune
    shapes.append(_rect(sid, "barre", 700000, 3050000, 2600000, 90000, YELLOW)); sid += 1
    shapes.append(_textbox(sid, "title", 700000, 2550000, 10800000, 1200000,
        _para(title, 4000, WHITE, bold=True), anchor="t")); sid += 1
    if subtitle:
        shapes.append(_textbox(sid, "subtitle", 700000, 3300000, 10800000, 900000,
            _para(subtitle, 2000, YELLOW), anchor="t")); sid += 1
    if note:
        shapes.append(_textbox(sid, "note", 700000, EMU_H - 700000, 10800000, 500000,
            _para(note, 1300, "AEC2D6"), anchor="t")); sid += 1
    return slide_xml("\n".join(shapes))


def build_content_slide(title, bullets, image=None, image_rid="rId2"):
    shapes = []
    sid = 2
    # barre jaune verticale à gauche du titre
    shapes.append(_rect(sid, "accent", 600000, 480000, 70000, 700000, YELLOW)); sid += 1
    # titre
    shapes.append(_textbox(sid, "title", 760000, 430000, 10700000, 900000,
        _para(title, 2800, BLUE, bold=True), anchor="t")); sid += 1
    # filet sous le titre
    shapes.append(_rect(sid, "filet", 600000, 1320000, 11000000, 18000, "CDD6E0")); sid += 1
    # largeur du corps : reduite si une image occupe la colonne de droite
    body_w = 5650000 if image else 10700000
    # corps : puces
    paras = []
    for b in bullets:
        if isinstance(b, tuple):
            txt, lvl = b
        else:
            txt, lvl = b, 0
        size = 1900 if lvl == 0 else 1600
        color = "1F2329" if lvl == 0 else GREY
        paras.append(_para(txt, size, color, bullet=True, level=lvl))
    body = "".join(paras) if paras else "<a:p/>"
    shapes.append(_textbox(sid, "body", 760000, 1560000, body_w, 4900000, body, anchor="t")); sid += 1
    # image dans la colonne de droite
    if image:
        path = os.path.join(IMGDIR, image)
        size = png_size(path) if os.path.exists(path) else None
        if size:
            x, y, w, h = fit_box(6550000, 1620000, 5100000, 4500000, size[0], size[1])
            shapes.append(_pic(sid, "image", x, y, w, h, image_rid)); sid += 1
    return slide_xml("\n".join(shapes))


# ----------------------------------------------------------------------------
# Assemblage du paquet
# ----------------------------------------------------------------------------

def assemble_slides():
    """Insere le Chapitre 7 (Scrum) au debut du Module 1 (Agilite)."""
    combined = []
    for s in SLIDES:
        combined.append(s)
        if s.get("type") == "section" and s.get("title", "").startswith("Module 1"):
            combined.extend(CH7_SLIDES)
    return combined


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    rendered = []   # (xml, image_filename_or_None)
    rendered.append((build_title_slide(TITLE, SUBTITLE, AUTHOR), None))
    for s in assemble_slides():
        if s["type"] == "section":
            xml = build_section_slide(s["title"], s.get("subtitle", ""), s.get("note", ""))
            rendered.append((xml, None))
        else:
            img = s.get("image")
            # une image presente dans le slide est toujours referencee par rId2
            if img and not os.path.exists(os.path.join(IMGDIR, img)):
                img = None
            xml = build_content_slide(s["title"], s["bullets"], image=img)
            rendered.append((xml, img))

    n = len(rendered)

    slide_overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, n + 1))

    # presentation.xml : liste des slides
    sldid = "".join(
        f'<p:sldId id="{255 + i}" r:id="rId{i + 1}"/>' for i in range(n))
    presentation = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" saveSubsetFonts="1">
<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{n + 1}"/></p:sldMasterIdLst>
<p:sldIdLst>{sldid}</p:sldIdLst>
<p:sldSz cx="{EMU_W}" cy="{EMU_H}"/>
<p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""

    # presentation.xml.rels : slides + master + theme + presProps
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i in range(n):
        rels.append(f'<Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i + 1}.xml"/>')
    rels.append(f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>')
    rels.append(f'<Relationship Id="rId{n + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>')
    rels.append(f'<Relationship Id="rId{n + 3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>')
    rels.append('</Relationships>')
    presentation_rels = "\n".join(rels)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES.format(slide_overrides=slide_overrides))
        z.writestr("_rels/.rels", RELS_ROOT)
        z.writestr("docProps/core.xml", CORE.format(title=escape(TITLE), author=escape(AUTHOR)))
        z.writestr("docProps/app.xml", APP)
        z.writestr("ppt/presentation.xml", presentation)
        z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels)
        z.writestr("ppt/presProps.xml", PRESPROPS)
        z.writestr("ppt/theme/theme1.xml", THEME)
        z.writestr("ppt/slideMasters/slideMaster1.xml", SLIDE_MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", SLIDE_MASTER_RELS)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", SLIDE_LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", SLIDE_LAYOUT_RELS)

        media = {}   # filename -> media index (dedup des images partagees)
        for i, (xml, img) in enumerate(rendered, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", xml)
            if img:
                if img not in media:
                    media[img] = len(media) + 1
                    z.write(os.path.join(IMGDIR, img),
                            f"ppt/media/image{media[img]}.png")
                slide_rels = (
                    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                    f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image{media[img]}.png"/>'
                    '</Relationships>')
                z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels)
            else:
                z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", SLIDE_RELS)

    print(f"OK -> {OUT}  ({os.path.getsize(OUT)//1024} KB, {n} slides, "
          f"{len(media)} images)")


if __name__ == "__main__":
    build()
