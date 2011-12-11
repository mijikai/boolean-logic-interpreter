#!/usr/bin/env python3

import parser

def testTokenizer():
    tokenizer = propositional.Tokenizer("")
    class Dummy(Exception): pass

    def test(string, opers, values, exception=Dummy):
        tokenizer.iterable = string
        tokenizer.operators = opers
        tokenizer.ind = 0
        passed = True

        try:
            for token, value in zip(tokenizer, values):
                if token != value:
                    passed = False
                    break

        except exception as ex:
            passed = True
        except Exception as ex:
            passed = False

        if passed:
            print('Passed: string =', repr(string), ', opers =',  repr(opers), 
                  ', values = ', repr(values))
        else:
            print('Failed:', 'string =', repr(string), ', opers =', repr(opers), ',',
                   repr(token), '!=', repr(value))

    test('', frozenset([]), [])
    test('2', frozenset([]), ['2'])
    test('2 e\t4\n5\r6', frozenset([]), ['2', 'e', '4', '5', '6'])
    test('2*3', frozenset(['*']), ['2', '*', '3'])
    test('2*3 +4 -5*6', frozenset(['+', '-', '*']),
        ['2', '*', '3', '+', '4', '-', '5', '*', '6'])

if __name__ == '__main__':
    testTokenizer()
