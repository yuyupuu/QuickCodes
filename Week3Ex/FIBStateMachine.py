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

class Fib(SM):
    def __init__(self):
        self.startState = None
        self.prevState = [0,1]
        self.count = 0
    def getNextValues(self, state, inp):
        if state == None:
            nextState = 0
            output = 0
        elif state == 0:
            nextState = 1
            output = 1
        elif self.count > 2:
            nextState = state + self.prevState[0]
            self.prevState[0] = self.prevState[1]
            self.prevState[1] = nextState
            output = state + nextState

        elif state == 1:
            nextState = 1
            output = 1

        self.count += 1
        return (nextState,output)
