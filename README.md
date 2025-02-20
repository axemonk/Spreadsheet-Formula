# [Spreadsheet Formula for Sublime Text][gh]

Spreadsheet formula syntax highlighting for Sublime Text. This syntax was originally
intended to only provide support for Excel formulae, but now also supports both Google Sheets
and LibreOffice Calc formulae.

The Excel variant (see [Usage](#usage)) of this syntax can also be used as a rough syntax highlighter
for DAX code used in Power Pivot and Power BI. I haven't run into any major issues using
it for that purpose so far. It will occassionally miss a keyword here and there, like the NOT in
`NOT ISBLANK(...`.

## Features

- Syntax highlighting for spreadsheet formulae used in Excel, Google Sheets, and LibreOffice Calc
- Built-in function completions
- Support for [locale-specific separators](#localization)
- SQL highlighting when using the `QUERY()` function in Google Sheets

## Installation

[Install][pc-install] via Package Control.

## Usage

1. In Sublime, open or navigate to a `.txt` file containing the spreadsheet
formulae you wish to be highlighted (or create a new file with <kbd>Ctrl</kbd>+<kbd>N</kbd>).
2. Activation options:
   - Depending on what spreadsheet application you plan on using, select the corresponding
   "(...) formula" syntax option from the syntax selection menu at the bottom right of Sublime Text.
   - Alternatively, open the Command Palette and type "formula". Select the option
   corresponding to your application of choice ("Set Syntax: (...) formula").
3. Enjoy!

New files will be saved with a two-level extension to signal Sublime Text to
use the right syntax in the future.

### Localization

Some locales use different characters for decimal numbers, function argument
separators, and array separators. If your locale differs from the characters
chosen by this package (US, decimal: `.`, argument: `,`, row: `,`, column: `;`),
you can make small extension syntax files to enable your local preferences.

Add a file containing one of the below code blocks in your `Packages/User` folder,
then modify the regular expression patterns in the `variables:` context to match your locale's format.
  - Since certain characters serve special roles in regex patterns, you can specify them as literal characters with `\`.
    - E.g., `.`, `*`, and `\` must be made literal like `\.`, `\*`, and `\\` in order for them to be used in the below variables.

The below examples denote a French locale with `(FR)` and `fr` where applicable.

If using Excel:

Filename `Excel Formula (FR).sublime-syntax`:
```yaml
%YAML 1.2
---
name: Excel Formula (FR)
scope: source.sheet.excel.fr
version: 2
extends: Excel Formula.sublime-syntax
file_extensions:
  - fr.xls.txt

variables:
  array_column_separator: ';'
  array_row_separator: '\\'
  number_radix: ','
  argument_separator: ';'
```

If using Google Sheets:

Filename `Google Sheets Formula (FR).sublime-syntax`:
```yaml
%YAML 1.2
---
name: Google Sheets Formula (FR)
scope: source.sheet.google.fr
version: 2
extends: Google Sheets Formula.sublime-syntax
file_extensions:
  - fr.google.txt

variables:
  array_column_separator: ';'
  array_row_separator: '\\'
  number_radix: ','
  argument_separator: ';'
```

If using LibreOffice Calc:

Filename `LibreOffice Calc Formula (FR).sublime-syntax`:
```yaml
%YAML 1.2
---
name: LibreOffice Calc Formula (FR)
scope: source.sheet.libre.fr
version: 2
extends: LibreOffice Calc Formula.sublime-syntax
file_extensions:
  - fr.localc.txt

variables:
  array_column_separator: ';'
  array_row_separator: '\\'
  number_radix: ','
  argument_separator: ';'
```

## Contributing

### Issues

Please send any bug reports or suggestions by opening an issue on Github
or to \_alco via a direct message on Discord.
You can find me on the official Sublime Text Discord server.

## Credits

Made by \_alco and [michaelblyons][]. Thanks to acid_form for the first key bug
reports we've received and for scraping the Google Sheets builtin functions.

A **huge** thank you to [michaelblyons][] for his collaboration.

[gh]: https://github.com/axemonk/Excel-formula
[pc-install]: https://packagecontrol.io/installation
[michaelblyons]: https://github.com/michaelblyons
