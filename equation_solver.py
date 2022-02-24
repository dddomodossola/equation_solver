class polynomial():
    monomials = None
    def __init__(self):
        self.monomials = []
        
    def append(self, poli):
        if type(poli) in (list, tuple):
            for m in poli:
                self.append(m)
        elif type(poli) == polynomial:
            for m in poli.monomials:
                self.append(m)
        else:
            self.monomials.append(poli)

    def __mul__(self, other):
        res = polynomial()
        for m1 in self.monomials:
            if type(other) == monomial:
                res.append(m1*other)
            elif type(other) == polynomial:
                for m2 in other.monomials:
                    res.append(m1*m2)
            else:
                print("polynomial.__mul__ (%s) not implemented"%str(type(other)))
                raise NotImplementedError

        return res

    def __add__(self, other):
        if type(other) == monomial:
            p = polynomial()
            for m in self.monomials:
                p.append(m)
            p.append(other)
            return p
        elif type(other) == polynomial:
            p = polynomial()
            for m in self.monomials:
                p.append(m)
            for m in other.monomials:
                p = p + m
            return p
        else:
            print("polynomial.__add__ (%s) not implemented"%str(type(other)))
            raise NotImplementedError

    def __sub__(self, other):
        if type(other) == monomial:
            p = polynomial()
            for m in self.monomials:
                p.append(m)
            other.coefficient = -other.coefficient
            p.append(other)
            return p
        elif type(other) == polynomial:
            p = polynomial()
            for m in self.monomials:
                p.append(m)
            for m in other.monomials:
                p = p - m
            return p
        else:
            print("polynomial.__sub__(%s) not implemented"%str(type(other)))
            raise NotImplementedError
    
    def __pow__(self, n):
        #self.coefficient **= n
        #self.literal_part = self.literal_part * n
        p = self*self
        for i in range(0,n-1):
            p*=self
        return p

    def __truediv__(self, other):
        if type(other) == monomial:
            p = polynomial()
            for m in self.monomials:
                p.append(m/other)
            return p
        elif type(other) == polynomial:
            f = algebraic_fraction(self, other)
            return f
        else:
            print("polynomial.__truediv__(%s) not implemented"%str(type(other)))
            raise NotImplementedError

    def sort_by_variable(self, letter):
        self.monomials = [v for v in sorted(self.monomials, key=lambda item: item.degree_for_letter(letter), reverse=True)]
        for m in self.monomials:
            if type(m) == polynomial:
                m.sort_by_variable(letter)

    def replace(self, letter, other_poly):
        p = polynomial()
        print("n monomi:", len(self.monomials))
        for m1 in self.monomials:
            p.append(m1.replace(letter, other_poly))
   
        return p

    def sum_and_substract(self):
        p = polynomial()
        while len(self.monomials) > 0:
            res = self.monomials[0]
            del self.monomials[0]

            if type(res) == polynomial:
                res.sum_and_substract()

            else:
                ii = 0
                while ii < len(self.monomials):
                    if type(self.monomials[ii]) == polynomial:
                        ii+=1
                        continue

                    if res == self.monomials[ii]:
                        res += self.monomials[ii]
                        del self.monomials[ii]
                    else:
                        ii+=1
            p.append(res)
        
        for m in p.monomials:
            self.monomials.append(m)

    def __str__(self):
        self.sum_and_substract()
        res = ''
        res = ' '.join([str(x) for x in self.monomials])
        return res
        
    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.monomials)

    def degree(self):
        res = 0
        for m in self.monomials:
            res = max(res, len(m.literal_part))
        return res

    def degree_for_letter(self, letter):
        res = 0
        for m in self.monomials:
            res = max(res, m.degree_for_letter(letter))
        return res


