import numpy as np

class Node:
    """
    Class for a node from the tree created from search algorithms

    Attributes
    ---------

    graph : object matrix
        the main object of the node which holds the current position of the
        objects in the puzzle

    pai : Node
        the parent node of the current node

    depth : int
        depth of the node only used for limited Depth-First Search
    
    heur : int
        heuristic of the node for the Best Match Search algorith
    
    path : Node array
        array the holds the path from the current node to the root
        in order = [current node, it's parent, it's parent's parent,..., root]

    Methods
    -------

    setPath()
        sets the path from the node to the root
    
    setHeur(obj)
        sets the heuristic value of the node based on the objective
    
    printPath()
        prints the path from the root to the node
    
    checkExiste(Nodes)
        checks if the node is present in an array of nodes
    
    getIndex(Nodes)
        gets the position of the node in an array of nodes
    
    findX()
        finds the position of the movable object from the main object
        of the node
    """

    def __init__(self, graph, pai=-1, depth=-1, heur=-1, aval=-1, path=[]) -> None:
        """
        Parameters
        ----------

        graph : object matrix
            the main object of the node which holds the current position of the
            objects in the puzzle
        
        pai : Node
            the parent node of the current node (default is -1 for the root [no parent])
        
        depth : int
            depth of the node only used for limited Depth-First Search
            (default is -1 since only one algorithm uses it)
        
        heur : int
            heuristic of the node for the Best Match Search algorith
            (default is -1 since only one algorithm uses it)
        
        path : Node array
            array the holds the path from the current node to the root
            in order = [current node, it's parent, it's parent's parent,..., root]
            (default is an empty array)
        """

        self.graph = graph  # Constructor behavior...
        self.pai = pai
        self.depth = depth
        self.heur = heur
        self.aval = aval
        self.path = path

    def setPath(self):
        """
        Sets the path from the node in it's path attribute. Starts at the
        desired node, adds it to the path's array, then moves to the node's
        parent, adding each parent until it reaches the root where the parent
        is -1
        """

        Aux = self                              # Stores the current node in an auxiliary node
        while 1:                                # Loops infinitely
            self.path = [*self.path, Aux.graph] # Adds the auxiliary's main matrix to the node's path array
            if Aux.pai == -1:                   # If the auxiliary node is the root (without parent)...
                break                           # Stops the loop
            Aux = Aux.pai                       # If it isn't, changes the auxiliary node to it's parent

    def setHeur(self, obj):
        """
        Sets the heuristic of the current by comparing the node with the objective.
        The lower the better. Starts at row*columns and subtracts 1 for each object
        in the correct position except for the movable object

        Parameters
        ----------

        obj : object matrix
            objective matrix for the puzzle
        """

        heur = 0

        ### h1(n) ###
        lin = np.shape(self.graph)[0]                                           # Gets the number of rows...
        col = np.shape(self.graph)[1]                                           # And columns of the node's main graph
        h1 = lin*col - 1                                                        # Multiply the rows and columns and starts the node's heuristic value with it
        for i in range(lin):                                                    # Loops the node's rows...
            for j in range(col):                                                # And columns
                if(self.graph[i][j] != 'X') and (self.graph[i][j] == obj[i][j]):# If a not-'X' object is in the correct position...
                    h1 -= 1                                              # Decrements the node's heuristic value by 1

        ### h2(n) ###
        # NodeTemp = Node(obj)
        # Xcur = self.findX()
        # Xobj = NodeTemp.findX()
        # h2 = abs(Xcur[0]-Xobj[0]) + abs(Xcur[1]-Xobj[1])

        # heur = h1 + h2
        heur = h1
        self.heur = heur

    def setAval(self):
        self.aval = self.heur + self.depth

    def printPath(self):
        """
        Prints the path by looping backwards the node's path array and printing
        each node's main object
        """

        for i in range(len(self.path)-1, -1, -1):   # Loops the node's path backwards...
            print(self.path[i], '\n')               # Printing it's main matrix, and jumping a line to visual clearance

    def checkExiste(self, Nodes):
        """
        Checks if the current node is present in a node array.
        The getIndex() method could be used to do this job, but it was decided that
        using a "true or false" method would be simpler for some specific needs

        Parameters
        ----------

        Nodes : Node array
            array of nodes to check if the current node is present within

        Returns
        -------

        1 
            if the node is present

        0
            if the node is not present
        """

        for j in range(len(Nodes)):                     # Loops the array
            if (Nodes[j].graph == self.graph).all():    # If the main matrix of the array is the same as the node's...
                return 1                                # Returns 1 (true)
        return 0                                        # If it couldn't be found, returns 0 (false)

    def getIndex(self, Nodes):
        """
        Gets the index of the current node in a node array

        Parameters
        ----------

        Nodes : Node array
            array of nodes to get the index of the current node from

        Returns
        -------

        j : int
            the position index of the current node inside the array

        -1
            if the node could not be found in the array
        """
        
        for j in range(len(Nodes)):                     # Loops the array
            if (Nodes[j].graph == self.graph).all():    # If the main matrix of the array is the same as the node's...
                return j                                # Returns the position index
        return -1                                       # If it couldn't be found, returns -1

    def findX(self):
        """
        Finds the position index of the movable object inside the current
        node's main object

        Returns
        -------

        [i, j] : int array
            two position int array with the row (i) and column (j) of the movable object
        """

        for i in range(np.shape(self.graph)[0]):        # Loops all the node's main matrix' rows...
            for j in range(np.shape(self.graph)[1]):    # And columns
                if(self.graph[i][j] == 'X'):            # If the current position object is the 'X'...
                    return [i, j]                       # Returns it's position index
        return -1                                       # It shouldn't, but if it couldn't find the 'X', returns -1

