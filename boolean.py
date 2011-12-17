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
    return TRUE if x == FALSE else FALSE

@check_if_literal
def and_(x, y):
    return x if x == FALSE else y

@check_if_literal
def or_(x, y):
    return x if x == TRUE else y

@check_if_literal
def xor(x, y):
    return not_(iff(x, y))

@check_if_literal
def if_(x, y):
    return TRUE if x != TRUE or y != FALSE else FALSE

@check_if_literal
def iff(x, y):
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
