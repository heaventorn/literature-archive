# -*- coding: utf-8 -*-
"""1_make_text_only.py — 由带图工作稿 md 派生纯文字版 md。

图片本身不保留；图注保留为小字说明，去掉「原书整页影印：」一类模板前缀；
整页没有文字的版面补一行「中译本从略」。
用法：python 1_make_text_only.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "SIEGE-中译-第五版.md")
BUILD = os.path.join(ROOT, "_build")
DST = os.path.join(BUILD, "纯文字.md")
NOTE = "（原书此页为整页影印图版／照片，中译本从略。）"
STRIP_PREFIX = re.compile(
    r"^(?:原书整页影印[:：]?|原书整页照片[:：]?|原书整页影印[／/]照片[:：]?)+"
)

os.makedirs(BUILD, exist_ok=True)

lines = open(SRC, encoding="utf-8").read().split("\n")
out = []
drop_img = keep_cap = 0
for ln in lines:
    s = ln.strip()
    if s.startswith("!["):
        drop_img += 1
        continue
    m = re.match(r"^\*?图注[：:]\s*(.+?)\*?$", s)
    if m:
        cap = STRIP_PREFIX.sub("", m.group(1).strip()).strip()
        if cap:
            out.append("图注：" + cap)
            keep_cap += 1
        continue
    out.append(ln)


def is_marker(t):
    return re.fullmatch(r"［PDF \d+］.*", t) is not None


res, i, added = [], 0, 0
while i < len(out):
    res.append(out[i])
    if is_marker(out[i].strip()):
        j = i + 1
        while j < len(out) and not out[j].strip():
            j += 1
        nxt = out[j].strip() if j < len(out) else ""
        if (not nxt) or is_marker(nxt) or re.fullmatch(r"-{3,}", nxt) or nxt.startswith("# "):
            res += ["", NOTE]
            added += 1
    i += 1

md = re.sub(r"\n{3,}", "\n\n", "\n".join(res))
open(DST, "w", encoding="utf-8").write(md)
print("images dropped", drop_img, "captions kept", keep_cap, "notes", added)
print("chars", len(md), "hanzi", len(re.findall(r"[\u4e00-\u9fff]", md)))
print("out", DST)