def BFS(inicial, obj):
    """
    Breadth-First Search algorith, checks all nodes of the same depth before 
    checking further

    Parameters
    ----------

    inicial : object matrix
        initial positions of the puzzle matrix
    
    obj : object matrix
        objective positions of the puzzle matrix

    Returns
    -------

    [X, iter] : [Node, int]
        two positions array where X is the node with the objective and iter is 
        the number of iterations until it was found
    
    [[], iter] : [[], int]
        two positions array with an empty array in the first position as a fail
        indication, the second position indicates the number of iterations until
        the fail
    """

    X = Node(inicial)                                   # Creates a node based on the initial matrix called X
    Abertos = [X]                                       # Creates an array (Open) with all the visited, but not finished, nodes with X in it
    Fechados = []                                       # Creates an empty array (Closed) to store all finished nodes (nodes that already had all it's children
                                                        # checked)
    iter = 0                                            # Initiates the iteration counter
    while Abertos != []:                                # Keeps checking the nodes until there's no unfinished node left
        iter += 1                                       # Increments the iteration counter by 1
        X = Abertos[0]                                  # X receives the first unfinished node
        del Abertos[0]                                  # Removes the first node from the Open array
        if (X.graph == obj).all():                      # If the main matrix of X is the objective...
            X.setPath()                                 # Sets the node's path...
            return [X, iter]                            # ...and returns it
        else:                                           # If it's not the objective...
            Aux = geraFilhos(X)                         # Generates it's children and stores it in an auxiliary array
            FilhosX = []                                # Initiates the Children array as empty
            for i in range(len(Aux)):                   # Loops the auxiliary array
                FilhosX = [*FilhosX, Node(Aux[i], X)]   # Generate new nodes with the auxiliary array's matrix as the main matrix, and X as parent
            Fechados.append(X)                          # Adds X to the end of the Closed array
            for i in range(len(FilhosX)):               # Loops the Children array backwards
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):
                                                        # If the current child is in neither Open nor Closed...
                    Abertos = [*Abertos, FilhosX[i]]    # Adds the current child to the LAST position of the Open array
    return [[], iter]                                   # If it didn't succeeded, returns an empty array

