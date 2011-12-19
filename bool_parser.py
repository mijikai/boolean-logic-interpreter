#!/usr/bin/env python3

from pyparsing import Word, Literal, Forward, OneOrMore, ZeroOrMore,\
    Or, MatchFirst, Group, StringEnd
from boolean import NOOP, UNARY, BINARY, OPERATORS, PRECEDENCE, CONSTANTS
from expression import Expression

__all__ = ['parse']

#This function will be called by the pattern when an expression is
#parsed. We only need the first element of tok and push them in the
#stack. If the function will just only append the first element of tok
#to the stack, the stack will appear to be in infix order.
stack = []
def toExpression(s, loc, tok):
    curr = tok[0]
    if curr in BINARY:
        args = []
        for i in range(2):
            args.append(stack.pop())
        args.reverse()
        stack.append(Expression(curr, *args))
    elif curr in UNARY:
        stack.append(Expression(curr, stack.pop()))
    elif curr != "(":
        stack.append(Expression(NOOP, curr))

#for variables
alpha = 'abcdefghijklmnopqrstuvwxyz'
alpha += alpha.upper()

alpha_list = list(alpha)
for i in CONSTANTS:
    alpha_list.remove(i)
alpha = ''.join(alpha_list)

#nesting
lpar = Literal('(')
rpar = Literal(')')

var = Word(alpha)
constant = MatchFirst([Literal(i) for i in CONSTANTS])
operand = constant | var

oper_literals = {oper:Literal(oper) for oper in OPERATORS}
oper_patterns = {oper:Forward() for oper in OPERATORS}

expr = Forward()
atom = operand | lpar + expr + rpar.setParseAction()

prev_pattern = atom

atom.setParseAction(toExpression) 

for opers in PRECEDENCE:
    pattern_list = []
    #only accepts unary and binary operation as there are not ternary in boolean
    for op in opers:
        if op in UNARY:
            alternative = OneOrMore(oper_literals[op]) + prev_pattern
            alternative.setParseAction(toExpression) 
            unary_pattern = prev_pattern | alternative
            pattern_list.append(unary_pattern)
        elif op in BINARY:
            rest = oper_literals[op] + prev_pattern
            rest.setParseAction(toExpression)
            binary_pattern = prev_pattern + ZeroOrMore(rest)
            pattern_list.append(binary_pattern)
        else:
            raise Exception(op)

    if len(pattern_list) == 1: 
        prev_pattern = pattern_list[0]
    else:
        prev_pattern = Or(pattern_list)

expr << prev_pattern
pattern = expr + StringEnd()

def parse(string):
    """Parses the string into an Expression object."""
    global stack
    stack = []
    pattern.parseString(string) 
    return stack.pop() #after parsing the stack should have only one item
