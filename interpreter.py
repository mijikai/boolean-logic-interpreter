#!/usr/bin/env python3
from truthtable import TruthTable
from bool_parser import parse
from pyparsing import ParseException
try:
    import readline
except ImportError:
    pass

prompt = "bool$: "


def loop():
    while True:
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            print('Goodbye!')
            break
        line = line.strip()
        
        if not line:
            continue

        try:
            expr = parse(line)
        except ParseException as ex:
            print(ex)
            continue

        table = TruthTable(expr)
        table.display_table()

if __name__ == '__main__':
    loop()
