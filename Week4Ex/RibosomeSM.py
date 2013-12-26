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

rnaToAminoAcid = {"UUU":"Phenylalanine", "UUC":"Phenylalanine", "UUA":"Leucine", 
    "UCU":"Serine", "UCC":"Serine", "UCA":"Serine", "UCG":"Serine",
    "UAU":"Tyrosine", "UAC":"Tyrosine", "UAA":"STOP", "UAG":"STOP",
    "UGU":"Cysteine", "UGC":"Cysteine", "UGA":"STOP", "UGG":"Tryptophan",
    "CUU":"Leucine", "CUC":"Leucine", "CUA":"Leucine", "CUG":"Leucine",
    "CCU":"Proline", "CCC":"Proline", "CCA":"Proline", "CCG":"Proline",
    "CAU":"Histidine", "CAC":"Histidine", "CAA":"Glutamine", "CAG":"Glutamine",
    "CGU":"Arginine", "CGC":"Arginine", "CGA":"Arginine", "CGG":"Arginine",
    "AUU":"Isoleucine", "AUC":"Isoleucine", "AUA":"Isoleucine", "AUG":"Methionine",
    "ACU":"Threonine", "ACC":"Threonine", "ACA":"Threonine", "ACG":"Threonine",
    "AAU":"Asparagine", "AAC":"Asparagine", "AAA":"Lysine", "AAG":"Lysine",
    "AGU":"Serine", "AGC":"Serine", "AGA":"Arginine", "AGG":"Arginine",
    "GUU":"Valine", "GUC":"Valine", "GUA":"Valine", "GUG":"Valine",
    "GCU":"Alanine", "GCC":"Alanine", "GCA":"Alanine", "GCG":"Alanine",
    "GAU":"Aspartic Acid", "GAC":"Aspartic Acid", "GAA":"Glutamic Acid", 
    "GAG":"Glutamic Acid", "UUG":"Leucine",
    "GGU":"Glycine", "GGC":"Glycine", "GGA":"Glycine", "GGG":"Glycine",}



class RibosomeSM(SM):
    def __init__(self):
        self.startState = (1,('G','G','G'),False)

    def getNextValues(self,state,inp):
        ind = state[0]
        amBool = state[2]
        codon = state[1][0] + state[1][1] + state[1][2] #should be a string
        
        if amBool and ind %3 == 0:
            ind += 1          
            if rnaToAminoAcid[codon] == 'STOP':
                amBool = False
                output = None
                print 'END'
            else:
                output = rnaToAminoAcid[codon]

        elif amBool:
            ind += 1
            output = None
        else:
            if codon == 'AUG':
                ind = 1
                amBool = True
                output = rnaToAminoAcid[codon]
                print 'START'
            else:
                output = None
        
        print 'codon' + str(codon)
        print 'ind = ' + str(ind)
        nxtState = (ind,(state[1][1],state[1][2], inp),amBool)
        return (nxtState, output)

testSeq = 'ACCGGUCGCCACCAUGGUGAGCAAGGGCGAGGAGCUGUAGCCGGACGUAACGUU'
result = RibosomeSM().transduce(testSeq)
print [i for i in result if i is not None]
##class isAminoSM(RibosomeSM):
##    def getNextValues(self,state,inp):
##        
##
##class isNoneSM(RibosomeSM):
##    