class algebraic_fraction(polynomial):
    denominator = None
    def __init__(self, _numerator = None, _denominator = None):
        polynomial.__init__(self)
        if _numerator:
            self.append(_numerator)

        self.denominator = polynomial()
        if _denominator:
            self.denominator.append(_denominator)
        else:
            self.denominator.append(monomial(1,''))

    def __add__(self, other):
        print("algebraic_fraction.__add__(%s) not implemented"%str(type(other)))
        raise NotImplementedError
    
    def __sub__(self, other):
        print("algebraic_fraction.__sub__(%s) not implemented"%str(type(other)))
        raise NotImplementedError
    
    def __mul__(self, other):
        print("algebraic_fraction.__mul__(%s) not implemented"%str(type(other)))
        raise NotImplementedError
        
    def __truediv__(self, other):
        print("algebraic_fraction.__truediv__(%s) not implemented"%str(type(other)))
        raise NotImplementedError

    def __str__(self):
        #self.sum_and_substract()
        res = ''
        res = ' '.join([str(x) for x in self.monomials])
        if len(self.denominator) > 0:
            #if it is not a denominator 1
            if not (len(self.denominator) == 1 and (self.denominator.degree() == 0)  and (self.denominator.monomials[0].coefficient == 1)):
                res = '+(' + res + ')/(' + str(self.denominator) + ')'
        return res
        
    def __repr__(self):
        return str(self)

    def sort_by_variable(self, letter):
        polynomial.sort_by_variable(self, letter)
        polynomial.sort_by_variable(self.denominator, letter)
        
    def replace(self, letter, other_poly):
        n = polynomial.replace(self, letter, other_poly)
        d = polynomial.replace(self.denominator, letter, other_poly)
        return algebraic_fraction(n, d)

    def sum_and_substract(self):
        polynomial.sum_and_substract(self)
        polynomial.sum_and_substract(self.denominator)

    def degree_for_letter(self, letter):
        n = polynomial.degree_for_letter(self, letter)
        d = polynomial.degree_for_letter(self.denominator, letter)
        return max(n, d)


class monomial():
    coefficient = 0
    literal_part = None
    def __init__(self, c, l):
        self.coefficient = c
        self.literal_part = l

    def sort_literal_part(self):
        letters_aggregated = {}
        for l in self.literal_part:
            if not l in list(letters_aggregated.keys()):
                letters_aggregated[l] = ''    
            letters_aggregated[l] = letters_aggregated[l] + l
        self.literal_part = ''
        for k in sorted(list(letters_aggregated.keys())):
            self.literal_part += letters_aggregated[k]

    def __eq__(self, other):
        for l in self.literal_part:
            if not self.literal_part.count(l) == other.literal_part.count(l):
                return False
        for l in other.literal_part:
            if not self.literal_part.count(l) == other.literal_part.count(l):
                return False
        return True
    
    def __add__(self, other):
        if type(other) != monomial:
            return other + self

        #si puo' sommare solo quando la parte letterale e' uguale tra i due monomi
        if self == other:
            return monomial(self.coefficient + other.coefficient, self.literal_part)
        else:
            p = polynomial()
            p.append(self)
            p.append(other)
            return p

    def __sub__(self, other):
        if type(other) == polynomial:
            p = polynomial()
            p.append(self)
            return p-other

        if type(other) != monomial:
            print("monomial.__sub__(%s) not implemented"%str(type(other)))
            raise NotImplementedError
            
        #si puo' sottrarre solo quando la parte letterale e' uguale tra i due monomi
        if self == other:
            return monomial(self.coefficient - other.coefficient, self.literal_part)
        else:
            p = polynomial()
            p.append(self)
            other.coefficient = -other.coefficient
            p.append(other)
            return p
            
    def __mul__(self, other):
        if type(other) == polynomial:
            return other*self

        if type(other) != monomial:
            print("monomial.__mul__(%s) not implemented"%str(type(other)))
            raise NotImplementedError

        return monomial(self.coefficient * other.coefficient, self.literal_part + other.literal_part)

    def __pow__(self, n):
        #self.coefficient **= n
        #self.literal_part = self.literal_part * n
        return monomial(self.coefficient**n, self.literal_part * n)

    def __truediv__(self, other):
        if type(other) == polynomial:
            p = polynomial()
            p.append(self)
            return p/other

        if type(other) != monomial:
            print("monomial.__truediv__(%s) not implemented"%str(type(other)))
            raise NotImplementedError
        
        other_copy = monomial(other.coefficient, other.literal_part)

        cof = self.coefficient
        let = self.literal_part
        #self.coefficient /= other_copy.coefficient
        cof /= other_copy.coefficient
        for l in self.literal_part:
            #self.literal_part = self.literal_part.replace(l, '', other_copy.count(l))
            let = let.replace(l, '', other_copy.literal_part.count(l))
            other_copy.literal_part = other_copy.literal_part.replace(l, '')

        other_copy.coefficient = 1
        m = monomial(cof, let)
        if len(other_copy.literal_part)>0:
            f = algebraic_fraction(m, other_copy)
            return f
        return m

    def replace(self, letter, other):
        m_res = monomial(self.coefficient, self.literal_part.replace(letter, ''))

        if type(other) == monomial:
            for i in range(0,self.literal_part.count(letter)):
                m_res = m_res*other
            return m_res
        
        if type(other) == polynomial:
            for i in range(0,self.literal_part.count(letter)):
                m_res = m_res*other
            return m_res
        return self

    def __str__(self):
        self.sort_literal_part()
        
        if self.coefficient == 0:
            return ''
        sign = ('+' if self.coefficient>0 else '-')
        cof = str(abs(self.coefficient)) if self.coefficient != 1.0 else ''
        if self.coefficient == 1.0:
            if len(self.literal_part) < 1:
                cof = '1'
        return  sign + cof + '*' + '*'.join([c for c in self.literal_part])
    
    def __repr(self):
        return str(self)

    def degree(self, letter):
        return len(self.literal_part)

    def degree_for_letter(self, letter):
        return self.literal_part.count(letter)
        

