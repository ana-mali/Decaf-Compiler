'''
----------------------------------------
[Parser]
----------------------------------------
__updated__= "2022-04-15"
----------------------------------------
'''
from TokenClass import Token,symbol_object,Tokenizer
from Elements import *
from _ast import And
state_machine=['start','keyword','id','number','operator','space']

#LL(1), type checking and scope checking 
#syntax does not change symbol table objects
#in documentation, grammer is given
#load manual parse table into seperate file 
class Node:
    def __init__(self,symbol_objects,counter):
        '''
        Parameters:
            symbol_objects - section of symbol table
            scopename - global or one that is in scopenames list
            counter - helper for generate_states
        Forms:
            value - list of all n tokens
            states - list of n states for each token
            scopename - scopename this scope exists in (storage for semantics)
            left - empty node to be added later
            right - empty node to be added later
            
        '''
        self.tokens=[]
        for x in symbol_objects:
            self.tokens.append(x)
        self.states=self.generate_states(counter)
        self.right=None 
        self.left=None
        
        
    def generate_states(self,counter):
        '''
        pre-hard coded states to be used while creating 
        parsing tree to check grammer
        '''
        if (counter==0):
            state0=[[state_machine[1],keywords[11]],[state_machine[2],'global'],
                [state_machine[4],operators[0]],[state_machine[1],keywords[15]],
                [state_machine[2],'global'],[state_machine[1],keywords[9]],
                [state_machine[4],operators[8]],[state_machine[3],'number'],
                [state_machine[4],operators[5]],[state_machine[1],keywords[15]],
                [state_machine[2],'global'],[state_machine[1],keywords[9]],
                [state_machine[4],operators[8]],[state_machine[3],'number'],
                [state_machine[4],operators[5]]]
            return state0
        elif (counter==1):
            state1=[[state_machine[1],keywords[7]],[state_machine[2],'GreatestCommonDivisor'],
                [state_machine[4],operators[6]],[state_machine[4],operators[7]],
                [state_machine[1],keywords[9]],[state_machine[4],operators[0]],
                [state_machine[1],keywords[15]],[state_machine[2],'main'],
                [state_machine[4],operators[4]],[state_machine[2],'main'],
                [state_machine[4],operators[4]],[state_machine[2],'main'],
                [state_machine[1],keywords[9]],[state_machine[4],operators[5]],
                [state_machine[2],'main'],[state_machine[4],operators[8]],
                [state_machine[2],'GreatestCommonDivisor'],[state_machine[4],operators[5]],
                [state_machine[2],'main'],[state_machine[4],operators[8]],
                [state_machine[2],'GreatestCommonDivisor'],[state_machine[4],operators[5]],
                [state_machine[2],'main'],[state_machine[4],operators[8]],
                [state_machine[2],'GreatestCommonDivisor'],[state_machine[4],operators[6]],
                [state_machine[2],'main'],[state_machine[4],operators[4]],
                [state_machine[2],'main'],[state_machine[4],operators[7]],
                [state_machine[4],operators[5]],[state_machine[4],operators[1]]]
            return state1
        elif (counter==2):
            state2=[[state_machine[1],keywords[7]],[state_machine[2],'GreatestCommonDivisor'],
                [state_machine[4],operators[6]],[state_machine[2],'GreatestCommonDivisor'],
                [state_machine[1],keywords[9]],[state_machine[4],operators[4]],
                [state_machine[2],'GreatestCommonDivisor'],[state_machine[1],keywords[9]],
                [state_machine[4],operators[7]],[state_machine[1],keywords[9]],
                [state_machine[4],operators[5]]]
            return state2
        elif (counter==3):
            state3=[[state_machine[1],keywords[8]],[state_machine[4],operators[6]],
               [state_machine[2],'gcd'],[state_machine[4],operators[21]],
               [state_machine[3],'number'],[state_machine[4],operators[7]],
               [state_machine[4],operators[0]],[state_machine[1],keywords[12]],
               [state_machine[4],operators[6]],[state_machine[2],'gcd'],
               [state_machine[4],operators[7]],[state_machine[4],operators[5]],
               [state_machine[4],operators[1]]]
            return state3
        elif (counter==4):
            state4=[[state_machine[1],keywords[3]],[state_machine[4],operators[0]],
                [state_machine[1],keywords[12]],[state_machine[4],operators[6]],
                [state_machine[2],'gcd'],[state_machine[4],operators[4]],
                [state_machine[2],'GreatestCommonDivisor'],[state_machine[4],operators[18]],
                [state_machine[2],'GreatestCommonDivisor'],[state_machine[4],operators[7]],
                [state_machine[4],operators[7]],[state_machine[4],operators[5]],
                [state_machine[4],operators[1]]]
            return state4
        elif (counter==5):
            state5=[[state_machine[4],operators[1]]]
            return state5
        elif (counter==6):
            state6=[[state_machine[4],operators[1]]]
            return state6
        else:
            print('counter wrong')
        return 
            
