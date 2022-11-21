def genStars (fileName):
    f = open(fileName, "r")
    n = len(f.readlines())
    f.seek(0)
    Stars = []
    for i in range(n):
        xyz = f.readline()
        [x, y, z] = xyz.split()
        Stars.append(Node(i, (float(x),float(y),float(z))))
    return Stars

def genChild(Stars, Open, Clsd):
    Child = []
    for i in range(len(Stars)):
        if not(Stars[i] in Open) and not(Stars[i] in Clsd):
            Child.append(Stars[i])
    return Child

class Node:
    """
    This class represents a node (possible index for Pacman)
    Parameters
    ----------
    index : (x:int,y:int)
        the position of the current node where x is the column and y is the row
    depth : int
        how many other nodes to reach the root. Default is -1 when unused
        (bfs and ucs)
    cost : float
        cost to reach this node, can be used to store the cost for ucs,
        or heuristic value for astar, making this the priority value,
        where the lower the better. Default is -1 when unused (dfs and bfs)
    fromRoot : list of Directions
        list containing the directions taken from the root to this node.
        Default is empty list for the root itself
    """

    def __init__(self, index, xyz, depth=0, cost=-1, fromRoot=0):
        self.index = index
        self.xyz = xyz
        self.depth = depth
        self.cost = cost
        self.fromRoot = fromRoot

    def __eq__(self, __o):
        """
        Makes possible for 'Node1 == Node2' or 'Node in List' comparisons
        by comparing only their indexes
        """

        return self.index == __o.index

    def __str__(self) -> str:
        return str(self.index) + " " + str(self.xyz)

    def getDist(self, parent):
        return ( (self.xyz[0] - parent.xyz[0])**2 + (self.xyz[1] - parent.xyz[1])**2 + (self.xyz[2] - parent.xyz[2])**2 )**0.5

    def isGoalindex(self):
        return (self.xyz == (0,0,0) and self.depth == 100)

    def getIndex(self, List):
        """
        Gets the index of the current node in a node list
        Parameters
        ----------
        List : Node list
            list of Nodes to get the index of the current node from
        Returns
        -------
        i : int
            the position index of the current node inside the list
        None
            if the node could not be found in the list
        """
        
        for i in range(len(List)):          # Loops the list
            if List[i].index == self.index: # If the index of the list's current position is the same as the node's...
                return i                    # Returns the current position
        return None                         # If it couldn't be found, returns None

    def insertionSort(self, List):
        """
        Inserts a node in a node list ordering crescently by cost
        Parameters
        ----------
        List : Node list
            list of Nodes to insert the new node in
        """

        for i in range(len(List)):          # Loops the List
            if List[i].cost > self.cost:    # If the cost of the node in the current position is higher than the cost of the new node
                List.insert(i, self)        # Inserts the new node on that position
                return                      # And breaks out of the function
        List.append(self)                   # If it didn't broke out, means that the cost of the new node is higher than all the nodes in the List,
                                            # so it just appends the node to end of the List

def breadthFirstSearch(Stars):
    """Search the shallowest List in the search tree first."""
    
    X = Stars[0]                                    # Creates the initial node
    X.index = -1
    Open = [X]                                      # Creates the Open list
    Clsd = []                                       # Creates the Closed list
    while Open != []:                               # Loops while Open isn't empty
        X = Open.pop(0)                                 # Pops the first element in Open and store it in X
        if X.isGoalindex():                # If X is the objective...
            return X.fromRoot                               # Returns its path
        else:                                           # Otherwise...
            Children = genChild(Stars, Open, Clsd)          # Generates it's children
            for i in range(len(Children)):                  # Loops the auxiliary list
                Children[i].fromRoot = X.fromRoot + Children[i].getDist # Creates the child Node with the new index and path, then adds it to list
            Clsd.append(X)                                  # Puts the parent in Closed
            for i in range(len(Children)):                  # Loops the Children list
                if not(Children[i] in Open) and not(Children[i] in Clsd):# If the current child is neither in Open nor in Closed
                    Open.append(Children[i])                        # Inserts the child at the END of the Open list
    return []                                       # Returns an empty list if it failed

def aStarSearch(problem, heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    depth = 0
    ini = problem.getStartindex()
    X = Node(ini,depth=depth,cost=heuristic(ini,problem))# Creates a node based on the initial index called X with a set depth and heuristic (cost)
    Open = [X]                                      # Creates the Open list
    Clsd = []                                       # Creates the Closed list
    while Open != []:                               # Loops while Open isn't empty
        X = Open.pop(0)                                 # Pops the first element in Open and store it in X
        depth = X.depth + 1                             # Makes the children's depth be their parent's depth + 1
        if problem.isGoalindex(X.index):                # If X is the objective
            return X.fromRoot                               # Returns its path
        else:                                           # Otherwise
            Aux = problem.getSuccessors(X.index)            # Generates it's children
            Children = []                                   # Initiates the Children list
            for i in range(len(Aux)):                       # Loops the auxiliary list
                path = []                                       # Initiates the path list
                for j in range(len(X.fromRoot)):                # Loops it's parent's path list
                    path.append(X.fromRoot[j])                      # Adds what's in the parent's path list to the newly created list
                path.append(Aux[i][1])                          # Inserts the path from the parent to the child at the end of the list
                Children.append(Node(Aux[i][0],depth=depth,cost=heuristic(Aux[i][0],problem)+depth,fromRoot=path))
                                                                # Creates the child Node with the new index, depth, cost and path, then adds it to list
                                                                # Note that the cost is the heuristic value + its depth. Since the algorithm prioritizes
                                                                # lower costs, shallower nodes will be prioritized as objective
            for i in range(len(Children)):                  # Loops the Children list
                if not(Children[i] in Open) and not(Children[i] in Clsd):# If the current child is neither in Open nor in Closed
                    Children[i].insertionSort(Open)                 # Inserts it in the Open list, ordering it crescently by cost
        Clsd.append(X)                                  # Then, inserts X at the end of the Closed list
    return []                                       # Returns an empty list if it failed

Stars = genStars("star10.xyz")
print(breadthFirstSearch(Stars))