p = monomial(1,'axxx') -monomial(0.5,'ax') + monomial(3,'axx')
print(p/monomial(-0.5,'ax'))

p = (monomial(2,"x") + monomial(1,"y") + monomial(1,"yy"))*monomial(-1,"y")/(monomial(1,'xy') + monomial(3,'yy') - monomial(1,'xx'))
p.sum_and_substract()
p.sort_by_variable('y')
print(p)
p.sort_by_variable('x')
print(p)

pc = polynomial()
#c = -X*X -Y*Y -a*X -b*Y
pc.append([ monomial(-1,"XX"), monomial(-1,"YY"), monomial(-1,"aX"), monomial(-1,"bY")])

pa = polynomial()
pa.append([ monomial(1,"aaBB") / monomial(1,"AA"), monomial(4,"bBC")/monomial(1,"AA"), monomial(-2, "abB")/monomial(1,"A"), monomial(4,"aC")/monomial(1,"A"), monomial(1,"bb"), monomial(-4,"c"), monomial(-4,"BBc")/monomial(1,"AA"), monomial(-4,"CC")/monomial(1,"AA")])
pa = pa.replace("c", pc) #+aaBB/AA -2abB/A +4aC/A +4BBa*X/AA +4a*X +4bBC/AA +bb +4X*X +4Y*Y +4b*Y +4BBX*X/AA +4BBY*Y/AA +4BBb*Y/AA -4CC/AA = 0 #equazione secondo grado calcoliamo il delta in a

pA = monomial(1,'a') - monomial(1,'o')
pa = pa.replace("A", pA)

print(pa)

