'''
----------------------------------------
[Lexical Analysis]
Anastasia Malinovski
Shima Iraniparast
----------------------------------------
__updated__= "2022-02-20"
----------------------------------------
'''

#one symbol table and simpler, file error, double buffer, regex
from Elements import *
import tokenize 
class symbol_object:
        """
        functions for symbol object
        """
        def __init__(self,token_obj):
            """
            Parameter:
                token_obj - list
                variable name, type and attribute 
            """
#            assert len(token_obj)==4,"invalid token"
            self.name=token_obj[0]
            self.type=token_obj[1]
            self.attribute=token_obj[2]
            self.value=token_obj[3]
            self.line=token_obj[4]
class Tokenizer:
    """
    Functions in order to provide lexical analysis 
    """
    
    def __init__(self,file_name):
        self.filename=file_name
        self.num_id=0
        self.scopenames=[]
        self.table=[] #buffer for symbol table

    def tokenize(self):
        """
        Returns:
         a list of symbol table values
        """
        buff1=[]
        buff2=[]
        comment_line=0
#            MAXARRAYSIZE=
        with tokenize.open(self.filename) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for token in tokens:
                buff1.append(token)
                if (comment_line==1):
                    if (token.string=='\n'):
                        comment_line=0
                    continue;
                if (token.string not in keywords and 
                     token.string not in operators and 
                     token.string not in special_characters):
                    if (token.string[0].isdigit()):
                        self.error(token)
                    else:
                        self.is_identifier(token)
                if (len(buff1)>=MAXARRAYSIZE)
                    buff2.append(token)
                    
        return
    def is_identifier(self,token):
        for x in self.table:
            if (x.name==token.string):
                x.lines.append(token.start[0])
                return 
        token_obj=[] 
        if (keywords[7] in token.line or keywords[11] in token.line):
            token_obj=self.is_func_or_package(token,token_obj)
            if not(keywords[4] in token.line):
                self.scopenames.append(token_obj)
            return
        string=token.line.split()
        if (string[0]=='var'):
            if ('=' in string):
                found2=0
                found3=0
                for x in string:
                    if (found2):
                        token_obj.append(x) #type
                        token_obj.append('var')
                    if (found3):
                        token_obj.append(x) #value
                        break;
                    if (x==token.string):
                        found2=1
                    if (x=='='):
                        found3=1;
        lines=[]
        lines.append(token.start[0])
        token_obj.append(lines)
        a=symbol_object(token_obj)
        self.table.append(a)
        self.num_id+=1
        return
    
    '''
    self.name=token[0]
    self.type=token[1]
    self.attribute=token[2]
    self.value=token[3]
    '''
    def is_func_or_package(self, token,token_obj):
        if (keywords[11] in token.line):
            token_obj.append(token.string)
            token_obj.append(keywords[11])
            token_obj.append('')
            token_obj.append(None)
        elif(keywords[7] in token.line):
            token_obj.append(token.string)
            token_obj.append(keywords[7])
            token_obj.append('')
            a=token.line.split(' ')
            a.append(None)
            prev=''
            counter=0
            if (keywords[4] in a):
                token_obj.append(a[-1])
            else:
                curr=a[counter]
                while curr is not None:
                    if prev is not None and prev is not keywords[7]:
                        if prev in keywords:
                            token_obj.append(prev)
                        else:
                            self.error(token,'error.txt')
                    counter+=1
                    curr=a[counter]
        else:
            self.error(token,'error.txt')
        if (len(self.scopenames)>0):
            token_obj[2]=self.scopenames[-1][0]
        else:
            token_obj[2]='global'
        return token_obj
    def error(self,token,f):
        fh=open(f,'r+')
        print("Error on line: "+str(token.start[0]),file=fh)
        print('\n',file=fh)
        fh.close()
        return 
    def print_table(self,output_filename):
        """
        Parameters:
            tokens - a list of tokens
        Returns:
            a printed table to a file 
        """
        fh=open(output_filename,'w+')
#        token_str_list=[]
        with tokenize.open(self.filename) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for token in tokens:
                print(token,file=fh)
#                fh.write('\n'.join('{}[}'.format(t[0], t[1]) for t in token_str_list))
        
        print('number of identifiers: {}'.format(self.num_id),file=fh)
        fh.close()
