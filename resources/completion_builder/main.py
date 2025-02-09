#! /usr/bin/env python3

import json
from argparse import ArgumentParser

from SpreadsheetFunction import APP_SUFFIXES, SpreadsheetFunction
from js import parse_function_list
from ld import dump_function_args
from mg import merge_function_args_with_desc

def main(sheet_app: str, write_intermediate_json: bool):

    # TODO: pass the data seamlessly without dumping files
    parse_function_list(sheet_app, write_intermediate_json)
    dump_function_args(sheet_app, write_intermediate_json)
    functions = merge_function_args_with_desc(sheet_app, write_intermediate_json)

    completions = {
        "scope": f'source.sheet.{sheet_app} - string - comment',
        "completions": [f.to_sublime_snippet_completion() for f in functions] +
                       [f.to_sublime_word_completion() for f in functions],
    }

    with open('.sublime-completions', 'w') as o:
        json.dump(completions, o, indent=4)


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Construct spreadsheet app function completions')
    parser.add_argument(
        '-s', '--spreadsheet-app',
        choices=APP_SUFFIXES,
        default='excel',
        help='spreadsheet application')
    parser.add_argument(
        '-j', '--dump-json',
        type=bool,
        default=True,
        help='dump JSON output to a file')
    args = parser.parse_args()

    main(args.spreadsheet_app, args.dump_json)
