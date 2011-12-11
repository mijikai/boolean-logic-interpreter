#!/usr/bin/env python3

import collections

class Expression(collections.namedtuple('Expression', ['oper', 'arg1', 'arg2'])):
    """Returns a tuple (oper, arg1, arg2)

    oper, arg1 and arg2 can be of any immutable type. oper and arg1 must not
    have a value of None."""

    def __new__(cls, oper, arg1, arg2=None):
        return super().__new__(cls, oper, arg1, arg2)

    def getsubexpr(self):
        """Returns a tuple composed of Expression objects. If the object has a
        depth h, the first elements of the tuple are the nodes of the root at
        level h, the next elements are the nodes at depth h - 1, and so on. The
        order is arg1 first before arg2

        Example:
        >>> a = Expression('+', 2, 3)
        >>> b = Expression('+', 4, 5)
        >>> c = Expression('-', a, b)
        >>> d = Expression('-', b, a)
        >>> e = Expression('*', c, d)
        >>> e.getsubexpr() == (a, b, b, a, c, d)
        True
        """

        stack = []
        current_frame = self
        subexpr = []
        type_expr = type(self)

        while current_frame:
            type_arg1 = type(current_frame.arg1)
            type_arg2 = type(current_frame.arg2)
            parents = []

            if type_arg2 == type_expr:
                subexpr.append(current_frame.arg2)
                parents.append(current_frame.arg2)

            if type_arg1 == type_expr:
                subexpr.append(current_frame.arg1)
                parents.append(current_frame.arg1)

            if parents:
                parents.reverse()
                stack.extend(parents)

            if stack:
                current_frame = stack.pop()
            else:
                current_frame = None

        subexpr.reverse()
        subexpr.append(self)
        return tuple(subexpr)

    def replaceexpr(self, expr, value, replaceall=False):
        subexpr_tuple = self.getsubexpr()
        stored_value = {}

        for curr in subexpr_tuple:
            if curr == expr and (replaceall or not curr in stored_value):
                stored_value[curr] = value
                continue

            args = [curr.oper]
            for arg in (curr.arg1, curr.arg2):
                if replaceall or not curr in stored_value:
                    if arg == expr:
                        args.append(value)
                    elif arg in stored_value:
                        args.append(stored_value[arg])
                else:
                    args.append(arg)

            stored_value[curr] = Expression(*args)

        return stored_value[self]


    def __str__(self):
        string = '(' + str(self.oper) + ' ' + str(self.arg1)
        if self.arg2 != None:
            string += ' ' + str(self.arg2)
        string += ')'
        return string
    __repr__ = __str__


def evaluate(expr, funcs, mapping={}):
    """Returns a list of tuples composed of Expression object and result.

    expr -> Expression object
    funcs -> a dictionary whose keys are possible objects in expr.oper and
        values are functions
    mapping -> a dictionary whose keys are possible objects contained in
    expr.arg1 or expr.arg2, and values which will be substitute when a key
        correspond to either expr.arg1 or expr.arg2."""

    expr_list = expr.getsubexpr()
    memo = {}
    results = []

    for curr_frame in expr_list:
        if curr_frame in memo:
            continue

        arg1 = curr_frame.arg1
        arg2 = curr_frame.arg2

        if arg1 in memo:
            arg1 = memo[arg1]
        elif arg1 in mapping:
            arg1 = mapping[arg1]

        if arg2 in memo:
            arg2 = memo[arg2]
        elif arg2 in mapping:
            arg2 = mapping[arg2]
        if arg2 == None:
            args = (arg1,)
        else:
            args = (arg1, arg2)

        memo[curr_frame] = funcs[curr_frame.oper](*args)
        results.append((curr_frame, memo[curr_frame]))

    return results

