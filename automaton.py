from AST import ASTNode, AST
from utils import *

# Check if a candidate set of sub-formulas satisfies the consistency condition
def check_consistent(closure, candidate: list[ASTNode]):
    ret = True

    for item in closure:
        if item.op == '&':
            if not eq(item.sub[0] in candidate and item.sub[1] in candidate,item in candidate):
                ret = False
    
    for item in candidate:
        if not implies(True, item.negation() not in candidate):
            ret = False

    for item in closure:
        if not implies(item.val[0] == 'True', item in candidate):
            ret = False

    return ret

# Check if a candidate set of sub-formulas satisfies the local consistency condition
def check_locally_consistent(closure, candidate: list[ASTNode]):
    ret = True
    for item in closure:
        if item.op == 'U':
            if not implies(item.sub[1] in candidate, item in candidate):
                ret = False
            if not implies(item in candidate and item.sub[1] not in candidate,item.sub[0] in candidate):
                ret = False
    return ret

# Check if a candidate set of sub-formulas satisfies the maximality condition
def check_maximal(closure, candidate: list[ASTNode]):
    ret = True
    for item in closure:
        if not implies(item not in candidate,item.negation() in candidate):
            ret = False
    return ret

# Check if a candidate set of sub-formulas satisfies all three conditions: consistency, local consistency, and maximality
def check_elementary(closure, candidate):
    return check_consistent(closure, candidate) \
        and check_locally_consistent(closure, candidate) \
        and check_maximal(closure, candidate)

# Generate all elementary sets of sub-formulas of the closure of an LTL formula
def generate_elementary_sets(closure):
    total = len(closure)
    ret = []
    for binary_code in range(0,2**total):
        tmp = []
        for bit in range(0,total):
            if (binary_code >> bit) & 1 == 1:
                tmp.append(closure[bit])
        if check_elementary(closure, tmp):

            # print("---------------?")
            # for i in tmp:
            #     print(i.tostr())
            
            ret.append(tmp)
    return ret

# Return the set of atomic propositions of an LTL formula
def AP(B):
    return list(set([item.tostr() for item in B if item.atomic() and not item.isLiteralTrue()]))

# The `automaton` class represents a basic automaton with a fixed number of states, initial states, accepting states, transition function, and set of atomic propositions (`AP`).
class automaton:
    def __init__(self, nstates, Q0, F, map, AP):
        self.nstates = nstates
        self.Q0 = Q0
        self.F = F
        self.map = map
        self.AP = AP
    
    @classmethod
    def class_name(cls):
        return cls.__name__

    def print_edge(self):
        print(f"{self.class_name()} edges:")
        for i in range(self.nstates):
            for j in range(self.nstates):
                print(self.map[i][j],end = ' ')
            print('')

# The `GNBA` class represents a Generalized Non-deterministic Büchi Automaton (GNBA) constructed from an LTL formula.
class GNBA(automaton):
    def __init__(self, phi:ASTNode):
        self.closure = AST(phi).generate_closure()
        self.Q = generate_elementary_sets(self.closure)
        super().__init__(len(self.Q), None, None, None, None)
        self.Q0 = [self.ind(B) for B in self.Q if phi in B]
        self.F = []
        for item in self.closure:
            if item.op == 'U':
                self.F.append([self.ind(B) for B in self.Q if item not in B or item.sub[1] in B])
        
        self.map = [[None for i in range(len(self.Q))] for j in range(len(self.Q))]
        
        # Determine if there is an edge between two states based on the subset relation between the corresponding elementary sets
        for i in range(self.nstates):
            for j in range(self.nstates):
                if self.has_edge(i,j):
                    self.map[i][j] = AP(self.Q[i])
        self.AP = AP(self.closure)
    
    def has_edge(self, i, j):
        ret = True
        for item in self.closure:
            if item.op == 'X':
                if not eq(item in self.Q[i], item.sub[0] in self.Q[j]):
                    ret = False
        
            elif item.op == 'U':
                if not eq(item in self.Q[i], \
                          item.sub[1] in self.Q[i] or (item.sub[0] in self.Q[i] and item in self.Q[j])):
                    ret = False
        return ret
    
    def ind(self, B):
        return self.Q.index(B)
    
    # Convert to a Non-deterministic Büchi Automaton (NBA)
    def toNBA(self):
        n = self.nstates
        m = len(self.F)
        if m == 0:
            return NBA(n, self.Q0, range(n), self.map, self.AP) # care

        Qnum = n * m
        tmp_map = [[None for i in range(Qnum)] for j in range(Qnum)]
        for i in range(m):
            for j in range(n):
                for k in range(n):
                    if self.map[j][k] != None:
                        if self.Q[j] in self.F[i]:
                            tmp_map[i*n+j][(i+1)%m*n+k] = self.map[j][k]
                        else:
                            tmp_map[i*n+j][i*n+k] = self.map[j][k]
        return NBA(Qnum, self.Q0, self.F[0], tmp_map, self.AP)

class NBA(automaton):
     def __init__(self, nstates, Q0, F, map, AP):
        super().__init__(nstates, Q0, F, map, AP)