def DFS(inicial, obj, lim=0):
    """
    (Limited) Depth-First Search algorith, checks a node, then that node's first 
    child and so on until there's no child node left to be generated, then goes
    back to the first node and checks it's next child on the list.
    If limit is set, it will only check until that limit depth

    Parameters
    ----------

    inicial : object matrix
        initial positions of the puzzle matrix
    
    obj : object matrix
        objective positions of the puzzle matrix
    
    lim : int
        depth limit. Will only deepen to this limit

    Returns
    -------

    [X, iter] : [Node, int]
        two positions array where X is the node with the objective and iter is 
        the number of iterations until it was found
    
    [[], iter] : [[], int]
        two positions array with an empty array in the first position as a fail
        indication, the second position indicates the number of iterations until
        the fail
    """

    depth = 0
    X = Node(inicial, depth=depth)                              # Creates a node based on the initial matrix called X with depth 0
    Abertos = [X]                                               # Creates an array (Open) with all the visited, but not finished, nodes with X in it
    Fechados = []                                               # Creates an empty array (Closed) to store all finished nodes (nodes that already had all it's
                                                                # children checked)
    iter = 0                                                    # Initiates the iteration counter
    while Abertos != []:                                        # Keeps checking the nodes until there's no unfinished node left
        iter += 1                                               # Increments the iteration counter by 1
        X = Abertos[0]                                          # X receives the first unfinished node
        del Abertos[0]                                          # Removes the first node from the Open array
        if (X.graph == obj).all():                              # If the main matrix of X is the objective...
            X.setPath()                                         # Sets the node's path...
            return [X, iter]                                    # ...and returns it
        elif X.depth < lim:                                     # If it's not the objective and it's below depth limit...
            Aux = geraFilhos(X)                                 # Generates it's children and stores it in an auxiliary array
            FilhosX = []                                        # Initiates the Children array as empty
            depth = X.depth + 1                                 # Makes the depth variable receive X's depth incremented by 1
            for i in range(len(Aux)):                           # Loops the auxiliary array
                FilhosX = [*FilhosX, Node(Aux[i], X, depth)]    # Generate new nodes with the auxiliary array's matrix as the main matrix, X as parent, and with
                                                                # incremented depth
            Fechados.append(X)                                  # Adds X to the end of the Closed array
            for i in range(len(FilhosX)-1,-1,-1):               # Loops the Children array backwards
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):
                                                                # If the current child is in neither Open nor Closed...
                    Abertos = [FilhosX[i], *Abertos]            # Adds the current child to the FIRST position of the Open array
    return [[], iter]                                           # If it didn't succeeded, returns an empty array

def BMS(inicial, obj):
    """
    Best Match Search algorith, from the root node, generates it's children,
    generates it's children heuristics, then checks the child with the best
    heuristic value until the objective is found

    Parameters
    ----------

    inicial : object matrix
        initial positions of the puzzle matrix
    
    obj : object matrix
        objective positions of the puzzle matrix

    Returns
    -------

    [X, iter] : [Node, int]
        two positions array where X is the node with the objective and iter is 
        the number of iterations until it was found
    
    [[], iter] : [[], int]
        two positions array with an empty array in the first position as a fail
        indication, the second position indicates the number of iterations until
        the fail
    """

    X = Node(inicial)                                                   # Creates a node based on the initial matrix called X
    Abertos = [X]                                                       # Creates an array (Open) with all the visited, but not finished, nodes with X in it
    Fechados = []                                                       # Creates an empty array (Closed) to store all finished nodes (nodes that already had all
                                                                        # it's children checked)
    iter = 0                                                            # Initiates the iteration counter
    while Abertos != []:                                                # Keeps checking the nodes until there's no unfinished node left
        iter += 1                                                       # Increments the iteration counter by 1
        X = Abertos[0]                                                  # X receives the first unfinished node
        del Abertos[0]                                                  # Removes the first node from the Open array
        if(X.graph == obj).all():                                       # If the main matrix of X is the objective...
            X.setPath()                                                 # Sets the node's path...
            return [X, iter]                                            # ...and returns it
        else:                                                           # If it's not the objective...
            Aux = geraFilhos(X)                                         # Generates it's children and stores it in an auxiliary array
            FilhosX = []                                                # Initiates the Children array as empty
            for i in range(len(Aux)):                                   # Loops the auxiliary array
                FilhosX = [*FilhosX, Node(Aux[i], X)]                   # Generate new nodes with the auxiliary array's matrix as the main matrix, and X as parent
            for i in range(len(FilhosX)):                               # Loops the Children array
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):  # If the current children is not in neither in Open nor Closed 
                                                                                                    # arrays...
                    FilhosX[i].setHeur(obj)                             # Sets that child's heuristic...
                    Abertos = insertionSort(Abertos, FilhosX[i], 0)     # And inserts it in the Open array, ordering it crescently by heuristic value
                 elif FilhosX[i].checkExiste(Abertos):                   # If it's in the Open array...
                     pos = FilhosX[i].getIndex(Abertos)                  # Gets it's position in the array...
                     if (len(FilhosX[i].path) < len(Abertos[pos].path)): # If the current child's path is shorter than the node in the Open array...
                         Abertos[pos] = FilhosX[i]                       # Swap them
                 elif FilhosX[i].checkExiste(Fechados):                  # If it's in the Closed array...
                     pos = FilhosX[i].getIndex(Fechados)                 # Gets it's position in the array...
                     if (len(FilhosX[i].path) < len(Fechados[pos].path)):# If it's path is shorter than the node currently inside the array...
                         del Fechados[pos]                               # Remove it from the Closed array...
                         Abertos = insertionSort(Abertos, FilhosX[i], 0) # And inserts it in the Open array, ordering it crescently by heuristic value
        Fechados = [*Fechados, X]                                       # After all this, inserts X in the end of the Closed array
    return [[], iter]                                                   # If it didn't succeeded, returns an empty array

