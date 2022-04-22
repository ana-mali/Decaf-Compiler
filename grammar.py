from Elements import *
from TokenClass import *
from ParseTree import *


class Grammar:


    def __init__(self, Tokenizer, type, gram):
        """
        Parameters:
            type - keywords and or statements
            gram - grammar associated with the keyword
        Forms:
            Generates errors where necessary 
            checks scope and types
            Updates symbol table with values 
        """
        self.type = type
        self.gram = []

    def read_line(self, s):
        gram = s.split(' ')
        gram = s.split('=')
        self.type = gram[0]
        self.gram = gram[1::]
        return

    def read_file(self, f):
        gram_file = open("grammar list.txt", 'r')
        for line in gram_file:
            read_line(line)
            return


