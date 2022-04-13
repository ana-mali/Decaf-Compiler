'''
----------------------------------------
[Lexical Analysis]
Anastasia Malinovski
Shima Iraniparast
----------------------------------------
__updated__= "2022-04-11"
----------------------------------------
'''
state_machine=['start','keyword/id/number','operator','space']
from Elements import *
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
            self.attribute=token_obj[2] #string   keyword, operator, identifier
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
        status=state_machine[0]
        prev_state=state_machine[0]
        state=0 #0 to indicate no current state change 
        MAXARRAYSIZE=2048
        with open(self.filename) as fh: 
            for line in fh: 
                lines+=1 #keep track of lines
                if (len(line)<1):
                    curr[0]+=1
                    continue;
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
                    curr[0]+=1
                    if (special_characters[11] in line):
                        index=curr[0]
                        buff=curr[1]
                        start[0]=index
                        start[1]=buff
                        continue;
                    if (start[1]==1 and curr[1]==1): #in buffer 1
                        temp=status
                        prev_state=temp
                        status,state=self.check_state(status, char)
                        if (prev_state=='space' and status=='space'):
                            token_obj='ignore'
                        if (state and token_obj==None): #if state=1 then a change of state has occurred
                            a=Token(''.join(buff1[start[0]:curr[0]]),lines,line)
                            if (prev_state==state_machine[1]):#keyword/id/number
                                if True in [x.isdigit() for x in a.string]:
                                    if (a.string.isdigit()):
                                        token_obj=[a,None,'number',None]
                                    else:
                                        token_obj=self.is_identifier(a)
                                elif (a.string in keywords):
                                    token_obj=[a,None,'keyword',None]
                                else:
                                    token_obj=self.is_identifier(a) #identifier w/o numbers
                            elif (prev_state==state_machine[2]): #operator
                                if (a.string in operators):
                                    token_obj=[a,None,'operator',None]
                                else:
                                    self.error(a,'Not an operator')
                            else:
                                
                                token_obj='ignore'
                            # if space or special characters, ignore and keep going
                
                    elif (start[1]==2 and curr[1]==2): #in buffer 2
                        temp=status
                        prev_state=temp
                        status,state=self.check_state(status, char)
                        if (prev_state=='space' and status=='space'):
                            token_obj='ignore'
                        if (state and token_obj==None): #if state=1 then a change of state has occurred
                            a=Token(''.join(buff1[start[0]:curr[0]]),lines,line)
                            if (prev_state==state_machine[1]):#keyword/id/number
                                if True in [x.isdigit() for x in a.string]:
                                    if (a.string.isdigit()):
                                        token_obj=[a,None,'number',None]
                                    else:
                                        token_obj=self.is_identifier(a)
                                elif (a.string in keywords):
                                    token_obj=[a,None,'keyword',None]
                                else:
                                    token_obj=self.is_identifier(a) #identifier w/o numbers
                            elif (prev_state==state_machine[2]): #operator
                                if (a.string in operators):
                                    token_obj=[a,None,'operator',None]
                                else:
                                    self.error(a,'Not an operator')
                            else:
                                
                                token_obj='ignore'
                            # if space or special characters, ignore and keep going
                    elif (start[1]==1 and curr[1]==2):#start in buff1, curr in buff2
                        temp=status
                        prev_state=temp
                        status,state=self.check_state(status, char)
                        if (prev_state=='space' and status=='space'):
                            token_obj='ignore'
                        if (state and token_obj==None): #if state=1 then a change of state has occurred
                            a=Token(''.join(buff1[start[0]:curr[0]]),lines,line)
                            if (prev_state==state_machine[1]):#keyword/id/number
                                if True in [x.isdigit() for x in a.string]:
                                    if (a.string.isdigit()):
                                        token_obj=[a,None,'number',None]
                                    else:
                                        token_obj=self.is_identifier(a)
                                elif (a.string in keywords):
                                    token_obj=[a,None,'keyword',None]
                                else:
                                    token_obj=self.is_identifier(a) #identifier w/o numbers
                            elif (prev_state==state_machine[2]): #operator
                                if (a.string in operators):
                                    token_obj=[a,None,'operator',None]
                                else:
                                    self.error(a,'Not an operator')
                            else:
                                
                                token_obj='ignore'
                            # if space or special characters, ignore and keep going
                    elif (start[1]==2 and curr[1]==1): #start in buff2, curr in buff1
                        temp=status
                        prev_state=temp
                        status,state=self.check_state(status, char)
                        if (prev_state=='space' and status=='space'):
                            token_obj='ignore'
                        if (state and token_obj==None): #if state=1 then a change of state has occurred
                            a=Token(''.join(buff1[start[0]:curr[0]]),lines,line)
                            if (prev_state==state_machine[1]):#keyword/id/number
                                if True in [x.isdigit() for x in a.string]:
                                    if (a.string.isdigit()):
                                        token_obj=[a,None,'number',None]
                                    else:
                                        token_obj=self.is_identifier(a)
                                elif (a.string in keywords):
                                    token_obj=[a,None,'keyword',None]
                                else:
                                    token_obj=self.is_identifier(a) #identifier w/o numbers
                            elif (prev_state==state_machine[2]): #operator
                                if (a.string in operators):
                                    token_obj=[a,None,'operator',None]
                                else:
                                    self.error(a,'Not an operator')
                            else:
                                token_obj='ignore'
                            # if space or special characters, ignore and keep going
                    if (token_obj!=None):
                        if (token_obj!='ignore' and not self.is_token_or_symbol(token_obj)):
                            b=symbol_object(token_obj)
                            self.table.append(b)
                            print(b.token.string)
                        elif (self.is_token_or_symbol(token_obj)):#true if symbol
                            self.table.append(token_obj)
                            print(token_obj.token.string)
                            
                        index=curr[0]
                        buff=curr[1]
                        start[0]=index
                        start[1]=buff
                        #set start=curr
                        if not(curr[0]+1<MAXARRAYSIZE):
                            if (curr[1]==1):
                                curr[1]=2
                                curr[0]=0
                            else:
                                curr[1]=1
                                curr[0]=0
        return
    def is_token_or_symbol(self,a):
        '''
        Parameter:
            a - either a symbol object or token object
        Return:
            b - 1 if symbol object and 0 if token object
        '''
        if (type(a)==symbol_object):
            return 1
        else:
            return 0
    def change_state(self,status,char):
        '''
        Parameters:
            status - string from state_machine
            char - from tokenizer
        Return: 
            status - new status
        '''
        if (char.isalpha() or char.isdigit() or char=='_'):
            status=state_machine[1]#keyword/id/number
        elif (char in operators):
            status=state_machine[2]#operator
        else:
            status=state_machine[3]#space or special character
        return status
    def check_state(self,status,char):
        '''
        Parameters:
            status - string from state_machine
            char - from tokenizer
        Returns:
            status - new or same status 
            change - 0 if same status and 1 if new status
        '''
        if (status==state_machine[0]):#start to beginning state 
            status=self.change_state(status, char)
            return status,0 #will return 0 to continue tokenizing 
        elif (status==state_machine[1]):#keyword/id/number
            if (char.isalpha() or char.isdigit() or char=='_'):
                return status,0 
            else:
                status=self.change_state(status, char)
                return status,1
        elif (status==state_machine[2]):#operator
            if (char in operators):
                return status,0
            else:
                status=self.change_state(status, char)
                return status, 1
        else: #space
            if (char in special_characters):
                return status,0
            else:
                status=self.change_state(status, char)
                return status, 1
    def is_identifier(self,token):
        if (token.string[0].isdigit()):
            self.error(token,'Incorrect identifier name')
            return 
        for x in self.table:
            if (x.token.string==token.string):
                x.line.append(token.line_num)
                return x
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
        print("Error on line: "+str(token.line_num)+"; token: "+token.string+' ; '+s,file=fh)
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
