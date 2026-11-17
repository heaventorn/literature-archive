# -*- coding: utf-8 -*-
"""2_md2html.py — 纯文字版 md 转 HTML（A4 排版、宋体正文、黑体标题、页标灰小字）。

用法：python 2_md2html.py
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "_build", "纯文字.md")
OUT = os.path.join(ROOT, "_build", "纯文字.html")

CSS = """
@page { size: A4; margin: 24mm 22mm 20mm 22mm; }
html, body { margin: 0; padding: 0; }
body { font-family: "SimSun", "宋体", serif; font-size: 10.5pt; line-height: 1.62; color: #000; }
p { margin: 0 0 3pt 0; text-indent: 2em; text-align: justify; }
h1 { font-family: "SimHei", "黑体", sans-serif; font-size: 16pt; text-align: center;
     margin: 6pt 0 12pt 0; page-break-before: always; font-weight: normal; }
h1.first { page-break-before: avoid; }
h2 { font-family: "SimHei", "黑体", sans-serif; font-size: 14pt; margin: 12pt 0 6pt 0; font-weight: normal; }
h3 { font-family: "SimHei", "黑体", sans-serif; font-size: 12pt; margin: 10pt 0 4pt 0; font-weight: normal; }
.mk { font-family: "KaiTi", "楷体", monospace; font-size: 9pt; color: #666; margin: 8pt 0 2pt 0;
      text-indent: 0; page-break-after: avoid; }
.note { font-family: "KaiTi", "楷体", sans-serif; font-size: 9.5pt; color: #444;
        text-align: justify; text-indent: 2em; margin: 2pt 0 4pt 0; }
.center { font-family: "SimHei", "黑体", sans-serif; font-size: 11pt; text-align: center;
          text-indent: 0; margin: 4pt 0; }
blockquote { font-family: "KaiTi", "楷体", sans-serif; font-size: 9.5pt; margin: 3pt 0 3pt 8mm;
             text-align: justify; }
table { border-collapse: collapse; margin: 6pt 0; width: 100%; font-size: 9.5pt; }
th, td { border: 0.5pt solid #999; padding: 2pt 4pt; text-align: left; text-indent: 0; }
th { background: #eee; font-family: "SimHei", "黑体", sans-serif; font-weight: normal; }
ul { margin: 4pt 0 4pt 6mm; padding: 0; }
li { font-size: 10pt; line-height: 1.5; }
"""


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", t)
    return t


lines = open(SRC, encoding="utf-8").read().split("\n")
buf = []
h1_seen = False
i = 0
while i < len(lines):
    s = lines[i].strip()
    i += 1
    if not s:
        continue
    if re.fullmatch(r"-{3,}", s):
        continue
    if s.startswith("|"):
        rows = []
        while i - 1 < len(lines):
            cur = lines[i - 1].strip()
            if not cur.startswith("|"):
                break
            rows.append(cur)
            i += 1
        i -= 1
        body = [r for r in rows if not re.fullmatch(r"[|\-: ]+", r)]
        if body:
            html_rows = []
            for k, r in enumerate(body):
                cells = [c.strip() for c in r.strip("|").split("|")]
                tag = "th" if k == 0 else "td"
                tds = "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells)
                html_rows.append(f"<tr>{tds}</tr>")
            buf.append("<table>" + "".join(html_rows) + "</table>")
        continue
    if s.startswith("- "):
        items = []
        while i - 1 < len(lines) and lines[i - 1].strip().startswith("- "):
            items.append(f"<li>{inline(lines[i - 1].strip()[2:])}</li>")
            i += 1
        i -= 1
        buf.append("<ul>" + "".join(items) + "</ul>")
        continue
    if s.startswith("!["):
        continue
    if s.startswith("图注："):
        buf.append(f'<p class="note">{inline(s[3:])}</p>')
        continue
    if re.fullmatch(r"［PDF \d+］.*", s):
        buf.append(f'<p class="mk">{inline(s)}</p>')
        continue
    if s.startswith("### "):
        buf.append(f"<h3>{inline(s[4:])}</h3>")
        continue
    if s.startswith("## "):
        buf.append(f"<h2>{inline(s[3:])}</h2>")
        continue
    if s.startswith("# "):
        cls = "" if h1_seen else ' class="first"'
        h1_seen = True
        buf.append(f"<h1{cls}>{inline(s[2:])}</h1>")
        continue
    if s.startswith("@center "):
        buf.append(f'<p class="center">{inline(s[8:])}</p>')
        continue
    if s.startswith("> "):
        buf.append(f"<blockquote>{inline(s[2:])}</blockquote>")
        continue
    buf.append(f"<p>{inline(s)}</p>")

doc = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
       f"<title>围攻 中译</title><style>{CSS}</style></head><body>\n"
       + "\n".join(buf) + "\n</body></html>\n")
open(OUT, "w", encoding="utf-8").write(doc)
print("html", OUT, len(doc), "blocks", len(buf))
