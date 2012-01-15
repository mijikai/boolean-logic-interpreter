# !/usr/bin/env python3

from bool_parser import parse
from boolean import bool_funcs_dict, CONSTANTS
from itertools import product
from expression import evaluate, evaluate2, Expression


class TruthTable:
    """Generates the truth table for the given string.

    Data defined:
    -> vars: Identifiers in the string
    -> var_combination: A tuple of dictionary of the possilbe combination of
        the truth value
    """

    def __init__(self, string):
        self._string = string
        self._expr = parse(string)
        self._find_variables()
        self._make_combination()

    def _find_variables(self):
        # Find all the identifier in the expression. Used in order to determine
        # the possible combination of truth table and assign those some value

        vars = set()
        stack = []
        if type(self._expr) == str:
            vars.add(self._expr)
        else:
            stack.append(self._expr)

        while stack:
            current = stack.pop()
            for i in (current.arg1, current.arg2):
                if type(i) == type(current):
                    stack.append(i)
                elif i in CONSTANTS or i is None:
                    pass
                elif type(i) == str:
                    vars.add(i)
                else:
                    raise Exception("'" + type(i).__name__ +
                            "' is not a str or Expression")

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
        """Generates the truth table. Returns a tuple of this format:
        (eval1, eval2, ...).

        evaln is a tuple of two elements composed of the variable and
        expression."""
        truth_table = []

        if len(self.var_combination):
            for mapping in self.var_combination:
                row = []
                row.extend(evaluate(self._expr, bool_funcs_dict, mapping))
                truth_table.append(row)
        else:
            row = evaluate(self._expr, bool_funcs_dict)
            truth_table.append(row)

        return tuple(truth_table)


if __name__ == '__main__':
    while True:
        try:
            string = input('>>> ')
        except EOFError:
            break
        else:
            string = string.strip()

        if not string:
            continue

        table = TruthTable(string)
        for row in table.generate():
            for column in row:
                print(*column)
