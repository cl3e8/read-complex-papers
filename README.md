# Read Complex Papers

一个用于精读复杂 PDF 论文和回答原文问题的 Codex Skill。适合双栏或多栏正文、跨栏图表、细小脚注、公式和扫描页。回答会给出 PDF 页码及图、表、公式或脚注编号，便于回到原文核对。

## 安装到 Codex

下载或克隆本仓库后，将内层的 `read-complex-papers/` 目录整体复制到用户的 `~/.agents/skills/`，或复制到目标项目的 `.agents/skills/`。确认安装后的入口为 `.agents/skills/read-complex-papers/SKILL.md`。在 Codex 中输入 `$read-complex-papers` 调用。

本地 PDF 助手需要 Python 和 PyMuPDF。在仓库根目录运行以下命令。Windows 上可使用 `py` 或 `python`。

```sh
python -m pip install -r requirements.txt
```

## 提问示例

- `$read-complex-papers` 精读我附上的论文。按研究问题、方法、主要结果和局限总结，每个关键结论标注 PDF 页码。
- `$read-complex-papers` 图 3b 支持作者的哪项结论？核对坐标轴、单位、图例和正文对该图的引用。
- `$read-complex-papers` 表 2 的脚注 b 限定了哪些样本？它是否影响作者报告的组间比较？

## 命令行取证

```sh
python read-complex-papers/scripts/pdf_evidence.py inspect paper.pdf --text-only > index.json
python read-complex-papers/scripts/pdf_evidence.py inspect paper.pdf --page 4
python read-complex-papers/scripts/pdf_evidence.py render paper.pdf 4 page-4.png --dpi 150
```

`inspect` 输出 UTF-8 JSON，默认保留文本块、行和文本片段的坐标。索引采用 PDF 的提取顺序，跨栏阅读顺序需要结合页面图像判断。扫描页的文本提取可能为空，技能会尝试使用运行环境提供的视觉阅读或 OCR 能力。问答由调用该技能的模型完成。
