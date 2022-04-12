'''
----------------------------------------
[Lexical Analysis]
Anastasia Malinovski
Shima Iraniparast
----------------------------------------
__updated__= "2022-04-11"
----------------------------------------
'''
from Elements import *
import tokenize 
class Token:
    def __init__(self,string,line_num,line):
        self.string=string #string of token
        self.line_num=line_num #line number in which it was found
        self.line=line #string of tokens line
class symbol_object:
        """
        functions for symbol object
        """
        def __init__(self,token_obj):
            """
            Parameter:
                token_obj - list -> token, type,attribute,value 
            """
#            assert len(token_obj)==4,"invalid token"
            self.token=token_obj[0]
            self.type=token_obj[1]
            self.attribute=token_obj[2]
            self.value=token_obj[3]
            self.line=[]
            self.line.append(token_obj[0].line_num)
class Tokenizer:
    """
    Functions in order to provide lexical analysis 
    """
    
    def __init__(self,file_name,error_filename):
        self.filename=file_name
        self.error_file=error_filename
        self.num_id=0
        self.scopenames=[]
        self.table=[] #for symbol table
        self.num_error=0
    def tokenize(self):
        """
        Returns:
         a list of symbol table values
        """
        buff1=[]
        buff2=[]
        start=[0,1] #[index,buffer]
        curr=[0,1]
        lines=0
        MAXARRAYSIZE=2048
        with open(self.filename) as fh: 
            for line in fh: 
                lines+=1 #keep track of lines
                for char in line:
                    token_obj=None
                    if (len(buff1)>=MAXARRAYSIZE):
                        if (len(buff2)>=MAXARRAYSIZE):#if both buffers are full...
                            curr=[0,1]
                            buff1.clear() #clear buffer1 and start again in buff1
                            buff1.append(char)
                        else:#if buff1 is full go to buff2
                            buff2.append(char)
                    else:
                        if (len(buff2)>=MAXARRAYSIZE):# if buff2 is full and buff1 is not..
                            buff2.clear()# then clear buff2
                        buff1.append(char)
                    if (start[1]==1 and curr[1]==1): #in buffer 1
                        if (buff1[curr[0]+1].isspace()):#if lookahead is whitespace
                            a=Token(buff1[start[0]:curr[0]],lines,line)
                            if (special_characters[2] in a.line):
                                start=curr
                                curr[0]+=1
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None,'keyword',None] 
                            elif(a.string in operators):
                                token_obj=[a,None,'operator',None]
                            else: 
                                if (not a.string[0].isalpha()):
                                    self.error(a,self.error_file,'Incorrect identifier name')
                                else:
                                    token_obj=self.is_identifier(a)
                        if (len(buff1)==MAXARRAYSIZE-1):
                            curr=[0,2]#change current to next buffer if buff1 is full
                        if (len(buff1)==MAXARRAYSIZE-1):
                            start=[0,2]
                    elif (start[1]==2 and curr[1]==2): #in buffer 2
                        if (buff2[curr[0]+1].isspace()):#if lookahead is whitespace
                            a=Token(buff2[start[0]:curr[0]],lines,line)
                            if (special_characters[2] in a.line):
                                start=curr
                                curr[0]+=1
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None,'keyword',None]
                            elif(a.string in operators):
                                token_obj=[a,None,'operator',None]
                            else:
                                if (not a.string[0].isalpha()):
                                    self.error(a,self.error_file,'Incorrect identifier name')
                                else:
                                    token_obj=self.is_identifier(a)
                        if (curr[0]==MAXARRAYSIZE-1): #end of buffer
                            curr=[0,2]#change current to next buffer if buff1 is full
                        if (start[0]==MAXARRAYSIZE-1):
                            start=[0,2]
                    elif (start[1]==1 and curr[1]==2):#start in buff1, curr in buff2
                        if (buff2[curr[0]+1].isspace()):
                            a=Token(buff1[start[1:-1]]+buff2[curr[0:1]],lines,line)
                            if (special_characters[2] in a.line):
                                start=curr
                                curr[0]+=1
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None,'keyword',None]
                            elif (a.string in operators):
                                token_obj=[a,None,'operator',None]
                            else:
                                if (not a.string[0].isalpha()):
                                    self.error(a,self.error_file,'Incorrect identifier name')
                                else:
                                    token_obj=self.is_identifier(a)
                    elif (start[1]==2 and curr[1]==1): #start in buff2, curr in buff1
                        if (buff1[curr[0]+1].isspace()):
                            a=Token(buff2[start[1]:-1]+buff1[0:curr[1]],lines,line)
                            if (special_characters[2] in a.line):
                                start=curr
                                curr[0]+=1
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None, 'keyword',None]
                            elif (a.string in operators):
                                token_obj=[a,None,'operator',None]
                            elif (a.string not in special_characters):#ignore any special characters
                                if (not a.string[0].isalpha()):
                                    self.error(a,self.error_file,'Incorrect identifier name')
                                else:
                                    token_obj=self.is_identifier(a)
                    if (token_obj!=None):
                        b=symbol_object(token_obj)
                        self.table.append(b)
                        start=curr 
                        
        return
    def is_identifier(self,token):
        for x in self.table:
            if (x.token.string==token.string):
                x.line.append(token.line_num)
                return 
        if (keywords[7] in token.line or keywords[11] in token.line): #func or package
            token_obj=self.is_func_or_package(token)
            if not(keywords[4] in token.line):
                self.scopenames.append(token_obj)
            return token_obj
        
        else:
            token_obj=[]
            token_obj.append(token)
            token_obj.append(None)#type
            token_obj.append('id')#attribute identifier
            token_obj.append(None)#value 

            self.num_id+=1
        return token_obj
    def is_func_or_package(self, token):
        token_obj=[]
        if (keywords[11] in token.line): #package
            token_obj.append(token)
            token_obj.append(None)
            token_obj.append(keywords[11])
            token_obj.append(None)
        elif(keywords[7] in token.line): #func
            token_obj.append(token) #token
            token_obj.append(None) #type 
            token_obj.append(keywords[7]) #attribute
            token_obj.append(None) #value
        return token_obj
    def error(self,token,f,s):
        fh=open(f,'r+')
        print("Error on line: "+str(token.start[0])+'; '+s,file=fh)
        print('\n',file=fh)
        fh.close()
        self.num_error+=1
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
