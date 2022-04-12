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
        """
        Creates a Token object with string name of token
        the line number in which it is used 
        and the full string of the line it is on
        """
        self.string=string #string of token
        self.line_num=line_num #line number in which it was found
        self.line=line #string of tokens line
class symbol_object:
        """
        function for symbol objects
        """
        def __init__(self,token_obj):
            """
            Parameter:
                token_obj - list -> token, type,attribute,value 
            """
#            assert len(token_obj)==4,"invalid token"
            self.token=token_obj[0] #list
            self.type=token_obj[1] #string
            self.attribute=token_obj[2] #string
            self.value=token_obj[3] #string 
            self.line=[] #list
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
        -reads filename and creates token objects
        -token objects are turned to symbol objects after analysis
        -symbol objects get added to symbol table that can be printed after
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
                    if (len(buff1)<2):
                        continue;
                    if (start[1]==1 and curr[1]==1): #in buffer 1
                        if (buff1[curr[0]+1].isspace()):#if lookahead is whitespace
                            a=Token(''.join(buff1[start[0]:curr[0]+1]),lines,line)
                            if (special_characters[2] in a.line):
                                index=curr[0]
                                buff=curr[1]
                                start[0]=index 
                                start[1]=buff
                                curr[0]+=1
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None,'keyword',None] 
                            elif(a.string in operators):
                                token_obj=[a,None,'operator',None]
                            elif (a.string not in special_characters):
                                if (not a.string[0].isalpha()):
                                    self.error(a,'Incorrect identifier name')
                                else:
                                    token_obj=self.is_identifier(a)
                    elif (start[1]==2 and curr[1]==2): #in buffer 2
                        if (buff2[curr[0]+1].isspace()):#if lookahead is whitespace
                            a=Token(''.join(buff2[start[0]:curr[0]+1]),lines,line)
                            if (special_characters[2] in a.line):
                                index=curr[0]
                                buff=curr[1]
                                start[0]=index 
                                start[1]=buff
                                curr[0]+=1
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None,'keyword',None]
                            elif(a.string in operators):
                                token_obj=[a,None,'operator',None]
                            else:
                                if (not a.string[0].isalpha()):
                                    self.error(a,'Incorrect identifier name')
                                else:
                                    if (not a.string in special_characters):
                                        token_obj=self.is_identifier(a)
                        if (curr[0]==MAXARRAYSIZE-1): #end of buffer
                            curr=[0,2]#change current to next buffer if buff1 is full
                        if (start[0]==MAXARRAYSIZE-1):
                            start=[0,2]
                    elif (start[1]==1 and curr[1]==2):#start in buff1, curr in buff2
                        if (buff2[curr[0]+1].isspace()):
                            a=Token(''.join(buff1[start[1:-1]]+buff2[0:curr[0]+1]),lines,line)
                            if (special_characters[2] in a.line):
                                index=curr[0]
                                buff=curr[1]
                                start[0]=index 
                                start[1]=buff
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None,'keyword',None]
                            elif (a.string in operators):
                                token_obj=[a,None,'operator',None]
                            else:
                                if (not a.string[0].isalpha()):
                                    self.error(a,'Incorrect identifier name')
                                else:
                                    if (not a.string in special_characters):
                                        token_obj=self.is_identifier(a)
                    elif (start[1]==2 and curr[1]==1): #start in buff2, curr in buff1
                        if (buff1[curr[0]+1].isspace()):
                            a=Token(''.join(buff2[start[1]:-1]+buff1[0:curr[1]+1]),lines,line)
                            if (special_characters[2] in a.line):
                                index=curr[0]
                                buff=curr[1]
                                start[0]=index 
                                start[1]=buff
                                curr[0]+=1
                                continue;
                            if (a.string in keywords):
                                token_obj=[a,None, 'keyword',None]
                            elif (a.string in operators):
                                token_obj=[a,None,'operator',None]
                            elif (a.string not in special_characters):#ignore any special characters
                                if (not a.string[0].isalpha()):
                                    self.error(a,'Incorrect identifier name')
                                else:
                                    if (not a.string in special_characters):
                                        token_obj=self.is_identifier(a)
                    if (token_obj!=None):
                        b=symbol_object(token_obj)
                        self.table.append(b)
                        index=curr[0]
                        buff=curr[1]
                        start[0]=index+2 #skip white space and last letter of token
                        start[1]=buff 
                        print(b.token.string)
                        if (curr[0]+1<MAXARRAYSIZE):
                            curr[0]+=1
                    else:
                        curr[0]+=1
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
    def error(self,token,s):
        fh=open(self.error_file,'r+')
        print("Error on line: "+str(token.line_num)+'; '+s,file=fh)
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
        for x in self.table:
            print(x)
        print('number of identifiers: {}'.format(self.num_id))
    return
