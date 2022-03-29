'''
----------------------------------------
[program description]
----------------------------------------
__updated__= "2022-02-20"
----------------------------------------
'''
from TokenClass import Tokenizer
a=Tokenizer('DexafCodeExample.txt')
a.tokenize()
a.print_table('output.txt')
