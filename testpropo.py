#!/usr/bin/env python3

import propositional

def testTokenize(): 
    def testvalue(string, output):
        try:
            token = propositional.tokenize(string)
            if token == output:
                print('Passed:', repr(string))
            else:
                print('Failed:', repr(string), repr(token))
        except Exception as ex:
            print('Failed:', repr(string), ex)

    def testfail(string, error):
        try:
            propositional.tokenize(string)
        except error:
            print('Passed:', repr(string))
        except Exception as ex:
            print('Failed:', repr(string), ex)
        else:
            print('Failed:', repr(string), 'No error')

    testvalue('T', ['T'])
    testvalue('F', ['F'])
    testvalue(' T \r\nF', ['T', 'F'])
    testvalue('T and F', ['T', 'AND', 'F'])
    testvalue('T oR F', ['T', 'OR', 'F'])
    testvalue('F IMplIES F', ['F', 'IMPLIES', 'F'])
    testvalue('F xOR T', ['F', 'XOR', 'T'])
    testvalue('T IFF T', ['T', 'IFF', 'T'])
    testvalue('NOT T', ['NOT', 'T'])
    testvalue('(T)', [['T']])
    testfail('a', SyntaxError)
    testfail('(T', SyntaxError)
    testfail(')', SyntaxError)
    testfail('T AND ( T Or F))', SyntaxError)

def testParse():
    def testvalue(string, value):
        try:
            parsed = propositional.parse(string)
            if parsed == value:
                print('Passed:', repr(string))
            else:
                print('Failed:', repr(string), repr(parsed), '!=', repr(value))
        except Exception as ex:
            print('Failed:', repr(string), ex)

    def testfail(string, error):
        try:
            parsed = propositional.parse(string)
        except error:
            print('Passed:', repr(string), repr(error))
        except Exception as ex:
            print('Failed:', repr(string), ex)
        else:
            print('Failed:', repr(string), repr(error))

    testvalue('T', ['T'])
    testvalue('T and F', ['T', 'F', 'AND'])
    testvalue('T and not F', ['T', 'F', 'NOT', 'AND'])
    testvalue('T and F and T', ['T', 'F', 'AND', 'T', 'AND' ])
    testvalue('T and T or T', ['T', 'T', 'AND', 'T', 'OR'])
    testvalue('T or F and T', ['T', 'F', 'T', 'AND', 'OR'])
    testvalue('t and not f or not f and t', ['T', 'F', 'NOT', 'AND', 'F', 'NOT', 'T', 'AND', 'OR'])
    testvalue('not not not not t', ['T', 'NOT', 'NOT', 'NOT', 'NOT'])
    testfail('and t', SyntaxError)
    testfail('t and f or', SyntaxError)
    testfail('not', SyntaxError)

if __name__ == '__main__':
    testTokenize()
    testParse()