class Parse_tree:
    """
    Functions used to utilize a structured tree from source code
    """
    def __init__(self,tokenizer,error_filename):
        """
        Parameter:
            scopenames - list of scopenames from Tokenizer
            error_filename - from Tokenizer 
        Forms:
            saves scopenames for reference of trees
            saves error_filename for error log
            create an empty head node 
            
            variable name, type and attribute 
        """
        
        self.error_file=error_filename
        self.head=None
        self.tokenizer=tokenizer
#            self.previousscope=None
    def Create_ParseTree(self):
        '''
        Parameters:
            symbol_table - entire symbol table generated from tokenizer
        Forms:
            -seperates scopes
        '''
        symbol_table=self.tokenizer.table
        counter=0 #number of scopes
        section=[]
        index_start=0 #method to form sections
        index_curr=0
        num_open=0 #open curly brackets
        num_close=0 #closed curly brackets
        for x in symbol_table:
            if (x==symbol_table[0]):
                continue
            index_curr+=1
            if(counter>6):
                print('counter over ')
                break;
            if (index_curr>=len(symbol_table)):
                self.check_section(symbol_table[index_start],counter)
                a=Node(section,counter)
                self.insert_node(a, counter)
                counter+=1
                #call final section
            if (x.token.string==operators[0]):
                num_open+=1
            elif (x.token.string==operators[1]):
                num_close+=1
                section=symbol_table[index_start:index_curr+1] #check lookahead
                a=Node(section,counter)
                self.insert_node(a,counter)
                index_curr+=1
                temp=index_curr 
                index_start=temp
                counter+=1
                continue
            if (x.token.string==keywords[7] #func
                or x.token.string==keywords[11] #package
                or keywords[3]==x.token.string #else
                or keywords[8]==x.token.string): #if
                section=symbol_table[index_start:index_curr]
                a=Node(section,counter)
                self.insert_node(a,counter)
                temp=index_curr 
                index_start=temp 
                counter+=1
    def insert_node(self,node,counter):
        if (self.head==None):
            self.head=node
        else:
            root=self.head
            if (root.left==None and counter==1):
                root.left=node
            elif (root.right==None and counter==2):
                root.right=node
            elif (root.right.left==None and counter==3):
                root.right.left=node
            elif (root.right.right==None and counter==4):
                root.right.right=node 
            elif (root.right.left==None and 
                  root.right.right.left==None and 
                  counter==5):                
                root.right.left=node
                root.right.right.left=node
            elif (root.left.right==None and 
                  root.right.right.left.left==None and 
                  root.right.left.right.left==None and 
                  counter==6):
                root.left.right=node
                root.right.right.left.left=node
                root.right.left.right.left=node 
            else:
                print('insert node incorrect')
        return
    def check_section(self,node):      
        '''
        Checks correct syntax
        generates errors if necessary
        '''
        for x in range(len(node.tokens)):
            if (node.tokens[x].attribute==node.states[x][0]):#correct state
                if (node.tokens[x].attribute==state_machine[1]):#keyword
                    if (node.tokens[x].token.string!=node.states[x][1]):
                        self.error(node.tokens[x],'Incorrect keyword used')
                elif(node.tokens[x].attribute==state_machine[4]):#operator
                    if (node.tokens[x].token.string!=node.states[x][1]):
                        self.error(node.tokens[x],'Incorrect operator used')
                elif (node.tokens[x].attribute==state_machine[3]):#number
                    if (not node.tokens[x].token.string.isdigit()):
                        self.error(node.tokens[x],'Expected a number')
                else:#identifier
                    if (keywords[7] in node.tokens[x].token.line):#func 
                        if(node.tokens[x].attribute!=keywords[7]):
                            self.error(node.tokens[x],'Identifier must be a func')
                    elif(keywords[11] in node.tokens[x].token.line):
                        if (node.tokens[x].attribute!=keywords[11]):
                            self.error(node.tokens[x],'Identifier must be a package')
                    else:
                        if (node.tokens[x].attribute!='id'):
                            self.error(node.tokens[x],'Expected an identifier')
    def error(self,sym_obj,s):
        fh=open(self.error_file,'r+')
        print("Error on line: "+str(sym_obj.token.line_num)+"; token: "+sym_obj.token.string+' ; '+s,file=fh)
        print('\n',file=fh)
        fh.close()
        self.tokenizer.num_error+=1
        return 
        
        
