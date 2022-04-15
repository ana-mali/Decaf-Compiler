'''
----------------------------------------
[Main program to run compiler]
----------------------------------------
__updated__= "2022-04-15"
----------------------------------------
'''
from TokenClass import Tokenizer
from ParseTree import *
a=Tokenizer('DexafCodeExample.txt','error.txt')#create token object...
#with source filename and error filename

#Lexical Analysis
a.tokenize() #initiate tokenization

#Syntax Analysis 
b=Parse_tree(a,'error.txt') #with tokenizer and error filename
b.Create_ParseTree()
#Semantic Analysis

#a.print_table('output.txt') #print symbol table to output file
