#!/usr/bin/env python3
"""
Convert a Markdown report to a simple PDF without external dependencies.

Usage:
    python3 markdown_to_pdf.py input.md output.pdf

The renderer is intentionally conservative: it preserves text, headings, and
tables in a readable wrapped layout. It is meant as a reliable fallback when
pandoc/weasyprint are unavailable.
"""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path


PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT = 54
TOP = 782
BOTTOM = 54
LINE_HEIGHT = 14
FONT_SIZE = 10
TITLE_SIZE = 16
HEADING_SIZE = 13
MAX_CHARS = 88


def strip_markdown(line: str) -> tuple[str, str]:
    raw = line.rstrip()
    if not raw:
        return "", "blank"
    if raw.startswith("# "):
        return raw[2:].strip(), "title"
    if raw.startswith("## "):
        return raw[3:].strip(), "heading"
    if raw.startswith("### "):
        return raw[4:].strip(), "heading"
    if raw.startswith("- "):
        return u"\u2022 " + raw[2:].strip(), "body"
    if re.match(r"^\d+\.\s+", raw):
        return raw, "body"
    if raw.startswith("|") and raw.endswith("|"):
        cells = [c.strip() for c in raw.strip("|").split("|")]
        if cells and all(set(c) <= {"-", ":"} for c in cells):
            return "", "blank"
        return " | ".join(cells), "body"
    raw = re.sub(r"\*\*(.*?)\*\*", r"\1", raw)
    raw = re.sub(r"`([^`]*)`", r"\1", raw)
    raw = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", raw)
    return raw, "body"


def encode_pdf_text(text: str) -> str:
    # Helvetica in standard PDF fonts uses WinAnsiEncoding. Replace unsupported
    # characters while preserving common French punctuation and accents.
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u2022", "*")
    data = text.encode("cp1252", errors="replace").decode("cp1252")
    return data.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def markdown_to_lines(markdown: str) -> list[tuple[str, str]]:
    rendered: list[tuple[str, str]] = []
    for source_line in markdown.splitlines():
        text, style = strip_markdown(source_line)
        if style == "blank":
            rendered.append(("", "blank"))
            continue
        width = 64 if style in {"title", "heading"} else MAX_CHARS
        wrapped = textwrap.wrap(text, width=width, replace_whitespace=False) or [""]
        for item in wrapped:
            rendered.append((item, style))
        if style in {"title", "heading"}:
            rendered.append(("", "blank"))
    return rendered


def paginate(lines: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    pages: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    y = TOP
    for line, style in lines:
        needed = LINE_HEIGHT * (2 if style == "title" else 1)
        if y - needed < BOTTOM and current:
            pages.append(current)
            current = []
            y = TOP
        current.append((line, style))
        y -= needed
    if current:
        pages.append(current)
    return pages


def page_stream(page: list[tuple[str, str]], page_number: int, total: int) -> bytes:
    y = TOP
    parts = ["BT"]
    for text, style in page:
        if style == "blank":
            y -= LINE_HEIGHT
            continue
        if style == "title":
            parts.append(f"/F1 {TITLE_SIZE} Tf")
            step = LINE_HEIGHT * 2
        elif style == "heading":
            parts.append(f"/F1 {HEADING_SIZE} Tf")
            step = LINE_HEIGHT + 3
        else:
            parts.append(f"/F1 {FONT_SIZE} Tf")
            step = LINE_HEIGHT
        parts.append(f"1 0 0 1 {LEFT} {y} Tm ({encode_pdf_text(text)}) Tj")
        y -= step
    parts.append(f"/F1 8 Tf 1 0 0 1 {LEFT} 30 Tm (Page {page_number}/{total}) Tj")
    parts.append("ET")
    return "\n".join(parts).encode("latin-1", errors="replace")


def build_pdf(markdown: str) -> bytes:
    pages = paginate(markdown_to_lines(markdown))
    objects: list[bytes] = []

    def add(obj: bytes) -> int:
        objects.append(obj)
        return len(objects)

    catalog_id = add(b"<< /Type /Catalog /Pages 2 0 R >>")
    pages_id = add(b"")
    font_id = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    content_ids = []

    for index, page in enumerate(pages, start=1):
        stream = page_stream(page, index, len(pages))
        content = (
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"
        )
        content_id = add(content)
        page_id = add(
            (
                f"<< /Type /Page /Parent {pages_id} 0 R "
                f"/MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Resources << /Font << /F1 {font_id} 0 R >> >> "
                f"/Contents {content_id} 0 R >>"
            ).encode()
        )
        content_ids.append(content_id)
        page_ids.append(page_id)

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode()

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj_id, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{obj_id} 0 obj\n".encode())
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n"
        ).encode()
    )
    return bytes(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    markdown = args.input.read_text(encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(build_pdf(markdown))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
