import random

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


pc = [random.random() for i in range(3)]
p = Polynomial(pc)
ans = p.roots()

