# odt-to-txt

Converts an OpenDocument Text (`.odt`) file to a plain text file. Comments left in the document are preserved inline, marking both the comment itself and the text it refers to:

```
[c/ comment text] the text being commented on [/c]
```

## Requirements

Install the `odfpy` library before use:

```
pip install odfpy
```

## Usage

Run the following command in the same directory as `odt_to_txt.py`:

```
python odt_to_txt.py input.odt output.txt
```

If no output file is specified, the output will be saved with the same name as the input file and a `.txt` extension:

```
python odt_to_txt.py input.odt
# saves to input.txt
```

## Output format

Regular document text is output as-is. Where a comment exists in the original file, the comment text appears first in a `[c/ ]` opening marker, followed by the passage it annotates, closed by `[/c]`:

```
...the bill was widely considered [c/ do you have a source for this?] the most consequential legislation of the decade [/c], drawing opposition from...
```

If a comment is not anchored to a specific passage, only the opening marker appears with no closing tag.

## Reason

The reason why i made this was because I needed to give Gemini CLI an essay with comments, but no filetype it supported also supported comments. So instead of going and putting in the comments manually, I made this script to do it automatically.
