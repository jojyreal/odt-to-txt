"""
odt_to_txt.py

Converts an OpenDocument Text (.odt) file to a plain text file,
with inline comments preserved using open/close markers:

    [c/ comment text] the text being commented on [/c]

Usage:
    python odt-to-txt.py input.odt output.txt

If no output file is specified, the output filename will mirror
the input filename with a .txt extension.
"""

import re
import argparse
from odf.opendocument import load

# Namespace URIs
NS_TEXT   = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
NS_OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
NS_DC     = "http://purl.org/dc/elements/1.1/"

OFFICE_NAME_ATTR = (NS_OFFICE, "name")


def get_ns_tag(element):
    qname = getattr(element, "qname", None)
    return (qname[0], qname[1]) if qname else ("", "")


def extract_comment_text(annotation):
    """Pull only text:p children from an annotation, skipping dc:creator / dc:date."""
    lines = []
    for child in annotation.childNodes:
        ns, tag = get_ns_tag(child)
        if ns == NS_DC:
            continue
        if ns == NS_TEXT and tag == "p":
            lines.append(get_plain_text(child))
    return " ".join(line for line in lines if line).strip()


def get_plain_text(element):
    """Recursively extract plain text, skipping annotations entirely."""
    parts = []
    for child in element.childNodes:
        ns, tag = get_ns_tag(child)
        if hasattr(child, "data"):
            parts.append(child.data)
        elif ns == NS_OFFICE and tag in ("annotation", "annotation-end"):
            continue
        elif ns == NS_TEXT and tag == "line-break":
            parts.append("\n")
        elif ns == NS_TEXT and tag == "tab":
            parts.append("\t")
        elif hasattr(child, "childNodes"):
            parts.append(get_plain_text(child))
    return "".join(parts)


def extract_paragraph(element):
    """
    Walk a text:p or text:h element and emit text interleaved with comment markers.

    When an annotation node is encountered, emit:   [c/ comment text]
    When an annotation-end node is encountered, emit: [/c]
    """
    parts = []
    for child in element.childNodes:
        ns, tag = get_ns_tag(child)

        if hasattr(child, "data"):
            parts.append(child.data)

        elif ns == NS_OFFICE and tag == "annotation":
            comment = extract_comment_text(child)
            if comment:
                parts.append(f"[c/ {comment}]")

        elif ns == NS_OFFICE and tag == "annotation-end":
            parts.append("[/c]")

        elif ns == NS_TEXT and tag == "line-break":
            parts.append("\n")

        elif ns == NS_TEXT and tag == "tab":
            parts.append("\t")

        elif hasattr(child, "childNodes"):
            parts.append(extract_paragraph(child))

    return "".join(parts)


def extract_body(element):
    """Walk the document body, emitting text paragraph by paragraph."""
    result = []
    for child in element.childNodes:
        ns, tag = get_ns_tag(child)

        if ns == NS_TEXT and tag in ("p", "h"):
            result.append(extract_paragraph(child))
            result.append("\n")

        elif ns == NS_TEXT and tag in ("list", "list-item", "section"):
            result.append(extract_body(child))

        elif hasattr(child, "childNodes"):
            result.append(extract_body(child))

    return "".join(result)


def convert(input_path, output_path):
    doc = load(input_path)
    raw = extract_body(doc.body)

    # Collapse 3+ consecutive newlines down to 2
    cleaned = re.sub(r"\n{3,}", "\n\n", raw).strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
        f.write("\n")

    print(f"Converted: {input_path} -> {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert an ODT file to plain text, preserving inline comments."
    )
    parser.add_argument("input", help="Path to the input .odt file")
    parser.add_argument(
        "output",
        nargs="?",
        help="Path to the output .txt file (default: same name as input with .txt extension)",
    )
    args = parser.parse_args()

    input_path = args.input
    if args.output:
        output_path = args.output
    else:
        import os
        base = os.path.splitext(input_path)[0]
        output_path = base + ".txt"

    convert(input_path, output_path)


if __name__ == "__main__":
    main()
