#!/usr/bin/env python3

from bool_parser import parse
from boolean import bool_funcs_dict, CONSTANTS
from itertools import product
from expression import evaluate, evaluate2, Expression, infixRepr
from pyparsing import ParseException


class TruthTable:
    """Generates the truth table for the given string.

    Data defined:
    -> vars: Identifiers in the string
    -> var_combination: A tuple of dictionary of the possilbe combination of
        the truth value
    """

    def __init__(self, expr):
        self._gen_order(expr)
        self._find_variables()
        self._make_combination()

    def _gen_order(self, expr):
        """Remove redundant expression from the list of statements."""
        order = expr.evaluation_order()
        new_order = []
        for i in order:
            if i not in new_order:
                new_order.append(i)
        self.__order = new_order
    def _find_variables(self):
        # Find all the identifier in the expression. Used in order to determine
        # the possible combination of truth table and assign those some value

        vars = set()
        stack = []

        for i in self.__order:
            if not isinstance(i, Expression) and i not in CONSTANTS:
                vars.add(i)

        vars = list(vars)
        vars.sort()
        self.vars = tuple(vars)

    def _make_combination(self):
    # Make all possible combinations of true and false using the given set of
    # variables.

        var_combination = []
        no_of_combination = len(self.vars)
        cartesian_product = product(CONSTANTS, repeat=no_of_combination)

        # Map all those values to their respective variable
        for values in cartesian_product:
            mapping = {}
            for variable, value in zip(self.vars, values):
                mapping[variable] = value
            var_combination.append(mapping)
        self.var_combination = tuple(var_combination)

    def generate(self):
        """Generates the truth table. Returns a list whose first element is a
        the formula and the rest are their corresponding values.
        """
        truth_table = []

        if len(self.var_combination):
            head = []
            truth_table.append(head)
            for mapping in self.var_combination:
                row = []
                for formula, value in evaluate(self._expr, bool_funcs_dict, mapping):
                    if formula not in head:
                        head.append(formula)
                    row.append(value)
                truth_table.append(row)
        else:
            for formula, value in evaluate(self._expr, bool_funcs_dict):
                row.append(value)
                truth_table.append(row)

        return truth_table

    def display_table(self):
        """Display table in the console"""
        truth_table = self.generate()
        head = truth_table[0]
        truth_table[0:1] = []
        length_row = sum(map(len, head)) + len(head) + 1
        for i, j in enumerate(head[:]):
            head[i] = infixRepr(j)
        for j in head:
            print('+', end='')
            print('-' * len(j), end='')
        print('+')
        for j in head:
            print('|', end='')
            print(j, end='')
        print('|')
        for j in head:
            print('+', end='')
            print('-' * len(j), end='')
        print('+')
        for row in truth_table:
            for head_col, col in zip(head, row):
                print('|', end='')
                print(col.rjust(len(head_col)), end='')
            print('|')
        for j in head:
            print('+', end='')
            print('-' * len(j), end='')
        print('+')


if __name__ == '__main__':
    while True:
        try:
            string = input('boolean> ')
        except EOFError:
            break
        else:
            string = string.strip()

        if not string:
            continue

        try:
            table = TruthTable(string)
        except ParseException as ex:
            print(ex)
        else:
            table.display_table()
