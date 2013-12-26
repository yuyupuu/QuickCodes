
WORDS = set([i.lower().strip() for i in open('words2.txt').readlines()])

def is_valid_word(word):
    return word in WORDS

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
    
class WordLadderSearchNode(SearchNode):
    def __init__(self,state, parent):
        self.state = state
        self.parent = parent
    def getChildren(self):
        children = []
        letters = string.ascii_lowercase
        for i in len(self.state):
            for j in letters:
                posschild = self.state.replace(i,j)
                if is_valid_word(posschild):
                    children.append(WordLadderSearchNode(posschild,self))
        return children
                
