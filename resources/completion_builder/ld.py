#! /usr/bin/env python3

import json
import pandas as pd
from argparse import ArgumentParser

from SpreadsheetFunction import APP_SUFFIXES, SpreadsheetFunction

def dump_function_args(sheet_app: str, write_json_file: bool = True):

    # Must use na_filter = False to prevent the func_name field of the NA() function's object being set to null.
    ref_file = pd.read_excel(
        f'{sheet_app}_funcs_ref.xlsx',
        sheet_name='Sheet1',
        na_filter=False
    ).to_json(orient='records', indent=4)

    if write_json_file:
        with open(f'{sheet_app}_funcs_ref.json', 'w') as o:
            o.write(ref_file)

    return ref_file


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Dump spreadsheet function descriptions to JSON from Excel')
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

    dump_function_args(args.spreadsheet_app, args.dump_json)
