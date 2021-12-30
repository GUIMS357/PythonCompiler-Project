# -*- coding: UTF-8 -*-

# Autora 1: Eliane Isadora Faveron Maciel
# Autor 2: Guilherme Menin Stedile
from analisador_lexico import AnaliserLexer
from grammar import MyParser


if __name__ == '__main__':

    file_open = open("fonte.txt", "r")
    lexer = AnaliserLexer()
    file_data = file_open.read()
    lexer.tokenize_data(file_data)

    lexer.transform_tokens()
    file_open = open("Saida.txt", "w")
    file_open.write("\n".join(lexer.tokens_result_str))
    file_open.close()

    file_open = open("fonte.txt", "r")
    data = file_open.readlines()
    lexer = AnaliserLexer()
    parser = MyParser()

    for line in data:
        result = parser.parse(lexer.tokenize(line))