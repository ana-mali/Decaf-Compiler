'''
----------------------------------------
[Intermediate Representation]
----------------------------------------
__updated__= "2022-04-17"
----------------------------------------
'''
from ParseTree import *
from TokenClass import *
from Semantics import * 

class IR:
    def __init__(self,tokenizer,parser,semn,output_file):
        self.tokenizer=tokenizer 
        self.parse=parser 
        self.semantics=semn 
        self.output=output_file
        self.package=None
        self.functions=[]
        self.N=10 #arbitrary memory space
        self.temp_var=[]
        self.temp_num=0 #number of temp variables
        self.pack_num=4 #number for package use variables
        self.L=0 #for GoTo's
     
    def Create_IR(self):
        if (self.tokenizer.num_error==0):
            lines=self.tokenizer.table[0].token.line_num
            curr_func=None
            fh=open(self.output,'w')
            line=[]
            print(lines)
            for y in self.tokenizer.table:
                temp=y.line.pop(0)
                if (temp>lines):
                    lines=temp 
                    for x in line:
                        if (x.attribute==keywords[11]):#package
                            self.package=x.token.string
                        elif (x.attribute==keywords[7]): #func 
                            self.functions.append(x.token.string)
                            l=[]
                            for o in line:
                                l.append(o.token.string)
                            if (keywords[7] in l):#func declaration
                                curr_func=x.token.string
                                s='_'+x.token.string 
                                if (self.package is not None):#func in package
                                    s='_'+self.package+'._'+s+':'
                                    print(s,file=fh)
                                    print('BeginFunc '+str(self.N)+';',file=fh)
                                else: #func with no package
                                    s='_'+s 
                                    print(s+':\n',file=fh)
                                    print('BeginFunc'+self.N+';',file=fh)
                            else: #function call
                                if ('return' in l):
                                    list=[] 
                                    var1=None 
                                    var2=None
                                    for e in l:
                                        if ('b'==e and var1==None):
                                            var1=e
                                        if ('a'==e):
                                            var2='*(this+4)%*(this+8)'
                                            break  
                                    j=len(self.temp_var)-1
                                    while j>0:
                                        if (self.temp_var[j][0]==var1):
                                            print('PushParam '+self.temp_var[j][1]+';',file=fh)
                                            break;
                                        elif (self.temp_var[j][0]==var2):
                                            print('PushParam '+self.temp_var[j][1]+';',file=fh)
                                        j-=1
                                    print('LCall _'+self.package+'._'+x.token.string,file=fh)
                                    print('PopParam '+str(self.N)+';',file=fh)
                                else:
                                    list=[] 
                                    i=0
                                    while (l[i]!=')'):
                                        if ((l[i] == "(" and l[i+1]!=')') or l[i] == ","):
                                            list.append(l[i+1])
                                        i+=1 
                                    for r in self.temp_var:
                                        if (r[0] in list):
                                            print('PushParam '+r[1]+';',file=fh)
                                    print('LCall _'+self.package+'._'+x.token.string,file=fh)
                                    print('PopParam '+str(self.N)+';',file=fh)
                        elif (x.attribute=='id'): #identifier
                            if (curr_func is None):#Inside package not function
                                l=[x.token.string,'*(this+'+str(self.pack_num)+')']
                                self.pack_num=self.pack_num+4
                                self.temp_var.append(l) #create variable
                                continue;
                            found=0
                            for r in line:
                                if (r.token.string=='var' or 
                                    r.token.string=='func'):
                                    found=1
                                    break; 
                            if (found):
                                print('_t'+str(self.temp_num)+'='+x.token.string+';',file=fh)
                                self.temp_var.append([x.token.string,'_t'+str(self.temp_num)])
                                self.temp_num+=1
                            
                        elif (x.token.string==operators[8]):#=
                            l=[]
                            for o in line:
                                l.append(o.token.string)
                            var1=None 
                            var2=None
                            for j in l:
                                for z in self.temp_var:
                                    if (z[0]==j and var1 is None):
                                        var1=z[1]
                                    elif (z[0]==j and var2 is None):
                                        var2=z[1]
                                        break;
                            if ('z' in l):
                                continue;
                            elif (var1!=None and var2!=None):
                                print(var1+'='+var2+';',file=fh)
                        elif (x.token.string==operators[1]): #closing curly bracket
                            l=[] 
                            for o in line:
                                l.append(o.token.string)
                            if (curr_func!=None and 'if' not in l):
                                print('EndFunc ;',file=fh)
                                curr_func=None
                                continue;
                        elif (x.token.string==keywords[8]): #If statement
                            l=[]
                            for o in line:
                                l.append(o.token.string)
                            list=[]
                            i=0
                            while (l[i] != ")"): #get boolean exp
                                if (l[i] == "(" or (l[i+1] != "(") and l[i+1] != ")"):
                                    list.append(l[i+1])
                                i+=1
                            var1=None 
                            var2=None
                            for z in self.temp_var:
                                if (z[0]==list[0]):
                                    var1=z[1] 
                                elif (z[0]==list[2]):
                                    var2=z[1]
                                    break;
                            if (var2==None):
                                var2=list[-1]
                            print('_t'+str(self.temp_num)+'='+var1+list[1]+var2+';',file=fh)
                            print("IfZ _t"+str(self.temp_num)+' GoTo _L'+str(self.L)+';',file=fh)
                            self.temp_num+=1
                                
                        elif (x.token.string==keywords[3]): #else statement
                            print('L'+str(self.L)+':',file=fh)
                            self.L+=1
                            l=[]
                            for o in line:
                                l.append(o.token.string)
                            if ('%' in l):
                                i=0
                                for n in line:
                                    if (n.token.string=='%'):
                                        j=i
                                    i+=1 
                                var1=None
                                var2=None
                                for z in self.temp_var: #search for 2 variables and operation
                                    if (z[0] in l[j-1] and var1 is None):
                                        var1=z[1] 
                                    elif (z[0] in l[j+1] and var2 is None):
                                        var2=z[1] 
                                print("_t"+str(self.temp_num)+'='+var1+l[j]+var2+';',file=fh) #temp made for operation result
                                obj=[var1+'%'+var2,'_t'+str(self.temp_num)]
                                self.temp_var.append(obj)
                                self.temp_num+=1
                        elif (x.token.string=='return'):
                            found=0
                            i=0
                            for t in line:
                                if ('gcd'==t.token.string):
                                    found=1
                                    break 
                                if (t.token.string=='return'):
                                    j=i+2
                                i+=1
                            if not found:
                                print("Return "+line[j].token.string+';',file=fh)
                            
                    for u in line:
                        print(u.token.string) 
                    print('-----')
                    print(lines)
                    line=[]
                line.append(y)
        else:
            
            print("Zero errors needed to create IR")
        return
          
