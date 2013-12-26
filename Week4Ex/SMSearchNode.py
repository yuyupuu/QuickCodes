class SM:
    startState = None

    def getStartState(self):
        return self.startState
    
    def start(self):
        self.state = self.getStartState()
        
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

class KnightSM(SM):
    legalInputs = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]

    def __init__(self,boardX,boardY,initLoc):
        self.startState = initLoc
        self.boardX = boardX
        self.boardY = boardY

    def getNextValues(self,state,inp):
        x,y = state
        dx,dy = inp
        nx = x + dx
        ny = y + dy
        if 0<=nx<self.boardX and 0<=ny<self.boardY:
            newState = (nx,ny)
        else:
             #if move would take us outside the board, stay put
            newState = state
        return newState,newState

    def done(self,state):
        return state == (7,7)

##########################       
class SearchNode:
    def __init__(self,state,parent):
        self.parent = parent
        self.state = state

    def getPath(self):
        pathLst = []
        current = self
        while current is not None:
            pathLst = [current.state] + pathLst
            current = current.parent
        return pathLst

class Queue():
    def __init__(self):
        self.array = []
    def push(self, val):
        self.array.append(val)
    def pop(self):
        return self.array.pop(0)
    def isempty(self):
        return len(self.array) == 0
        
class Stack():
    def __init__(self):
        self.array = []
    def push(self, val):
        self.array.append(val)
    def pop(self):
        return self.array.pop()
    def isempty(self):
        return len(self.array) == 0

def search(startNode, goalTest, dfs=False):
    testBool = dfs
    if dfs == None:
        testBool == False
    if goalTest(startNode.state):
        return [startNode.state]
    if testBool:
        agenda = Stack()
    else:
        agenda = Queue()
        
    agenda.push(startNode)
    visited = [startNode.state];
    while not agenda.isempty():
        parent = agenda.pop()
        for child in parent.getChildren():
            if goalTest(child.state):
                return child.getPath()
            elif child.state not in visited:
                visited.append(child.state)
                agenda.push(child)
                continue
    return None

class SMSearchNode(SearchNode):
    def __init__(self,sm,state,parent=None):
        self.sm = sm
        SearchNode.__init__(self,state,parent)

    def getChildren(self):
        legalInp = self.sm.legalInputs
        childLst = []
        for i in legalInp:
            #print 'i: ' + str(i)
            (s,o) = self.sm.getNextValues(self.state,i)
            childLst.append(SMSearchNode(self.sm, o, self))
                #print [x.state for x in childLst]
        #print '-----------------------end getChildren'
        print 'FINAL:' + str([x.state for x in childLst])
        return childLst

def smSearch(sm):
    return search(SMSearchNode(sm,sm.startState,None),sm.done,False)
