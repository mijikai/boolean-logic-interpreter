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

def args_literal_check(func):
    def checker(*args, **kwargs):
        for arg in args:
            if arg not in LITERALS:
                raise ValueError('invalid argument given for ' + checker.__name__ + ': ' + str(arg))
        return func(*args, **kwargs)

    checker.__name__ = func.__name__
    checker.__doc__ = func.__doc__

    return checker

def return_literal_check(func):
    def checker(*args, **kwargs):
        return_value = func(*args, **kwargs)
        if return_value not in LITERALS:
            raise Exception('invalid return value for ' + checker.__name__ + ': ' + str(return_value))
        return return_value

    checker.__name__ = func.__name__
    checker.__doc__ = func.__doc__

    return checker

@args_literal_check
@return_literal_check
def not_(x):
    """Returns the value of TRUE if x is FALSE else FALSE

    >>> not_(TRUE)
    'F'
    >>> not_(FALSE)
    'T'
    """
    return TRUE if x == FALSE else FALSE

@args_literal_check
@return_literal_check
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

@args_literal_check
@return_literal_check
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

@args_literal_check
@return_literal_check
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

@args_literal_check
@return_literal_check
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

@args_literal_check
@return_literal_check
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
