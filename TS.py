# Import necessary modules
from automaton import NBA
from utils import *

# Define a Transition System (TS) class
class TS:
    # Define the constructor method for the TS class
    def __init__(self, nstates, ntrans, I, act, AP, map, label):
        # Initialize instance variables
        self.nstates = nstates
        self.ntrans = ntrans
        self.I = I
        self.act = act
        self.AP = AP
        self.map = map
        self.label = label
        self.R = None
        self.U = None
        self.T = None
        self.V = None
        self.cycle_found = None
        self.F = None
        
    # Define a function to find the post set of a given state
    def Post(self, s):
        return [i for i in range(self.nstates) if self.map[s][i] != None]
    
    # Define a function to check for cycles starting at a given state
    def cycle_check(self, s):
        # Initialize the cycle_found flag to False
        cycle_found = False
        # Add the current state to the list of visited states and mark it as visited
        self.V.append(s)
        self.T[s] = True
        # Continue exploring states until there are no more states to explore or a cycle is found
        while len(self.V)>0 and not cycle_found:
            # Get the current state to explore
            s_ = self.V[-1]
            # Find the states that can be reached from the current state
            post = self.Post(s_)
            # Check if any of the reachable states are already in the visited states list
            if s in post:
                # A cycle has been found
                cycle_found = True
                # Add the starting state of the cycle to the visited states list
                self.V.append(s)
            else:
                complete = True
                # Add any unvisited states that can be reached from the current state to the visited states list
                for s2 in post:
                    if self.T.get(s2) == None:
                        self.V.append(s2)
                        self.T[s2] = True
                        complete = False
                # If all reachable states have been visited, remove the current state from the visited states list
                if complete:
                    self.V.pop()
        # Return whether or not a cycle was found
        return cycle_found
    
    # Define a function to find all states that can be reached from a given state and check if there is a cycle
    def reachable_cycle(self, s):
        # Add the starting state to the list of states to explore and mark it as visited
        self.U.append(s)
        self.R[s] = True
        # Continue exploring states until there are no more states to explore or a cycle is found
        while len(self.U)>0 and not self.cycle_found:
            # Get the current state to explore
            s_ = self.U[-1]
            # Find the states that can be reached from the current state
            post = self.Post(s_)
            complete = True
            # Add any unvisited states that can be reached from the current state to the list of states to explore
            for s2 in post:
                if self.R.get(s2) == None:
                    self.U.append(s2)
                    self.R[s2] = True
                    complete = False
            # If all reachable states have been visited, remove the current state from the list of states to explore
            if complete:
                self.U.pop()
                # If the starting state is an accepting state and a cycle has been found, check if the cycle is valid
                if s_ in self.F:
                    self.cycle_found = self.cycle_check(s_)

    # Define a function to perform a nested depth-first search to check for cycles in the graph
    def nested_dfs(self):
        # Initialize necessary instance variables
        self.R = {}
        self.U = []
        self.T = {}
        self.V = []
        self.cycle_found = False
        # Loop through all initial states and check if there are any cycles starting at those states
        for s in self.I:
            if self.R.get(s) == None:
                self.reachable_cycle(s)
            # print("After nested dfs",s,self.R)
            # If a cycle is found, return False
            if self.cycle_found:
                return False, self.U + self.V
        # If no cycles are found, return True
        return True
    
    # Define a function to return the name of the class
    @classmethod
    def class_name(cls):
        return cls.__name__
    
    # Define a function to print the edges of the TS
    def print_edge(self):
        cnt = 0
        print(f"{self.class_name()} edges:")
        for i in range(self.nstates):
            for j in range(self.nstates):
                if self.map[i][j]!=None:
                    cnt = cnt + 1
                print(self.map[i][j],end = ' ')
            print("cnt = ",cnt)

# Define a Product class that inherits from the TS class
class Product(TS):
    # Define the constructor method for the Product class
    def __init__(self, ts:TS, nba:NBA):
        # Initialize instance variables
        self.nstates = ts.nstates * nba.nstates
        self.nbastates = nba.nstates

        self.I = []
        # Loop through all initial states of the TS and the NBA and add any valid combinations to the initial states list
        for s in ts.I:
            # print("list_and",list_and(ts.label[s],nba.AP))
            for q in range(nba.nstates):
                test = False
                for q_ in nba.Q0:
                    if seteq(nba.map[q_][q],list_and(ts.label[s],nba.AP)):
                        test = True
                if test:
                    self.I.append(self.ind(s,q))
        
        self.act = ts.act
        
        self.map = [[None for i in range(self.nstates)] for j in range(self.nstates)]
        # Create the transition map for the product automaton by combining the transition maps for the TS and the NBA
        for s in range(ts.nstates):
            for t in range(ts.nstates):
                if ts.map[s][t] != None:
                    for q in range(nba.nstates):
                        for p in range(nba.nstates):
                            if seteq(nba.map[q][p],list_and(ts.label[t],nba.AP)):
                                self.map[self.ind(s,q)][self.ind(t,p)] = 1

        # Create the list of final states for the product automaton
        self.F = [self.ind(i,j) for i in range(ts.nstates) for j in nba.F]

    # Define a function to calculate the index of a state in the product automaton
    def ind(self, s, q):
        return s * self.nbastates + q
    
# Define a function to load a TS from a file
def load_ts(data_path, **kwargs):
    
    data = load_data(data_path)

    for i in range(len(data)):
        if i!=3:
            data[i]=[int(j) for j in data[i]]
    
    nstates = data[0][0]
    ntrans = data[0][1]
    if kwargs.get('I'):
        I = kwargs['I']
    else:
        I = data[1]
    
    act = data[2]
    AP = data[3]
    map = [[None for i in range(nstates)] for j in range(nstates)]
    for i in range(4,4+ntrans):
        map[data[i][0]][data[i][2]] = data[i][1]
    labels = []
    assert 4+ntrans+nstates == len(data)
    for i in range(4+ntrans,4+ntrans+nstates):
        if len(data[i])==1 and data[i][0]==-1:
            labels.append([-1])
        else:
            labels.append([AP[j] for j in data[i]])

    return TS(nstates, ntrans, I, act, AP, map, labels)

# If the script is run as the main program, load the TS from a file
if __name__ == "__main__":
    load_ts()