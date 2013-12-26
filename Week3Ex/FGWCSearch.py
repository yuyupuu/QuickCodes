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

def isLegal(state):
    if state[0] == state[1] or state[1] != state[3] and state[1] != state[2]:
        return True
    else:
        return False
class FGWCSearchNode(SearchNode):
    def __init__(self,state, parent):
        self.state = state
        self.parent = parent
        
    def getChildren(self):
        childLst = []
        rlArr = ['R','L']
        currstate = [x for x in self.state]
        print "initial:" + str(currstate)
        for i in range(len(self.state)):
            if currstate[i] == self.state[0]:
                if currstate[i] == rlArr[0]:
                    currstate[i] = rlArr[1]
                    
                else:
                    currstate[i] = rlArr[0]

                print "i = " + str(i)
                print "currstate @ " + str(i) + ":" + str(currstate)
                    
                if currstate != self.state and isLegal(currstate):
                #ASK ABOUT THE CHANGING VALUES AND STUFFS!!!!
                    tupstate = (currstate[0],currstate[1],currstate[2],currstate[3])
                    childLst.append(FGWCSearchNode(tupstate,self))
                    print "valid child:" + str(currstate)
                    print "childLst:" + str([l.state for l in childLst])
                else:
                    print "invalid:" + str(currstate)
                    print "childLst:" + str([l.state for l in childLst])
                if i > 0:
                    currstate[i] = self.state[i]
        print "FINAL childLst:" + str([l.state for l in childLst])
        return childLst         

def goalTest(s):
    atGoal = True
    for i in range(len(s)):
        if s[i] == 'L':
            atGoal = False
    return atGoal

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
        
