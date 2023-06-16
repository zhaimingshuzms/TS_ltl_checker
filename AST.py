operators = [
    '!',
    '&',
    '|',
    '->',
    '<->',
    'X',
    'F',
    'G',
    'U',
    'R'
]

class ASTNode:
    @staticmethod
    def analyze(formula):
        global operators
        ret = []
        op = ''
        for sub in formula:
            if isinstance(sub,str) and sub in operators:
                op = sub
            else:
                ret.append(sub)

        # leaf special case
        if op == '':
            return '', []
        assert len(ret) <= 2
        return op, ret

    def __init__(self, formula):
        self.val = formula
        self.op, self.sub = ASTNode.analyze(self.val)

        if self.op == 'F':
            self.op = 'U'
            self.sub = [ASTNode(['True']), ASTNode(self.sub[0]) ]
        elif self.op == 'G':
            self.op = '!'
            self.sub = [ASTNode(['F',['!',self.sub[0]]])]
        else:
            self.sub = [ASTNode(i) for i in self.sub]
    
    def tostr(self):
        if self.op =='':
            return self.val[0]
        elif len(self.sub)==1:
            return '('+self.op + self.sub[0].tostr()+')'
        else:
            return '('+self.sub[0].tostr() + self.op + self.sub[1].tostr()+')'
        
    def __eq__(self, other):
        return self.val == other.val
    
    def __hash__(self):
        # not efficient but work
        return hash(self.tostr())
    
    def negation(self):
        #elementary !! dealing
        if self.val[0] == 'True':
            return ASTNode(['False'])
        elif self.val[0] == 'False':
            return ASTNode(['True'])
        elif self.op == '!':
            assert len(self.sub)==1
            return self.sub[0]
        else:
            return ASTNode(['!', self.val])
    
    def atomic(self):
        return self.op==''
    
class AST:
    def __init__(self, root:ASTNode):
        self.nodelist = []
        self.dfs(root)
    
    def dfs(self, node):
        self.nodelist.append(node)
        for sub in node.sub:
            self.dfs(sub)
    
    def generate_closure(self):
        negation_list = [i.negation() for i in self.nodelist]
        ret = self.nodelist + negation_list
        ret = list(set(ret))
        # print("closure :")
        # for i in ret:
        #     print(i.tostr())
        return ret