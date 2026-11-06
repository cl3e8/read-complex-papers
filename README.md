# Read Complex Papers

A Codex skill for closely reading complex PDF papers and answering questions grounded in the source. It handles layouts with multiple columns, figures and tables that span columns, small footnotes, equations, and scanned pages. Answers cite PDF page numbers and relevant figure, table, equation, or footnote identifiers so you can verify them in the paper.

## Install in Codex

Download or clone this repository. Copy the inner `read-complex-papers/` directory into `~/.agents/skills/` for personal use or into `.agents/skills/` in your project. The skill entry point should be at `.agents/skills/read-complex-papers/SKILL.md` relative to your home or project directory. Invoke it in Codex with `$read-complex-papers`.

The local PDF helper requires Python and PyMuPDF. Run this command from the repository root. On Windows, you can use `py` in place of `python`.

```sh
python -m pip install -r requirements.txt
```

## Example prompts

- `$read-complex-papers` Read the attached paper closely. Summarize the research question, methods, main findings, and limitations. Cite the PDF page for each key claim.
- `$read-complex-papers` Which of the authors' claims does Figure 3b support? Check the axes, units, legend, and the passage that refers to the figure.
- `$read-complex-papers` Which samples does footnote b in Table 2 apply to? Does it affect the comparison the authors report between groups?

## Inspect PDF evidence from the command line

```sh
python read-complex-papers/scripts/pdf_evidence.py inspect paper.pdf --text-only > index.json
python read-complex-papers/scripts/pdf_evidence.py inspect paper.pdf --page 4
python read-complex-papers/scripts/pdf_evidence.py render paper.pdf 4 page-4.png --dpi 150
```

`inspect` emits UTF-8 JSON. By default, it includes coordinates for text blocks, lines, and spans. The text index follows the PDF's extraction order. Use the rendered page to check the reading order across columns. Scanned pages may yield empty text, so the skill uses visual reading or OCR when available. The model that invokes the skill answers the questions.
