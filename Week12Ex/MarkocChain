class MarkovChain:
    def __init__(self, startDistribution,
                 transitionDistribution):
        self.startDistribution = startDistribution
        self.transitionDistribution = transitionDistribution  
        self.state = None
        
    def initialize(self):
        self.state = self.startDistribution.draw()

    def transition(self):
        self.state = self.transitionDistribution(self.state).draw()

    def stateSequenceProb(self, seq):
        self.initialize()
        prob = self.startDistribution.prob(seq[0])
        for s in range(len(seq)-1):
            currSt = state
            prob *= self.transitionDistribution(seq[s]).prob(seq[s+1])
        return prob

    def occupationProb(self, T):
        if T == 0:
            return self.startDistribution
        else:
            currstate = self.startDistribution
            currDict = {}
            for i in range(T):
                for key in self.startDistribution.support():
                    currDict[key] = 0 
                    for key2 in self.startDistribution.support():
                        currDict[key] += self.transitionDistribution(key).prob(key2)
            return currstate
