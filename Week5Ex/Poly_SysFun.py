class Polynomial:
    ## Intialize a polynomial with a list of coefficients.
    ## The coefficient list starts with the highest order term.
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.order = len(coeffs)-1            

    ## Return the coefficient of the x**i term
    def coeff(self,i):
        return self.coeffs[self.order - i]

    ## Return the value of this Polynomial evaluated at x=v
    def val(self, v):
        total = 0
        for i in range(self.order+1):
            total += self.coeff(i) * v**i
        return total

    ## Return the roots of this Polynomial
    def roots(self):
        if self.order > 2:
            print 'error, we do not take that order of polynomial'
        elif self.order == 2:
            a = self.coeffs[0]
            b = self.coeffs[1]
            c = self.coeffs[2]
            det = b**2 - 4*a*c

            if det < 0:
                print det
                return (complex((-b/(2*a)),  ((-det) ** (.5))/(2*a)), complex((-b/(2*a)),  -((-det) ** (.5))/(2*a)))
                
            else:
                return ((-b + det **(.5))/(2*a), (-b - det **(.5))/(2*a))
        else:
            a = self.coeffs[0]
            b = self.coeffs[1]
            return (-b/a)

    ## Add two polynomials, return a new Polynomial
    def add (self, other):
        
        if len(self.coeffs)>len(other.coeffs):
            shortPol = other
            longPol = self
        else:
            shortPol = self
            longPol = other
            
        addCoeff = [0 for x in range(longPol.order+1)]
        
        for i in range(longPol.order+1):
            ind = longPol.order - i
            if i <= shortPol.order:
                addCoeff[ind] = (self.coeff(i)+other.coeff(i))
            else:
                addCoeff[ind] = longPol.coeff(i)
            
        return Polynomial(addCoeff)
    ## Multiply two polynomials, return a new Polynomial
    def mul(self, other):
        mulCoeff = [0 for x in range(self.order+other.order+1)]
        
        for i in range(self.order+1):
            print 'i= ' + str(i)
            for j in range(other.order+1):
                print 'j= ' + str(j)
                print i+j
                print"self.order - i = " + str(self.order+1 - i)
                mulCoeff[i+j] += (self.coeff(i) * other.coeff(j))
        mulCoeff.reverse()    
        return Polynomial(mulCoeff)

    def __add__(self, other):
        #override the + operator so we can do things like p1+p2
        return self.add(other)

    def __mul__(self, other):
        #override the * operator so we can do things like p1*p2
        return self.mul(other)

    def __str__(self):
        coeffs = [self.coeff(i) for i in xrange(self.order,-1,-1)]
        return 'Polynomial(%r)' % coeffs
    
class SystemFunctional:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def poles(self):
        d = self.denominator.coeffs
        reverseCoeff = [d[len(d)-i-1] for i in range(len(d))]
        #d.reverse()
        revPol = Polynomial(reverseCoeff)
        return revPol.roots()

    def poleMagnitudes(self):
##        poleArr = poles(self)
##        magArr = poles
##        for i in range(len(poleArr)):
##            if type(poleArr[i]) == 'complex':
##                magArr[i] = 
##
        poleArr = self.poles()
        print poleArr
        return [abs(x) for x in poleArr]

    def dominantPole(self):
        poleArr = self.poleMagnitudes()
        polInit = self.poles()
        print 'poleArr' + str(poleArr)
        maxInd = 0
        for i in poleArr:
            if i > poleArr[maxInd]:
                maxInd = i

        maxPol = polInit[maxInd]
        return maxPol

def R():
    return SystemFunctional(Polynomial([1,0]),Polynomial([1]))
def Gain(k):
    return SystemFunctional(Polynomial([k]),Polynomial([1]))
def Cascade(sf1, sf2):
    num1 = sf1.numerator
    num2 = sf2.numerator
    d1 = sf1.denominator
    d2 = sf2.denominator
    numPol = num1.mul(num2)
    dPol = d1.mul(d2)
    return SystemFunctional(numPol,dPol)
def FeedbackAdd(sf1, sf2):
    num1 = sf1.numerator
    num2 = sf2.numerator
    d1 = sf1.denominator
    d2 = sf2.denominator
    numPol = num1.mul(d2)
    x = d1.mul(d2)
    y = Polynomial([-1]).mul(num1.mul(num2))
    dPol = x.add(y) 
    return SystemFunctional(numPol,dPol)

x = SystemFunctional(Polynomial([0.1,0,0]),Polynomial([0.2,-.96,1]))

S = 2
T = 0.1
D = 0.96
A0 = FeedbackAdd(Cascade(Gain(S),Cascade(Gain(T),Cascade(R(),Cascade(R(),FeedbackAdd(Gain(1),Cascade(R(),Gain(D))))))),Gain(-1))

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

class AneSM(SM):
    def __init__(self):
        self.startState = ((0,0),(0,0,0))
    def getNextValues(self,state,inp):
        output = 0.5*state[0][1] - 0.2*state[0][0] + 0.2 * state[1][0]
        nextState = ((state[0][1],output),(state[1][1],state[1][2],inp))
        return (nextState, output)
##      
##class repeat(SM):
##    def __init__(self, sm,n = None):
##        self.sm = sm
##        self.startState = (0,self.sm.startState)
##        self.n = n
##    def getNextValues(self, state, inp):
##        (nextVal, smO) = self.sm.getNextValues(state[1],inp)
##        nextState = (state[0]+1, nextVal)
##        output = smO
##        return (nextState,output)

a = AneSM()
print a.transduce([0.5 for i in range(100)])
