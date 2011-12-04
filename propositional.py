#!/usr/bin/env python3

UNARY = 'NOT',
BINARY = 'AND', 'OR', 'XOR', 'IMPLIES', 'IFF'
OPER = UNARY + BINARY
LITERAL = frozenset({ 'T', 'F' })
PRECEDENCE = {i:j for i, j in zip(OPER, range(len(OPER)))}

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


