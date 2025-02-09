#! /usr/bin/env python3

import json
import sys
from argparse import ArgumentParser

from SpreadsheetFunction import APP_SUFFIXES, SpreadsheetFunction

SKIPPED_FUNCTIONS = [
    'TRUE',
    'FALSE',
]


def merge_function_args_with_desc(sheet_app: str, write_json_file: bool = True):
    # completion-arg functions file
    func_file = open(f'{sheet_app}_funcs.json', 'r')
    js_func = json.load(func_file)
    func_file.close()

    # Permute the functions for quick lookup
    js_func = {f['func_name']: f for f in js_func}

    # function description and category file
    ref_file = open(f'{sheet_app}_funcs_ref.json', 'r')
    js_ref = json.load(ref_file)
    ref_file.close()

    print('Length of Reference List: ' + str(len(js_ref)))
    print('Length of Completions List: ' + str(len(js_func)))

    # Goal: For each object in _ref,
    #           if "is_nullary" == True:
    #               (DONE) look for a matching function in _func and return the "comp_str" field, then load it into a new field for the current object in _ref.
    #           if "is_nullary" == False:
    #               generate a nullary-specific completion string using f'={func_name}()', then load it into a new field for the current object in _ref.

    functions = []
    for ref in js_ref:
        function = SpreadsheetFunction.from_json(ref)
        if function.name in SKIPPED_FUNCTIONS:
            continue
        if ref['is_nullary']:
            functions.append(function)
            continue

        try:
            lookup = js_func[function.name]
            if function.name == 'IMAGE':
                print(function.to_json())
                print(lookup)
            function.required_args = lookup['req_param']
            function.optional_args = lookup['opt_param']
            function.has_ellipsis = lookup['ellipsis']
            if function.name == 'IMAGE':
                print('after')
                print(function.to_json())
                # print(lookup)
        except:
            print("\nError when when matching comp_str for nonnullary function:")
            print(f'{function.name=}')
            print(f'{lookup=}')

        functions.append(function)


    print(f'Length of Master List: {len(functions)}')

    if write_json_file:
        with open(f'{sheet_app}_funcs_master.json', 'w') as o:
            json.dump([f.to_json() for f in functions], o, indent=4)

    return functions


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Merge spreadsheet function metadata with their arguments')
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

    merge_function_args_with_desc(args.spreadsheet_app, args.dump_json)
