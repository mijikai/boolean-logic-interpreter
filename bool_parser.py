#!/usr/bin/env python3

import pyparsing
import boolean

alpha = 'abcdefghijklmnopqrstuvwxyz'
alpha += alpha.upper()

#remove literal true and false
alpha_list = list(alpha)
for i in boolean.LITERALS:
    alpha_list.remove(i)
alpha = ''.join(alpha_list)

lpar = pyparsing.Literal('(')
rpar = pyparsing.Literal(')')

#operator literals
not_ = pyparsing.Literal(boolean.NOT)
and_ = pyparsing.Literal(boolean.AND)
or_ = pyparsing.Literal(boolean.OR)
xor = pyparsing.Literal(boolean.XOR)
if_ = pyparsing.Literal(boolean.IF)
iff = pyparsing.Literal(boolean.IFF)

expr = pyparsing.Forward()
negation = pyparsing.Forward()

var = pyparsing.Word(alpha)
constant = (pyparsing.Literal(boolean.TRUE) |
        pyparsing.Literal(boolean.FALSE))
operand = constant | var

atom = operand | lpar + expr + rpar
negation << (not_ + atom | not_ + negation)
conjunction = (atom | negation) + pyparsing.ZeroOrMore(and_ + (atom | negation))
disjunction = conjunction + pyparsing.ZeroOrMore(or_ + conjunction)
ex_disjunction = disjunction + pyparsing.ZeroOrMore(xor + disjunction)
conditional = ex_disjunction + pyparsing.ZeroOrMore(if_ + ex_disjunction)
expr << conditional + pyparsing.ZeroOrMore(iff + conditional)

pattern = expr + pyparsing.StringEnd()
