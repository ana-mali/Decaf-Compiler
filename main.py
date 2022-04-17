'''
----------------------------------------
[Main program to run compiler]
----------------------------------------
__updated__= "2022-04-15"
----------------------------------------
'''
from TokenClass import Tokenizer
from ParseTree import *
from Semantics import *
a=Tokenizer('DexafCodeExample.txt','error.txt')#create token object...
#with source filename and error filename

#Lexical Analysis
a.tokenize() #initiate tokenization

for x in a.table:
    print(x.token.string+' : '+x.attribute)
a.count_identifiers()
print('number of identifiers: '+ str(a.num_id))

#Syntax Analysis 
b=Parse_tree(a,'error.txt') #with tokenizer and error filename
b.Create_ParseTree()

#Semantic Analysis
c=Semantic_analysis(a,b,'error.txt')
c.Semantics()
print('number of errors: '+ str(a.num_error))

#a.print_table('output.txt') #print symbol table to output file
