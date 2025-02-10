#! /usr/bin/env python3

import json
import re
from argparse import ArgumentParser

from SpreadsheetFunction import APP_SUFFIXES, SpreadsheetFunction

def parse_function_list(sheet_app: str, write_json_file: bool = True):

    with open(f'{sheet_app}_funcs_data_list.txt', 'r') as file:
        lines = [line.strip() for line in file]

    # Debug
    # lines = ['CALL~register_id,[argument1],...']

    functions = []

    for line in lines:
        func_name, param_str = line.split('~')
        param_list = param_str.split(',')
        req_param = []
        opt_param = []

        ellipsis = False

        for param in param_list:
            if param[0] == '[':
                opt_param.append(re.sub(r'[\[\]]', '', param))

            elif param[0] == '.':
                ellipsis = True

            else:
                req_param.append(param)

        function = SpreadsheetFunction(
            func_name,
            required_args = req_param,
            optional_args = opt_param,
            has_ellipsis = ellipsis,
        )

        functions.append(function)

    if write_json_file:
        with open(f'{sheet_app}_funcs.json', 'w') as o:
            json.dump([f.to_json() for f in functions], o, indent=4)

    return functions


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Parse ~-delimited spreadsheet function list from a file')
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

    parse_function_list(args.spreadsheet_app, args.dump_json)
