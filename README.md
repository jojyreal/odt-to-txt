# odt-to-txt

Converts an OpenDocument Text (.odt) file to a plain text file,
with inline comments preserved using open/close markers:

    [c/ comment text] the text being commented on [/c]

Usage:
    python odt_to_txt.py input.odt output.txt

If no output file is specified, the output filename will mirror
the input filename with a .txt extension.
