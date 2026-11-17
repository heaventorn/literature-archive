# -*- coding: utf-8 -*-
"""3_build_docx.py — 由纯文字版 md 生成可编辑 docx（A4／宋体 10.5／黑体标题）。
用法：python 3_build_docx.py
"""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, "_build", "纯文字.md")
DOCX = os.path.join(ROOT, "SIEGE-中译-第五版.docx")

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Mm(210), Mm(297)
sec.left_margin = sec.right_margin = Mm(22)
sec.top_margin, sec.bottom_margin = Mm(24), Mm(20)

st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_after = Pt(3)


def style_run(r, font="宋体", size=10.5, bold=False, italic=False, color=None):
    r.font.size = Pt(size)
    r.bold, r.italic = bold, italic
    if color is not None:
        r.font.color.rgb = color
    rPr = r._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.insert(0, rf)
    rf.set(qn("w:eastAsia"), font)
    rf.set(qn("w:ascii"), "Times New Roman")
    rf.set(qn("w:hAnsi"), "Times New Roman")


TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*)")


def add_inline(p, text, font="宋体", size=10.5, color=None):
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            style_run(p.add_run(part[2:-2]), font, size, bold=True, color=color)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            style_run(p.add_run(part[1:-1]), font, size, italic=True, color=color)
        else:
            style_run(p.add_run(part), font, size, color=color)


lines = open(MD, encoding="utf-8").read().split("\n")
first_h1 = True
for raw in lines:
    s = raw.strip()
    if not s or re.fullmatch(r"-{3,}", s) or s.startswith("!["):
        continue
    if s.startswith("图注："):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        add_inline(p, s, font="楷体", size=9.5, color=RGBColor(0x44, 0x44, 0x44))
        continue
    if re.fullmatch(r"［PDF \d+］.*", s):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        add_inline(p, s, font="楷体", size=9, color=RGBColor(0x66, 0x66, 0x66))
        continue
    if s.startswith("### "):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        add_inline(p, s[4:], font="黑体", size=12)
        continue
    if s.startswith("## "):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        add_inline(p, s[3:], font="黑体", size=14)
        continue
    if s.startswith("# "):
        if not first_h1:
            doc.add_page_break()
        first_h1 = False
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(10)
        add_inline(p, s[2:], font="黑体", size=16)
        continue
    if s.startswith("@center "):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_inline(p, s[8:], font="黑体", size=11)
        continue
    if s.startswith("> "):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Mm(8)
        add_inline(p, s[2:], font="楷体", size=9.5)
        continue
    if s.startswith("|"):
        continue
    if s.startswith("- "):
        p = doc.add_paragraph(style="List Bullet")
        add_inline(p, s[2:], size=10)
        continue
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(21)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_inline(p, s)

doc.save(DOCX)
print("SAVED", DOCX, os.path.getsize(DOCX))
