"""Build all project documentation PDFs from docs-src/*.md.

Requirements for documentation generation:
    pandoc
    weasyprint

Run from the project root:
    python tools/build_docs.py
"""
import html
import json
import re
import subprocess
from pathlib import Path
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs-src"

CSS = """
@page { size: A4; margin: 10mm 8mm 10mm 8mm; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt; line-height: 1.35; color: #111; margin: 0 auto; padding: 0 !important; max-width: none !important; width: 100%; box-sizing: border-box; }
h1 { font-size: 19pt; text-align: center; margin: 0 0 8pt; }
h2 { font-size: 13.5pt; margin: 12pt 0 5pt; border-bottom: 1px solid #999; padding-bottom: 2pt; }
h3 { font-size: 11.5pt; margin: 9pt 0 3pt; }
p { margin: 5pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt auto 9pt; font-size: 9pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #555; padding: 3pt 4pt; vertical-align: top; text-align: left; }
th { background: #e8e8e8; }
pre { background: #f4f4f4; border: 1px solid #bbb; padding: 6pt; font-size: 8pt; line-height: 1.2; white-space: pre-wrap; }
code { font-family: Consolas, monospace; font-size: 8.7pt; }
img { max-width: 100%; border: 1px solid #bbb; margin: 4pt 0; }
.hdr { width: 100% !important; table-layout: fixed; }
.hdr td:first-child { width: 25%; font-weight: bold; background: #f0f0f0; }
blockquote { margin: 6pt 10pt; }
ul, ol { margin-top: 3pt; margin-bottom: 5pt; }
"""


def make_header(marks: str, values: dict) -> str:
    rows = [
        ("Date", values["date"]),
        ("Team ID", values["team_id"]),
        ("Project Name", values["project_name"]),
        ("Maximum Marks", marks),
    ]
    body = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{html.escape(str(v))}</td></tr>"
        for k, v in rows
    )
    return f'<table class="hdr">{body}</table>'


def prepare_markdown(md_path: Path, values: dict) -> str:
    text = md_path.read_text(encoding="utf-8")
    text = re.sub(
        r"\{\{HEADER:(.+?)\}\}",
        lambda m: make_header(m.group(1), values),
        text,
    )
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def main() -> None:
    values = json.loads((SRC / "project.json").read_text(encoding="utf-8"))
    files = sorted(SRC.rglob("*.md"))

    for md in files:
        if md.name.startswith("_"):
            continue
        prepared = prepare_markdown(md, values)
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "html5", "--standalone", "--metadata", "title="],
            input=prepared,
            text=True,
            capture_output=True,
            cwd=SRC,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        document = result.stdout.replace(
            "</head>", f"<style>{CSS}</style></head>", 1
        )
        output = ROOT / md.relative_to(SRC).with_suffix(".pdf")
        output.parent.mkdir(parents=True, exist_ok=True)
        HTML(string=document, base_url=str(md.parent)).write_pdf(str(output))
        print("built", output.relative_to(ROOT))


if __name__ == "__main__":
    main()
