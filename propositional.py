#!/usr/bin/env python3

import itertools

UNARY = 'NOT',
BINARY = 'AND', 'OR', 'XOR', 'IMPLIES', 'IFF'
OPER = UNARY + BINARY
LITERAL = frozenset({ 'T', 'F' })
PRECEDENCE = {i:j for i, j in zip(OPER, range(len(OPER)))}

class Tokenizer(object):
    def __init__(self, string, keywords=frozenset({}), operators=frozenset({})):
        self.ind = 0
        self.keywords = keywords
        self.operators = operators
        self.string = string
        self.WHITESPACE = " \n\r\t\b"

    def __iter__(self):
        return self

    def __next__(self):
        if self.ind >= len(self.string):
            raise StopIteration

        for char in itertools.islice(self.string, self.ind, None):
            if char in self.WHITESPACE:
                self.ind += 1
            else:
                break

        tok_funcs = [self.__opertok, self.__keywordtok, self.__ordinarytok]

        for func in tok_funcs:
            tok = func(self.ind)
            if tok:
                self.ind += len(tok)
                return tok


    def __opertok(self, ind):
        operators = list(self.operators)
        tok = []

        for char, oper_ind in zip(itertools.islice(self.string, ind, None), itertools.count()):
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

    def __keywordtok(self, ind):
        keywords = list(self.keywords)
        tok = []

        for char, key_ind in zip(itertools.islice(self.string, ind, None), itertools.count()):
            if char in self.WHITESPACE:
                break
            elif not keywords:
                return False

            matched = False
            for key, ind in zip(keywords[:], range(len(keywords))):
                if key_ind < len(key) and char == key[key_ind]:
                    if not matched:
                        tok.append(key[key_ind])
                        matched = True
                else:
                    keywords.remove(key)

        if not tok: return False
        return ''.join(tok)

    def __ordinarytok(self, ind):
        tok = []
        for char, tok_ind in zip(itertools.islice(self.string, ind, None), itertools.count(ind)):
            if char in self.WHITESPACE or self.__opertok(tok_ind):
                return ''.join(tok)
            tok.append(char)

        if not tok: return False
        return ''.join(tok)


def tokenize(string):
    tokens = []
    stack = []
    ind = 0
    length = len(string)

    def consume(oper):
        nonlocal ind
        i = 0
        
        for charstr, charoper in zip(string[ind:ind + len(oper)].upper(), oper):
            if charstr != charoper:
                raise SyntaxError
            i += 1
        if i != len(oper):
            raise SyntaxError

        tokens.append(oper)
        ind += len(oper) - 1
    
    while ind < length:
        char = string[ind].upper()

        if char in "TF":
            tokens.append(char)
        elif char == 'N':
            consume('NOT')
        elif char == 'A':
            consume('AND')
        elif char == 'O':
            consume('OR')
        elif char == 'I':
            try:
                consume('IFF')
            except SyntaxError:
                consume('IMPLIES')
        elif char == 'X':
            consume('XOR')
        elif char == '(':
            child = []
            tokens.append(child)
            stack.append(tokens)
            tokens = child
        elif char == ')':
            if not stack:
                raise SyntaxError
            tokens = stack.pop()
        elif char in " \t\n\r":
            pass
        else:
            raise SyntaxError

        ind += 1

    if stack:
        raise SyntaxError
    return tokens


def parse(string):
    tokens = tokenize(string)
    stk_oper = []
    stk_post = []
    stk_tok = []

    while tokens:
        tok = tokens.pop(0)
        if tok in LITERAL:
            if stk_oper:
                oper = stk_oper.pop()
                if oper in BINARY and not stk_post:
                    raise SyntaxError

                stk_oper.append(oper) 
                stk_post.append(tok)

                while stk_oper:
                    oper = stk_oper.pop()
                    stk_post.append(oper)

            else:
                stk_post.append(tok)
        elif tok in UNARY:
            stk_oper.append(tok)
        elif tok in BINARY:
            if not stk_post:
                raise SyntaxError

            elem = stk_post.pop()
            while stk_post and elem in OPER and PRECEDENCE[tok] < PRECEDENCE[elem]:
                stk_oper.append(elem)
                elem = stk_post.pop()

            if elem in LITERAL:
                stk_post.append(elem)
            elif elem in OPER:
                if PRECEDENCE[tok] < PRECEDENCE[elem]:
                    stk_oper.append(elem)
                else:
                    stk_post.append(elem)

            stk_oper.append(tok)

    if stk_oper:
        raise SyntaxError
    return stk_post


