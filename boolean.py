#!/usr/bin/env python3

TRUE = 'T'
FALSE = 'F'
NOT = '~'
AND = '&'
OR = '|'
XOR = '^'
IF = '=>'
IFF = '<=>'
LITERALS = (TRUE, FALSE)
UNARY = (NOT)
BINARY = (AND, OR, XOR, IF, IFF)

def check_if_literal(func):
    def checker(*args, **kwargs):
        for arg in args:
            if arg not in LITERALS:
                raise Exception
        return func(*args, **kwargs)

    checker.__name__ = func.__name__
    checker.__doc__ = func.__doc__

    return checker

@check_if_literal
def not_(x):
    """Returns the value of TRUE if x is FALSE else FALSE

    >>> not_(TRUE)
    'F'
    >>> not_(FALSE)
    'T'
    """
    return TRUE if x == FALSE else FALSE

@check_if_literal
def and_(x, y):
    """Returns the value of TRUE if both x and y are TRUE else FALSE

    >>> and_(TRUE, TRUE)
    'T'
    >>> and_(TRUE, FALSE)
    'F'
    >>> and_(FALSE, TRUE)
    'F'
    >>> and_(FALSE, FALSE)
    'F'
    """
    return x if x == FALSE else y

@check_if_literal
def or_(x, y):
    """Returns the value of FALSE if neither x nor y are TRUE

    >>> or_(TRUE, TRUE)
    'T'
    >>> or_(TRUE, FALSE)
    'T'
    >>> or_(FALSE, TRUE)
    'T'
    >>> or_(FALSE, FALSE)
    'F'
    """
    return x if x == TRUE else y

@check_if_literal
def xor(x, y):
    """Like or_ but returns FALSE if both are TRUE. Opposite of iff.

    >>> xor(TRUE, TRUE)
    'F'
    >>> xor(TRUE, FALSE)
    'T'
    >>> xor(FALSE, TRUE)
    'T'
    >>> xor(FALSE, FALSE)
    'F'
    """
    return not_(iff(x, y))

@check_if_literal
def if_(x, y):
    """Returns the value of FALSE if x == TRUE and y == FALSE else TRUE

    >>> if_(TRUE, TRUE)
    'T'
    >>> if_(TRUE, FALSE)
    'F'
    >>> if_(FALSE, TRUE)
    'T'
    >>> if_(FALSE, FALSE)
    'T'
    """
    return TRUE if x != TRUE or y != FALSE else FALSE

@check_if_literal
def iff(x, y):
    """Returns the VALUE of TRUE if the condition and its converse are
    TRUE. Opposite of xor.

    >>> iff(TRUE, TRUE)
    'T'
    >>> iff(TRUE, FALSE)
    'F'
    >>> iff(FALSE, TRUE)
    'F'
    >>> iff(FALSE, FALSE)
    'T'
    """
    res_and = and_(x, y)
    return res_and if res_and == TRUE else not_(or_(x, y))

bool_funcs_dict = {NOT: not_,
        AND: and_,
        OR: or_,
        XOR: xor,
        IF: if_,
        IFF: iff}

if __name__ == '__main__':
    if TRUE == FALSE:
        raise ValueError('TRUE value equals FALSE.')

    import doctest
    doctest.testmod()

    truth_combination = ((TRUE, TRUE),
            (TRUE, FALSE),
            (FALSE, TRUE),
            (FALSE, FALSE))

    truth_result_not = (FALSE, TRUE)
    truth_result = {
            AND: (TRUE, FALSE, FALSE, FALSE),
            OR: (TRUE, TRUE, TRUE, FALSE),
            XOR: (FALSE, TRUE, TRUE, FALSE),
            IF: (TRUE, FALSE, TRUE, TRUE),
            IFF: (TRUE, FALSE, FALSE, TRUE)}

    for arg, expected_result in zip((TRUE, FALSE), (FALSE, TRUE)):
        value = not_(arg)
        if value == expected_result:
            print('Passed: ', end='')
        else:
            print('Failed: ', end='')
        print(not_.__name__, arg, '=>', value, ':', expected_result)

    for oper in truth_result:
        results = truth_result[oper]
        bool_func = bool_funcs_dict[oper]

        for args, expected_result in zip(truth_combination, results):
            value = bool_func(*args)
            if expected_result == value:
                print('Passed: ', end='')
            else:
                print('Failed: ', end='')
            print(bool_func.__name__, args, '=>', value, ':',
                    expected_result)
