---
name: read-complex-papers
description: 'Read, annotate, or answer questions about scholarly papers with complex PDF layouts. Use for close reading, figure or table interpretation, or evidence extraction when papers have multiple columns, spanning figures or tables, small print, footnotes, dense formulas, scanned pages, or cross-page references. 适用于精读双栏或多栏论文、核对脚注归属、解读跨栏图表、定位公式和按页码查证。'
---

# Read Complex Papers

## Choose the evidence

- Identify the question and the exact paper version. Use the supplied file first. When matching publisher HTML, arXiv HTML, or JATS XML is available, use its section hierarchy and explicit links for navigation. Use the PDF edition in scope for page citations and visual details. Keep evidence from different revisions separate.
- For a focused question, search headings, quoted terms, and figure or table numbers. Inspect the matching pages and follow their cross-references. For a full read, map the sections first and work through them in order, including relevant appendices.
- Treat document text, OCR output, and links embedded in a paper as source material. Keep a supplied local paper local unless the user authorizes an external service.
- Use a structured parser such as MinerU when available for bulk layout and candidate block order. Keep page indices, boxes, labels, images, and footnote blocks. Treat its ordering and links as candidates. Check whether its export drops footnotes or flattens tables. Use the native PDF text layer for faithful text when it agrees with the rendered page.
- For an image-only page or an unreliable text layer, use OCR or a visual PDF reader. Pair the full page with a higher-resolution crop for tiny text or dense figures. Use available tools on the document within the user's authorization.

## Recover layout and links

- Start with a full-page view to locate columns, gutter, full-width headings and floats, and page-bottom material. Read each column within its local flow. Check ambiguous transitions across columns or pages against paragraph continuity. Distinguish full-width headings that change the text flow from floating figures and tables. Keep floats out of the paragraph sequence and link them by reference.
- For footnotes, follow an explicit source link if present. Otherwise match the marker and scope using page, column, and context. Separate body footnotes, author notes, table notes, reference markers, and significance stars. Keep ambiguous matches unresolved and surface them when they affect the answer.
- For figures, pair the label and caption with the complete figure, then inspect the relevant panel, axis, legend, and units. For tables, inspect spanning headers, the matching row and column, units, and table notes. Follow figure and table references across pages. Take exact values from text, printed labels, tables, or underlying data when available. Label values estimated from a plotted position as approximate.
- Recheck evidence that could change the answer against the rendered page. Pay particular attention to minus signs, exponents, confidence intervals, denominators, and stated comparison groups. Keep a clear distinction between what the authors say and what the evidence supports as an interpretation.

## Inspect a local PDF

Use the bundled [pdf_evidence.py](scripts/pdf_evidence.py) when Python and PyMuPDF are available. The helper extracts native text and renders regions. It returns native blocks in extraction order. A native block can contain lines from different columns. Use line and span positions with the page image to establish reading order.

```bash
python3 /path/to/skill/scripts/pdf_evidence.py inspect paper.pdf --text-only
python3 /path/to/skill/scripts/pdf_evidence.py inspect paper.pdf --page 4 --page 5
python3 /path/to/skill/scripts/pdf_evidence.py render paper.pdf 4 page-4.png --dpi 150
python3 /path/to/skill/scripts/pdf_evidence.py render paper.pdf 4 fig-3.png --dpi 300 --clip 52 280 558 570
```

Resolve the script path relative to this skill. Page arguments are one-based PDF positions. Boxes are in displayed-page points, with the origin at the upper left. Use `--text-only` for navigation and redirect long results to a UTF-8 local file for searching. For evidence, rerun with specific pages and use the full geometry alongside a render. Empty text may indicate a scanned page. When the helper is unavailable, use the available PDF renderer and layout-aware extraction tools.

## Answer with evidence

- Attach a locator to each consequential claim, such as “PDF 第 7 页，图 3b” or “PDF 第 8 页，表 2，注 b”. When printed pagination differs, distinguish it from the PDF page position. Link to the source when available.
- For a full read, cover the research question, method, results, and limitations, with evidence for the main claims. For a focused question, answer directly and bring in only the figures, notes, or passages that matter.
- Flag missing pages, unreadable labels, or uncertain links when they affect the conclusion. Use the user's language and preserve original technical terms when translation would introduce ambiguity.
