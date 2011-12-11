#!/usr/bin/env python3

import itertools
import inspect

class Tokenizer(object):
    """Creates an iterable object that returns a token."""
    
    def __init__(self, iterable, operators=frozenset({})):
        if type(operators) != frozenset:
            raise TypeError('operators must be of type frozenset')

        self.ind = 0
        self.operators = operators
        self.iterable = iterable
        self.WHITESPACE = " \n\r\t\b"

    def __iter__(self):
        return self

    def __next__(self):
        """Returns the next token.

        The token is a string from the current index up to (but not
        including) a whitespace. If the string matches one of the item
        in the operator set, token will be the longest possible match
        and ignore the consideration whether the next character is a
        whitespace or not."""

        if self.ind >= len(self.iterable):
            raise StopIteration

        for char in itertools.islice(self.iterable, self.ind, None):
            if char in self.WHITESPACE:
                self.ind += 1
            else:
                break

        tok_funcs = [self.__opertok, self.__ordinarytok]

        for func in tok_funcs:
            tok = func(self.ind)
            if tok:
                self.ind += len(tok)
                return tok

    def __opertok(self, ind):
        """Returns the longest match from the operator set or False if
        no match is found."""
        
        operators = list(self.operators)
        tok = []

        #Loop over the string from ind and match the operators list in parallel.
        for char, oper_ind in zip(itertools.islice(self.iterable, ind, None), itertools.count()):
            if not operators or char in self.WHITESPACE:
                break

            matched = False
            for oper, opers_ind in zip(operators[:], range(len(operators))):
                if oper_ind < len(oper) and char == oper[oper_ind]:
                    if not matched:
                        tok.append(oper[oper_ind])
                        matched = True
                else:
                    operators.remove(oper)

        if not tok: return False
        return ''.join(tok)

    def __ordinarytok(self, ind):
        """Returns a substring starting from ind up to a whitespace or a
        beginning of one of the item in the operator set, otherwise
        False if the string is composed of whitespaces."""

        tok = []
        for char, tok_ind in zip(itertools.islice(self.iterable, ind, None), itertools.count(ind)):
            if char in self.WHITESPACE or self.__opertok(tok_ind):
                return ''.join(tok)
            tok.append(char)

        if not tok: return False
        return ''.join(tok)

    def peek(self):
        """Returns the next token but not update the index"""
        tok = self.__next__()
        self.ind -= len(tok)
        return tok


class Evaluator(object):
   def __init__(self, postExpr, funcs, vars={}):
       self.postExpr = list(postExpr)
       self.funcs = dict(funcs)
       self.vars = dict(vars)

   def __iter__(self):
       stk_opern = []
       stk_oper = []

       for i in self.postExpr[:]:
           if i in self.funcs:
               func = self.funcs[i]
               arg = []
               arglen = len(inspect.getfullargspec(func)[0])

               for j in range(arglen):
                   arg.append(stk_opern.pop())

               arg.reverse()
               value = func(*arg)
               stk_opern.append(value)

               yield value
           elif i in self.vars:
               value = self.vars[i]
               stk_opern.append(value)
               yield value
           else:
               stk_opern.append(i)

       if len(stk_opern) != 1:
           raise Exception
       raise StopIteration


def parse(iterable, operation, preced):
    """Parses the iterable object into a list whose elements are arrange in
    postfix form.

    iterable -> a iterable object that returns a single character string.
    operation -> a dictionary type composed of keys unary, binary, and
        parenthesis. The unary and binary keys has a value of tuple
        composed of strings and the parenthesis key has a value of dictionary
        whose key is the open parenthesis and value is a close parenthesis.  
    preced -> a dictionary type whose keys are the valid operations and value
        corresponding to their precedence."""
    
    stk_oper = []
    stk_post = []
    stk_tok = []
    unary = operation['unary']
    binary = operation['binary']
    operators = unary + binary
    parenthesis = operation['parenthesis']
    tok_iter = Tokenizer(iterable, frozenset(operators +
        tuple(parenthesis.keys()) + tuple(parenthesis.values())))

    for tok in tok_iter:
        if tok in parenthesis:
            stk_oper.append(tok)
        elif tok in list(parenthesis.values()):
            close_paren = stk_oper.pop()
            if parenthesis[close_paren] != tok:
                raise SyntaxError

            while stk_oper:
                oper = stk_oper.pop()
                if not oper in operators:
                    break
                stk_post.append(oper)
        elif tok in unary:
            stk_oper.append(tok)
        elif tok in binary:
            if not stk_post:
                raise SyntaxError
            elem = stk_post.pop()

            while stk_post and elem in operators and preced[tok] < preced[elem]:
                stk_oper.append(elem)
                elem = stk_post.pop()

            if elem in operators:
                if preced[tok] < preced[elem]:
                    stk_oper.append(elem)
                else:
                    stk_post.append(elem)
            elif elem in parenthesis:
                pass
            else:
                stk_post.append(elem)
                stk_oper.append(tok)
        else:
            if stk_oper:
                oper = stk_oper.pop()
                if oper in binary and not stk_post:
                    raise SyntaxError

                stk_post.append(tok)

                while stk_oper and oper in operators:
                    stk_post.append(oper)
                    oper = stk_oper.pop()

                if oper in parenthesis:
                    stk_oper.append(oper)
                else:
                    stk_post.append(oper)
            else:
                stk_post.append(tok)

    if stk_oper:
        raise SyntaxError
    return stk_post