def AST(inicial, obj):
    """
    Best Match Search algorith, from the root node, generates it's children,
    generates it's children heuristics, then checks the child with the best
    heuristic value until the objective is found

    Parameters
    ----------

    inicial : object matrix
        initial positions of the puzzle matrix
    
    obj : object matrix
        objective positions of the puzzle matrix

    Returns
    -------

    [X, iter] : [Node, int]
        two positions array where X is the node with the objective and iter is 
        the number of iterations until it was found
    
    [[], iter] : [[], int]
        two positions array with an empty array in the first position as a fail
        indication, the second position indicates the number of iterations until
        the fail
    """

    depth = 0
    X = Node(inicial, depth=depth)                                      # Creates a node based on the initial matrix called X
    X.setHeur(obj)
    X.setAval()
    Abertos = [X]                                                       # Creates an array (Open) with all the visited, but not finished, nodes with X in it
    Fechados = []                                                       # Creates an empty array (Closed) to store all finished nodes (nodes that already had all
                                                                        # it's children checked)
    iter = 0                                                            # Initiates the iteration counter
    while Abertos != []:                                                # Keeps checking the nodes until there's no unfinished node left
        iter += 1                                                       # Increments the iteration counter by 1
        X = Abertos[0]                                                  # X receives the first unfinished node
        del Abertos[0]                                                  # Removes the first node from the Open array
        if(X.graph == obj).all():                                       # If the main matrix of X is the objective...
            X.setPath()                                                 # Sets the node's path...
            print('\n------------------------------------\n')
            for i in range(len(Abertos)):
                print(Abertos[i].graph, Abertos[i].aval, '\n')
            print('\n------------------------------------\n')
            for i in range(len(Fechados)):
                print(Fechados[i].graph, Fechados[i].aval, '\n')
            return [X, iter]                                            # ...and returns it
        else:                                                           # If it's not the objective...
            Aux = geraFilhos(X)                                         # Generates it's children and stores it in an auxiliary array
            FilhosX = []                                                # Initiates the Children array as empty
            depth = X.depth + 1
            for i in range(len(Aux)):                                   # Loops the auxiliary array
                FilhosX = [*FilhosX, Node(Aux[i], X, depth=depth)]      # Generate new nodes with the auxiliary array's matrix as the main matrix, and X as parent
            for i in range(len(FilhosX)):                               # Loops the Children array
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):  # If the current children is not in neither in Open nor Closed 
                                                                                                    # arrays...
                    FilhosX[i].setHeur(obj)                             # Sets that child's heuristic...
                    FilhosX[i].setAval()
                    Abertos = insertionSort(Abertos, FilhosX[i], 1)     # And inserts it in the Open array, ordering it crescently by heuristic value
        Fechados = [*Fechados, X]                                       # After all this, inserts X in the end of the Closed array
    return [[], iter]                                                   # If it didn't succeeded, returns an empty array

