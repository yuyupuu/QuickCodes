class SM:
    def start(self):
        self.state = self.startState
        
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

class CommentsSM(SM):
    startState = False

    def getNextValues(self, state, inp):
        nextVal = state
        if inp == '#':
            nextVal = True
        elif inp == '\n':
            nextVal = False
            
        if nextVal:
            output = inp
        else:
            output = None
        
        return (nextVal, output)
