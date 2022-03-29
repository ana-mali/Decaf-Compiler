'''
----------------------------------------
[Parser]
----------------------------------------
__updated__= "2022-03-23"
----------------------------------------
'''
class Parse_tree:
        """
        Functions used to utilize a structured tree from source code
        """
        def __init__(self,scopename):
            """
            Parameter:
                token - list
                variable name, type and attribute 
            """
            self.scopename=scopename
            self.head=None
            self.next=None
            self.symboltable=[]
#            self.previousscope=None