def geraFilhos(Node):
    """
    Generates a node's children. This method specifically generates the children
    of a 8-puzzle by finding the 'X' (movable object), then swapping the 'X''s
    position with it's possible neighbours

    Parameters
    ----------

    Node : Node
        matrix of the current 8-puzzle matrix

    Returns
    -------

    Aux[2:4] : array of object arrays
        array from 2 to 4 positions containing all possible children
    """

    posX = Node.findX()                                             # Finds the 'X' index in the Node's matrix
    Aux = np.ndarray(shape=(4,np.shape(Node.graph)[0],np.shape(Node.graph)[1]), dtype=object)
                                                                    # Creates a 3D array of 4x3x3 (4 matrices) to store the node's children
    k = 0                                                           # Index to store the number of children generated
                                                                    # Will now generate the children by moving the 'X'
                                                                    # First will try to move to the left, then up, then right, then down
    if(posX[1]-1 >= 0):                                             # Checks if moving to the left is possible
        Aux[k] = Node.graph                                         # Stores the current node's matrix in the auxiliary array
        Aux[k][posX[0]][posX[1]-1] = Node.graph[posX[0]][posX[1]]   # Moves the 'X' to the left
        Aux[k][posX[0]][posX[1]] = Node.graph[posX[0]][posX[1]-1]   # Moves the number that was on the left, to the right
        k += 1                                                      # Increments the number of children
    if(posX[0]-1 >= 0):                                             # Same to up...
        Aux[k] = Node.graph
        Aux[k][posX[0]-1][posX[1]] = Node.graph[posX[0]][posX[1]]
        Aux[k][posX[0]][posX[1]] = Node.graph[posX[0]-1][posX[1]]
        k += 1
    if(posX[1]+1 <= np.shape(Node.graph)[1]-1):                     # Right...
        Aux[k] = Node.graph
        Aux[k][posX[0]][posX[1]+1] = Node.graph[posX[0]][posX[1]]
        Aux[k][posX[0]][posX[1]] = Node.graph[posX[0]][posX[1]+1]
        k += 1
    if(posX[0]+1 <= np.shape(Node.graph)[1]-1):                     # And down
        Aux[k] = Node.graph
        Aux[k][posX[0]+1][posX[1]] = Node.graph[posX[0]][posX[1]]
        Aux[k][posX[0]][posX[1]] = Node.graph[posX[0]+1][posX[1]]
        k += 1
    return Aux[0:k]                                                 # Returns an array of the size of the number of children generated containing said children

def insertionSort(A, ins, ind):
    """
    Inserts a node in a node array ordering crescently by heuristic if index is
    0, or by evaluation if index is 1
    """

    n = len(A)

    if ind == 0:
        for i in range(n):
            if A[i].heur > ins.heur:
                return [*A[0:i], ins, *A[i:n]]
    else:
        for i in range(n):
            if A[i].aval > ins.aval:
                return [*A[0:i], ins, *A[i:n]]
    return [*A, ins]

############################################################################## MAIN ###############################################################################

Obj = np.array([[1,  2 , 3],
                [8, 'X', 4],
                [7,  6 , 5]])   # Objective matrix

Ini = np.array([[2,  8 , 3],
                [1,  6 , 4],
                [7, 'X', 5]])   # Initial matrix

BFSres = BFS(Ini, Obj)          # Runs the BFS algorithm
print('\nBFS:', BFSres[1], 'iteracoes\n\n',BFSres[0].graph, '\n\nCAMINHO:\n')
                                # Prints the algorithm, result, iterations...
BFSres[0].printPath()           # ... and the path to the result

DFSres = DFS(Ini, Obj, 5)       # Same for DFS...
print('\nDFS:', DFSres[1], 'iteracoes\n\n',DFSres[0].graph, '\n\nCAMINHO:\n')
DFSres[0].printPath()

BMSres = BMS(Ini, Obj)          # BMS...
print('\nBusca Melhor Escolha:', BMSres[1], 'iteracoes\n\n',BMSres[0].graph, '\n\nCAMINHO:\n')
BMSres[0].printPath()

ASTres = AST(Ini, Obj)          # ... and for AST
print('\nA*:', ASTres[1], 'iteracoes\n\n',ASTres[0].graph, '\n\nCAMINHO:\n')
ASTres[0].printPath()
