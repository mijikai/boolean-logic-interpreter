#!/usr/bin/env python3

from boolean import bool_funcs_dict, CONSTANTS
from itertools import product
from expression import Expression, simulate


class TruthTable:
    """Generates the truth table for the given string.

    Data defined:
        vars: Identifiers in the string
        var_combination: A tuple of dictionary of the possilbe combination of
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
            if (isinstance(i, Expression) and i.is_leaf() and
                    i.arg1 not in CONSTANTS):
                vars.add(i.arg1)
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

        Examples:
            >>> TruthTable(Expression(' ', 'a')).generate()
            [[Expression(oper=' ', arg1='a', arg2=None)], ['T'], ['F']]
            >>> TruthTable(Expression('~', 'a')).generate()
            ...  # doctest: +NORMALIZE_WHITESPACE
            [['a', Expression(oper='~', arg1='a', arg2=None)],
             ['T', 'F'],
             ['F', 'T']]
            >>> TruthTable(Expression('&', 'a', 'b')).generate()
            ...  # doctest: +NORMALIZE_WHITESPACE
            [['a', 'b', Expression(oper='&', arg1='a', arg2='b')],
             ['T', 'T', 'T'],
             ['T', 'F', 'F'],
             ['F', 'T', 'F'],
             ['F', 'F', 'F']]
        """
        truth_table = []

        if len(self.var_combination):
            head = []
            truth_table.append(head)
            for mapping in self.var_combination:
                row = []
                for formula, value in zip(self.__order, simulate(self.__order,
                    mapping, bool_funcs_dict)):
                    if formula not in head:
                        head.append(formula)
                    row.append(value)
                truth_table.append(row)
        else:
            for formula, value in zip(self.__order, simulate(self.__order,
                mapping, bool_funcs_dict)):
                row.append(value)
                truth_table.append(row)

        return truth_table

    def display_table(self):
        """Display table in the console"""
        truth_table = self.generate()
        head = truth_table[0]
        truth_table[0:1] = []
        col_len = []

        for i, j in enumerate(head[:]):
            head[i] = str(j)
            col_len.append(len(head[i]) + 2)

        self._print_row(head, col_len, True)
        for row in truth_table:
            self._print_row(row, col_len)

    def _print_row(self, row, col_len, upper=False):
        """Print the row of the table and border it.

        row - an iterable of fixed length
        col_len - the width of each cell
        upper - determine whether the upper border will be printed.
            Default is False.
        """

        if upper:
            print('+', end='')
            for i in col_len:
                print('-' * i, end='+')
            print()

        print('|', end='')
        for col, length in zip(row, col_len):
            print(str(col).center(length), end='|')

        print()
        print('+', end='')
        for i in col_len:
            print('-' * i, end='+')
        print()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
