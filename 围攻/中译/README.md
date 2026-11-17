# 《围攻》（SIEGE）中译

詹姆斯·梅森《围攻：詹姆斯·梅森文集》第五版（2021）全书中译。

- **原著**：James Mason, *SIEGE: The Collected Writings of James Mason*, 5th Edition, 2021（632 页）
- **底本**：Internet Archive `siege-5th-edition_202505`（632 页 / 46.28 MB / 含文字层）
- **篇幅**：全书 632 个 PDF 页全部译出；汉字约 26.7 万
- **交付**：`SIEGE-中译-第五版.pdf`（276 页 / 3.06 MB，纯文字版）、`SIEGE-中译-第五版.docx`（可编辑）、`SIEGE-中译-第五版.md`（工作稿源文件）

## 体例

1. 页标两个：`［PDF n］` 是 PDF 顺序页，`［p.n］` 是原书印刷页码；**PDF 页比印刷页大 10**。
2. 全书按 PDF 顺序切成 62 个单元，译完追加，不重排既有段落。
3. **交付版只排文字**：原书插图不排入，图注降为小字说明并去掉「原书整页影印：」这类模板前缀；整页没有文字的版面留一行「原书此页为整页影印图版／照片，中译本从略」。
4. 固定译名见文末术语表：`Nationalsozialismus` 的 *National* 译「民族的」，作「民族社会主义」，不作「国家社会主义」；SIEGE 作《围攻》，Atomwaffen Division 作「原子武器师」，NATIONAL-SOCIALIST 作「民族社会主义」。
5. 原文引号、撇号多处编码错乱（显示成替换方块），按语义还原；辨不清标〔辨不清〕，据上下文推定者标〔拟〕。

## 加工链（不再经过 Word）

```
工作稿 md → make_text_only.py（去图、图注转小字）→ md2html.py（HTML + 排版样式）
          → msedge --headless --print-to-pdf（秒级出 PDF）
          → python-docx（可选，出可编辑 docx）
```

Word 只在这两种场合才需要：要交 .doc 老格式，或要人工加批注。

## 已知取舍

- 交付版没有页码、页眉、自动目录。定位靠正文里的 `［PDF n］［p.n］` 页标。
- 图版页面（主要在附录一至六）只留文字说明，原图不在本仓内。
