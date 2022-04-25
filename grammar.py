from Elements import *
from TokenClass import *
from ParseTree import *
from Semantics import *


class Grammar_analysis:


    def __init__(self, parse_tree_filename, error_filename):
        """
        Parameters:
            type - keywords and or statements
            gram - grammar associated with the keyword
        Forms:
            Generates errors where necessary 
            checks scope and types
            Updates symbol table with values 
        """
        self.tokenizer = Tokenizer
        self._error_file = error_filename
        self.parse_tree_file = parse_tree_filename
        self.type = ""
        self.gram = []
        self.all_gram = []
        # self.scopes = Tokenizer.generate_scopenames(Tokenizer)

    def read_lines_grammer(self):
        gram_file = open("grammar list.txt", 'r')
        for line in gram_file:
            gram = line.split(' ')
            gram = line.split('=')
            self.type = gram[0]
            self.gram = gram[1::]
            a = []
            a.append(self.type)
            a.append(self.gram)
            self.all_gram.append(a)
            print(self.all_gram)
        return

    def find_gram(self, token):
        # for t in

        return
    
    def print_tree(self):
        success = False
        tree_file = open("parse tree.txt", 'r+')
        code = open("DexafCodeExample.txt", 'r+')
        error = open("error.txt", 'r+')
        tabs = "\t"
        n_tabs = 0
        print( "program", file=tree_file)
        for line in code:
            l = line.split(" ")
            if "//" not in l:
                if "package" in l: #package found
                    print("package" + l[-1], file=tree_file)
                    n_tabs+=1
                    print("block", file=tree_file)
                elif "var" in l: #variable decleration/definition
                    if "=" in l:
                        print("variable :" + l[1] + l[-1] + l[-2], file=tree_file)
                    else:
                        print("variable " + l[-2], file=tree_file)

                elif "func" in l: #function decleration
                    print("Function: " + l[1] + l[-2], file=tree_file)
                    n_tabs+=1
                elif "if" in l:
                    print("Conditional", file = tree_file)
                    n_tabs+=1
                    print("if: " + l[2] + l[3] + l[4], file=tree_file)
                    n_tabs +=1
                    print("return: " + "location: "+ l[-4], file=tree_file)
                elif "else" in l:
                    print("Conditional", file = tree_file)
                    n_tabs+=1
                    print( "else: " , file=tree_file)
                    n_tabs +=1
                    print( "return: " + "location: "+ l[-3], file=tree_file)
                else:
                    print("could not create parse tree", file = error )
            else:
                continue;

            # for i in range (len(l)):
            #     if l[i] in self.scopes:
            #         print("FunctionCall:" + l[i] + l[i+1::], file = tree_file)
                
    
        tree_file.close()
        code.close()
        error.close()
        return


