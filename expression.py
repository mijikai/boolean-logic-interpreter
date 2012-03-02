#!/usr/bin/env python3

import collections as _collections

__all__ = ['Expression', 'evaluate', 'evaluate2']


class Expression(_collections.namedtuple('Expression',
    ['oper', 'arg1', 'arg2'])):
    """Returns a tuple (oper, arg1, arg2)

    oper, arg1 and arg2 can be of any immutable type. oper and arg1 must not
    have a value of None."""

    def __new__(cls, oper, arg1, arg2=None):
        return super().__new__(cls, oper, arg1, arg2)

    def sexpr(self):
        r"""Returns an s expr representation of the object. If oper is composed
        of whitespace only, return the str of arg1.

        Examples:
        >>> print(Expression(' ', 3).sexpr())
        3
        >>> print(Expression('-', 3).sexpr())
        (- 3)
        >>> print(Expression('*', 8, 4).sexpr())
        (* 8 4)
        >>> print(Expression('+', Expression('-', 6), 3).sexpr())
        (+ (- 6) 3)
        """

        values = [self.oper, self.arg1, self.arg2]
        if self.is_leaf():
            template = '{}'
            values = [self.arg1]
        elif self.arg2 == None:
            template = '({} {})'
            values.pop()
        else:
            template = '({} {} {})'
        for i, j in enumerate(values[:]):
            if isinstance(j, self.__class__):
                values[i] = j.sexpr() 
        return template.format(*values)

    def getsubexpr(self):
        r"""Returns a tuple composed of Expression objects. If the object has a
        depth h, the first elements of the tuple are the nodes of the root at
        level h, the next elements are the nodes at depth h - 1, and so on. The
        order is arg1 first before arg2

        Examples:
        >>> a = Expression('+', 2, 3)
        >>> print(*a.getsubexpr(), sep='\n')
        (+ 2 3)
        >>> b = Expression('+', a, 4)
        >>> print(*b.getsubexpr(), sep='\n')
        (+ 2 3)
        (+ (+ 2 3) 4)
        >>> c = Expression('-', 5, a)
        >>> print(*c.getsubexpr(), sep='\n')
        (+ 2 3)
        (- 5 (+ 2 3))
        >>> d = Expression('*', b, c)
        >>> print(*d.getsubexpr(), sep='\n')
        (+ 2 3)
        (+ 2 3)
        (+ (+ 2 3) 4)
        (- 5 (+ 2 3))
        (* (+ (+ 2 3) 4) (- 5 (+ 2 3)))
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

    def replace_expr(self, expr, value, replaceall=False):
        """Replaces one of the subexpression with value.

        If replaceall is set to True, it will replace all instances of
        subexpression expr with value.
        If expr is not found, returns self.

        Example:
        >>> a = Expression('+', 'a', 'b')
        >>> b = Expression('*', 'a', 'b')
        >>> c = Expression('-', a, b)
        >>> c.replace_expr(a, 3) == Expression('-', 3, b)
        True
        """

        subexpr_tuple = self.getsubexpr()
        stored_value = {}
        has_matched = False

        for curr in subexpr_tuple:
            if curr == expr:
                stored_value[curr] = value
                continue

            args = [curr.oper]
            found = False

            for arg in (curr.arg1, curr.arg2):
                if arg == expr:
                    if not has_matched or replaceall:
                        found = True
                        args.append(value)
                    has_matched = True
                elif arg in stored_value:
                    found = True
                    args.append(stored_value[arg])
                    if not replaceall:
                        del stored_value[arg]
                else:
                    args.append(arg)

            if found:
                stored_value[curr] = Expression(*args)

        if self in stored_value:
            return stored_value[self]
        return self


def evaluate(expr, funcs, mapping={}):
    """Returns a list of tuples composed of Expression object and result.

    expr -> Expression object
    funcs -> a dictionary whose keys are possible objects in expr.oper and
        values are functions
    mapping -> a dictionary whose keys are possible objects contained in
    expr.arg1 or expr.arg2, and values which will be substitute when a key
        corresponds to either expr.arg1 or expr.arg2."""

    expr_list = expr.getsubexpr()
    memo = {}
    results = []

    for curr_frame in expr_list:
        if curr_frame in memo:
            continue

        args = [curr_frame.arg1]

        if curr_frame.arg2 != None:
            args.append(curr_frame.arg2)

        for ind, arg in zip(range(len(args)), args):
            if arg in memo:
                args[ind] = memo[arg]
            elif arg in mapping:
                args[ind] = mapping[arg]

        memo[curr_frame] = funcs[curr_frame.oper](*args)
        results.append((curr_frame, memo[curr_frame]))

    return results


def evaluate2(expr, funcs, mapping={}):
    """Returns a list of Expression objects. The list is a sequence that shows
    the evaluation of the Expression into a simple form.

    Example:
    >>> funcs = {'+': lambda x, y: x + y,
    ...     '-': lambda x, y: x - y,
    ...     '*': lambda x, y: x * y}
    >>> a = Expression('+', 3, 2)
    >>> b = Expression('-', 7, 4)
    >>> c = Expression('*', a, b)
    >>> for i in evaluate2(c, funcs): print(i)
    (* (+ 3 2) (- 7 4))
    (* 5 (- 7 4))
    (* 5 3)
    15
    """

    memo = {}
    results = []
    type_expr = type(expr)
    orig_expr = expr

    results.append(expr)

    for var in mapping:
        expr = expr.replace_expr(var, mapping[var], True)

    if orig_expr != expr:
        results.append(expr)

    for curr_frame in expr.getsubexpr():
        # Don't recalculate the result
        if curr_frame in memo:
            expr = expr.replace_expr(curr_frame, memo[curr_frame])
            results.append(expr)
            continue

        args = [curr_frame.arg1, curr_frame.arg2]

        args_equiv = []
        # If the argument has a result in the memo,
        # the result replaces that argument.
        for arg in args[:]:
            if arg in memo:
                args_equiv.append(memo[arg])
            else:
                args_equiv.append(arg)

        answer = funcs[curr_frame.oper](*args_equiv)
        memo[curr_frame] = answer

        eqv = Expression(curr_frame.oper, *args_equiv)
        if curr_frame == eqv:
            expr = expr.replace_expr(curr_frame, answer)
        else:
            expr = expr.replace_expr(eqv, answer)

        results.append(expr)

    return results


def infixRepr(expr):
    """'Convert the expr into a string in infix form."""
    if expr.oper == ' ':
        return str(expr.arg1)
    if expr.arg2 == None:
        return '{}{}'.format(expr.oper, infixRepr(expr.arg1))
    return '({} {} {})'.format(infixRepr(expr.arg1), expr.oper, infixRepr(expr.arg2))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