#delta1a=BB/AA      
deltaa = monomial(1, 'BB') / monomial(1,'AA')
#delta1b=-2bB/A +4C/A +4BBX/AA +4X        
deltab = monomial(-2, 'bB') / monomial(1,'A') + monomial(4, 'C') / monomial(1,'A') + monomial(4, 'BBX') / monomial(1,'AA') + monomial(4,'X')
#delta1c=           +4bBC/AA                  +bb               +4X*X            +4Y*Y             +4b*Y             +4BBX*X/AA                            +4BBY*Y/AA                               +4BBb*Y/AA                          -4CC/AA
deltac = monomial(4, 'bBC') / monomial(1,'AA') + monomial(1,'bb') + monomial(4,'XX') + monomial(4,'YY') + monomial(4,'bY') + monomial(4,'BBXX') / monomial(1,'AA') + monomial(4,'BBYY') / monomial(1,'AA') + monomial(4,'BBbY') / monomial(1,'AA') -monomial(4,'CC') / monomial(1,'AA')
delta = deltab*deltab - monomial(4,'')*deltaa*deltac
#sol = (deltab*deltab - math.sqrt(delta))/(monomial(2,'')*deltaa)
#+aaRR/TT +4bRG/TT -2abR/T +4aG/T  +bb +4X*X +4Y*Y +4a*X +4b*Y +4RRX*X/TT +4RRY*Y/TT +4RRa*X/TT +4RRb*Y/TT -4GG/TT = 0
print(delta)
#+(+20.0AAAAAAAAAABBbb -80.0AAAAAAAAAABCb -160.0AAAAAAAABBBXb -160.0AAAAAAAABXb -80.0AAAAAAAAABXb +80.0AAAAAAAAAACC +320.0AAAAAAAABBCX +320.0AAAAAAAACX +160.0AAAAAAAAACX +320.0AAAAAABBBBXX +640.0AAAAAABBXX +320.0AAAAAAABBXX +320AAAAAAXX +320AAAAAAAXX +80AAAAAAAAXX -64.0AAAAAAAAAABBBCb -64.0AAAAAAAAAAABBBCb -16.0AAAAAAAAAAAABBBCb -16.0AAAAAAAAAAAABBbb -16.0AAAAAAAAAAAAABBbb -4.0AAAAAAAAAAAAAABBbb -64.0AAAAAAAAAAAABBXX -64.0AAAAAAAAAAAAABBXX -16.0AAAAAAAAAAAAAABBXX -64.0AAAAAAAAAAAABBYY -64.0AAAAAAAAAAAAABBYY -16.0AAAAAAAAAAAAAABBYY -64.0AAAAAAAAAAAABBYb -64.0AAAAAAAAAAAAABBYb -16.0AAAAAAAAAAAAAABBYb -64.0AAAAAAAAAABBBBXX -64.0AAAAAAAAAAABBBBXX -16.0AAAAAAAAAAAABBBBXX -128.0AAAAAAAABBBBYY -128.0AAAAAAAAABBBBYY -32.0AAAAAAAAAABBBBYY -192.0AAAAAABBBBYb -192.0AAAAAAABBBBYb -48.0AAAAAAAABBBBYb +256.0AAAABBCC +256.0AAAAABBCC +64.0AAAAAABBCC)/(+4AA +4AAA +6AAAA)
#+(+20.0AAAAAAAAAABBbb -80.0AAAAAAAAAABCb -160.0AAAAAAAABBBXb -160.0AAAAAAAABXb -80.0AAAAAAAAABXb +80.0AAAAAAAAAACC +320.0AAAAAAAABBCX +320.0AAAAAAAACX +160.0AAAAAAAAACX +320.0AAAAAABBBBXX +640.0AAAAAABBXX +320.0AAAAAAABBXX +320AAAAAAXX +320AAAAAAAXX +80AAAAAAAAXX -64.0AAAAAAAAAABBBCb -64.0AAAAAAAAAAABBBCb -16.0AAAAAAAAAAAABBBCb -16.0AAAAAAAAAAAABBbb -16.0AAAAAAAAAAAAABBbb -4.0AAAAAAAAAAAAAABBbb -64.0AAAAAAAAAAAABBXX -64.0AAAAAAAAAAAAABBXX -16.0AAAAAAAAAAAAAABBXX -64.0AAAAAAAAAAAABBYY -64.0AAAAAAAAAAAAABBYY -16.0AAAAAAAAAAAAAABBYY -64.0AAAAAAAAAAAABBYb -64.0AAAAAAAAAAAAABBYb -16.0AAAAAAAAAAAAAABBYb -64.0AAAAAAAAAABBBBXX -64.0AAAAAAAAAAABBBBXX -16.0AAAAAAAAAAAABBBBXX -128.0AAAAAAAABBBBYY -128.0AAAAAAAAABBBBYY -32.0AAAAAAAAAABBBBYY -192.0AAAAAABBBBYb -192.0AAAAAAABBBBYb -48.0AAAAAAAABBBBYb +256.0AAAABBCC +256.0AAAAABBCC +64.0AAAAAABBCC)/+2AA(+1 +2A +3AA)
#+(+10.0AAAAAAAABBbb -40.0AAAAAAAABCb -80.0AAAAAABBBXb -80.0AAAAAABXb -40.0AAAAAAABXb +40.0AAAAAAAACC +160.0AAAAAABBCX +160.0AAAAAACX +80.0AAAAAAACX +160.0AAAABBBBXX +320.0AAAABBXX +160.0AAAAABBXX +160AAAAXX +160AAAAAXX +40AAAAAAXX -32.0AAAAAAAABBBCb -32.0AAAAAAAAABBBCb -8.0AAAAAAAAAABBBCb -8.0AAAAAAAAAABBbb -8.0AAAAAAAAAAABBbb -2.0AAAAAAAAAAAABBbb -32.0AAAAAAAAAABBXX -32.0AAAAAAAAAAABBXX -8.0AAAAAAAAAAAABBXX -32.0AAAAAAAAAABBYY -32.0AAAAAAAAAAABBYY -8.0AAAAAAAAAAAABBYY -32.0AAAAAAAAAABBYb -32.0AAAAAAAAAAABBYb -8.0AAAAAAAAAAAABBYb -32.0AAAAAAAABBBBXX -32.0AAAAAAAAABBBBXX -8.0AAAAAAAAAABBBBXX -64.0AAAAAABBBBYY -64.0AAAAAAABBBBYY -16.0AAAAAAAABBBBYY -96.0AAAABBBBYb -96.0AAAAABBBBYb -24.0AAAAAABBBBYb +128.0AABBCC +128.0AAABBCC +32.0AAAABBCC)/(+1 +2A +3AA)





