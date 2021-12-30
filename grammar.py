# -*- coding: UTF-8 -*-

from sly import Parser
from analisador_lexico import AnaliserLexer


class Expr:
    pass


class BinOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssingOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Number(Expr):
    def __init__(self, value):
        self.value = int(value)


class MyParser(Parser):
    tokens = AnaliserLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', AND, OR),
        ('left', MAIOR, MENOR, MAIOREQUALS, MENOREQUALS, EQUALS, DIFF),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', IF, ELSE),
        ('right', NOT),
    )

    def __init__(self):
        self.debug = True
        self.names = {}

    @_('ID ASSIGN expr')
    def statement(self, p):
        self.names[p.ID] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('expr PLUS expr',
        'expr MINUS expr',
        'expr TIMES expr',
        'expr DIVIDE expr')
    def expr(self, p):
        return BinOp(p[1], p.expr0, p.expr1)

    @_('expr MENOR expr',
        'expr MAIOR expr',
        'expr MENOREQUALS expr',
        'expr MAIOREQUALS expr')
    def expr(self, p):
        return BinOp(p[1], p.expr0, p.expr1)


    @_('ID SUMEQUALS expr')
    def sumequals(self, p):
        try:
            if self.names[p.ID]:
                self.names[p.ID] += int(p.NUMBER)
        except LookupError:
            print("Undefined name '%s'" % p.ID)
            return 0

    @_('ID MINUSEQUALS expr')
    def minusequals(self, p):
        return (p[1], p[2])

    @_('COLON')
    def expr(self, p):
        return p.COLON

    @_('IF ID IN ID COLON expr')
    def expr(self, p):
        return p.expr

    @_('IF expr COLON')
    def expr(self, p):
        return p

    @_('IF ID COLON')
    def expr(self, p):
        return p

    @_('FOR ID IN ID COLON')
    def expr(self, p):
        return p

    @_('WHILE ID COLON',
        'WHILE TRUE COLON')
    def expr(self, p):
        return p

    @_('DEF ID factor COLON')
    def expr(self, p):
        return p

    @_('CLASS ID factor COLON',
        'CLASS ID COLON')
    def expr(self, p):
        return p

    @_('PASS')
    def expr(self, p):
        return p.PASS

    @_('expr OR expr')
    def expr(self, p):
        return ('OR', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('AND', p.expr0, p.expr1)

    @_('factor')
    def expr(self, p):
        return p.factor

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    @_('ID')
    def expr(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            print("Undefined name '%s'" % p.ID)
            return 0

    def error(self, p):
        if p:
            print("Syntax error at {0}, in line {1}, colum {2}".format(
                    p.type,
                    p.lineno,
                    p.index
                )
            )
            self.errok()
        else:
            # print("End of File!")
            return
        self.restart()
