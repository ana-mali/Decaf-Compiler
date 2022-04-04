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
        MAXARRAYSIZE=2048
        with tokenize.open(self.filename) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for token in tokens:
                if (len(buff1)>=MAXARRAYSIZE):
                    buff2.append(token)
                else:
                    buff1.append(token)
                if (comment_line==1):
                    if (token.string=='\n'):
                        comment_line=0
                    continue;
                if (token.string not in keywords and 
                     token.string not in operators and 
                     token.string not in special_characters):
                    if (token.string[0].isdigit()):
                        self.error(token,'error.txt','Incorrect identifier name')
                    else:
                        if (keywords[0] in token.line or keywords[9] in token.line):
                            self.is_identifier(token)
                        else:
                            self.error(token,'error.txt',"Not a 'var' type")
                
        return
    def is_identifier(self,token):
        for x in self.table:
            if (x.name==token.string):
                x.lines.append(token.start[0])
                return 
        token_obj=[] 
        if (keywords[7] in token.line or keywords[11] in token.line): #func or package
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
                        token_obj.append('var') #attribute
                    if (found3):
                        if (token_obj[1]==keywords[0]):#bool
                            if ('true' in x or 'false' in x ):
                                token_obj.append(x) #value
                            else:
                                self.error(token,'error.txt','value does not match type')
                        elif (token_obj[1]==keywords[9]):#int 
                            if (x[-1]==';'): 
                                if (x[0:-2].isdigit()):
                                    token_obj.append(x)#value
                                else:
                                    self.error(token,'error.txt','value does not match type')
                            else:
                                self.error(token,'error.txt','no semi colon')
                        break;
                    if (x==token.string):
                        token_obj.append(x)
                        found2=1
                    if (x=='='):
                        found3=1;
            else:
                for x in string:
                    if (x==token.string):
                        if (','==x[-1]):
                            token_obj.append(x[0:-2]) #name
                        else:
                            token_obj.append(x)
                    break;
                if (string[-1] in keywords[0]): #bool 
                    if ('true' in string[-1] or 'false' in string[-1]):
                        if (string[-1][-1]==';' ):
                            token_obj.append(x[0:-2])
                        else:
                            self.error(token,'error.txt','no semi colon')
                elif (string[-1] in keywords[9]): #int
                    if (string[-1][-1]==';'):
                        token_obj.append(x[0:-2])
                    else:
                        self.error(token,'error.txt','no semi colon')
                else:
                    self.error(token,'error.txt','Incorrect syntax')
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
                            self.error(token,'error.txt','Repeated keyword')
                    counter+=1
                    curr=a[counter]
        else:
            self.error(token,'error.txt','Not a function or package')
        if (len(self.scopenames)>0):
            token_obj[2]=self.scopenames[-1][0]
        else:
            token_obj[2]='global'
        token_obj.append(token.start[0])
        return token_obj
    def error(self,token,f,s):
        fh=open(f,'r+')
        print("Error on line: "+str(token.start[0])+'; '+s,file=fh)
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