"""



Python 3.10.0 (tags/v3.10.0:b494f59, Oct  4 2021, 19:00:18) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
++(+aaBB)/(+AA) +(+4.0bBC)/(+AA) +(-2.0abB)/(+A) +(+4.0aC)/(+A) +bb +-4XX -4YY -4aX -4bY +(+-4.0BBXX -4.0BBYY -4.0BBaX -4.0BBbY)/(+AA) +(-4.0CC)/(+AA)
SyntaxError: invalid decimal literal
a = 1
b=2
c=3
A = 10
B = 20
C = 30
X = 100
Y = 200
++(+a*a*B*B)/(+A*A) +(+4.0*b*B*C)/(+A*A) +(-2.0*a*b*B)/(+A) +(+4.0*a*C)/(+A) +b*b ++4*X*X +4*Y*Y +4*a*X +4*b*Y +(++4.0*B*B*X*X +4.0*B*B*Y*Y +4.0*B*B*a*X +4.0*B*B*b*Y)/(+A*A) +(-4.0*C*C)/(+A*A)
1010024.0
+a*a*B*B/(A*A) -2*a*b*B/A +4*a*C/A +4*B*B*a*X/(A*A) +4a*X +4*b*B*C/(A*A) +b*b +4*X*X +4*Y*Y +4*b*Y +4*B*B*X*X/(A*A) +4*B*B*Y*Y/(A*A) +4*B*B*b*Y/(A*A) -4*C*C/(A*A)
SyntaxError: invalid decimal literal
+a*a*B*B/(A*A) -2*a*b*B/A +4*a*C/A +4*B*B*a*X/(A*A) +4*a*X +4*b*B*C/(A*A) +b*b +4*X*X +4*Y*Y +4*b*Y +4*B*B*X*X/(A*A) +4*B*B*Y*Y/(A*A) +4*B*B*b*Y/(A*A) -4*C*C/(A*A)
1010024.0
sorted('dac')
['a', 'c', 'd']
128/2
64.0
192/2
96.0
delta1a=B*B/(A*A)
delta1b=-2*b*B/A +4*C/A +4*B*B*X/(A*A) +4*X
delta1c=+4*b*B*C/(A*A) +b*b +4*X*X +4*Y*Y +4*b*Y +4*B*B*X*X/(A*A) +4*B*B*Y*Y/(A*A)
delta1b*delta1b - 4.0*delta1a*delta1c
-12010416.0
+(+10.0AAAAAAAABBbb -40.0AAAAAAAABCb -80.0AAAAAABBBXb -80.0AAAAAABXb -40.0AAAAAAABXb +40.0AAAAAAAACC +160.0AAAAAABBCX +160.0AAAAAACX +80.0AAAAAAACX +160.0AAAABBBBXX +320.0AAAABBXX +160.0AAAAABBXX +160AAAAXX +160AAAAAXX +40AAAAAAXX -32.0AAAAAAAABBBCb -32.0AAAAAAAAABBBCb -8.0AAAAAAAAAABBBCb -8.0AAAAAAAAAABBbb -8.0AAAAAAAAAAABBbb -2.0AAAAAAAAAAAABBbb -32.0AAAAAAAAAABBXX -32.0AAAAAAAAAAABBXX -8.0AAAAAAAAAAAABBXX -32.0AAAAAAAAAABBYY -32.0AAAAAAAAAAABBYY -8.0AAAAAAAAAAAABBYY -32.0AAAAAAAAAABBYb -32.0AAAAAAAAAAABBYb -8.0AAAAAAAAAAAABBYb -32.0AAAAAAAABBBBXX -32.0AAAAAAAAABBBBXX -8.0AAAAAAAAAABBBBXX -64.0AAAAAABBBBYY -64.0AAAAAAABBBBYY -16.0AAAAAAAABBBBYY -96.0AAAABBBBYb -96.0AAAAABBBBYb -24.0AAAAAABBBBYb +128.0AABBCC +128.0AAABBCC +32.0AAAABBCC)/(+2*A +3*A*A)

"""