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

        Examples:



        Example:
        >>> a = Expression('+', 'a', 'b')
        >>> b = Expression('*', 'a', 'b')
        >>> c = Expression('-', a, b)
        >>> c.replace_expr(a, 3) == Expression('-', 3, b)
        True
    def evaluation_order(self):
        """Returns a list of the evaluation order of the Expression object.
        When oper is a space, the list will be composed of the value of arg1
        otherwise, the list will be composed of the evaluation order of arg1,
        evaluation order of arg2 and the object itself in order.
        
        Examples:
        >>> Expression(' ', 'a').evaluation_order()
        [Expression(oper=' ', arg1='a', arg2=None)]
        >>> a = Expression('+', 3, 2)

        >>> a.evaluation_order()
        [3, 2, Expression(oper='+', arg1=3, arg2=2)]
        >>> b = Expression('*', 4, 5)

        >>> b.evaluation_order()
        [4, 5, Expression(oper='*', arg1=4, arg2=5)]
        >>> c = Expression('/', a, 'a')

        >>> c.evaluation_order()
        [3, 2, Expression(oper='+', arg1=3, arg2=2), 'a', Expression(oper='/', arg1=Expression(oper='+', arg1=3, arg2=2), arg2='a')]
        """

        args = [self.arg1, self.arg2]

        if self.arg2 == None or self.is_leaf():
            args.pop()

        order = []
        for i, arg in enumerate(args):
            if isinstance(arg, self.__class__):
                order.extend(arg.evaluation_order())
            elif not self.is_leaf():
                order.append(arg)
        order.append(self)

        return order

def simulate(order, mappings={}, funcs={}):
    """Make some simplification and substitution to the list of expression.
    oper, arg1 and arg2 refers to the attribute of the Expression object.

    order - if an Expression object, get first the evaluation order. The
        order controls the simplification and substitution.
    mappings - a dictionary in which an element from order or arg1 or arg2 of
        the object will be replaced by the value of the key equal to that
        element. 
    funcs - a dictionary in which the oper will be match against the key of the
        dictionary. The value must be a callable object. 

    If an element in ``order`` is not an ``Expression``, the value
    corresponding to the element will substitute that element. If an element is
    an ``Expression`` but its ``oper`` is a space. match the ``arg1`` in the
    keys of ``mappings`` and substitute the element with the matching value.
    After those substitution, find the corresponding ``oper`` in ``funcs`` and
    use that value to simplify the expression.

    No error is thrown if ``oper``, ``arg1`` or ``arg2`` does not match
    ``mappings`` or ``funcs``

    Returns a list equal to the length of ``order`` composed of evaluated
    values correspond to the aformentioned list.
        
    Examples:
        >>> mappings = {'a': 3, 'b': 8, 'c': 4}
        >>> funcs = {'+': lambda x, y: x + y, '*': lambda x, y: x * y}
        >>> a = Expression(' ', 'a') # a
        >>> simulate(a, mappings, funcs)
        [3]
        >>> b = Expression('+', 5, a) # 5 + a
        >>> simulate(b, mappings, funcs)
        [5, 3, 8]
        >>> c = Expression('*', a, 'c') # a * c
        >>> simulate(c, mappings, funcs)
        [3, 4, 12]
        >>> d = Expression('+', b, c) # (5 + a) + (a * c)
        >>> simulate(d, mappings, funcs)
        [5, 3, 8, 3, 4, 12, 20]
        >>> e = Expression('*', 'b', d) # b * ((5 + a) + (a * c))
        >>> simulate(e, mappings, funcs)
        [8, 5, 3, 8, 3, 4, 12, 20, 160]
    """

    if isinstance(order, Expression):
        order = order.evaluation_order()

    new_order = []
    subs_expr = {}
    for stmt in order:
        var = stmt
        if isinstance(stmt, Expression):
            if stmt.oper == ' ':
                var = stmt.arg1
            else:
                del var

        if 'var' in dir():
            try:
                sub = mappings[var]
            except KeyError:
                sub = var
            subs_expr[stmt] = sub
            new_order.append(sub)
            continue

        if stmt in subs_expr:
            new_order.append(subs_expr[stmt])
            continue

        args = [stmt.arg1, stmt.arg2]
        if stmt.oper == ' ' or stmt.arg2 == None:
            args.pop()

        for i, arg in enumerate(args[:]):
            try:
                args[i] = mappings[arg]
            except KeyError:
                try:
                    args[i] = subs_expr[arg]
                except KeyError:
                    pass

        try:
            ans = funcs[stmt.oper](*args)
        except KeyError:
            ans = stmt
        subs_expr[stmt] = ans
        new_order.append(ans)
    return new_order

if __name__ == '__main__':
    import doctest
    doctest.testmod()
