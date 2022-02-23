class polinomio():
    monomi_numeratore = None
    monomi_denominatore = None
    def __init__(self):
        self.monomi_numeratore = []
        self.monomi_denominatore = []
        #self.append_denominator(monomio(1,''))
        
    def append_numerator(self, poli):
        if type(poli) in (list, tuple):
            for m in poli:
                self.monomi_numeratore.append(m)
        else:
            self.monomi_numeratore.append(poli)

    def append_denominator(self, poli):
        if type(poli) in (list, tuple):
            for m in poli:
                self.monomi_denominatore.append(m)
        else:
            self.monomi_denominatore.append(poli)
            
    def __mul__(self, other):
        res = polinomio()
        for m1 in self.monomi_numeratore:
            if type(other) == monomio:
                res.append_numerator(m1*other)
            else:
                for m2 in other.monomi_numeratore:
                    res.append_numerator(m1*m2)
        
        for m1 in self.monomi_denominatore:
            if type(other) == polinomio:
                for m2 in other.monomi_denominatore:
                    res.append_denominator(m1*m2)
            else:
                res.append_denominator(m1)
        return res

    def __add__(self, other):
        if type(other) == monomio:
            p = polinomio()
            for m in self.monomi_numeratore:
                p.append_numerator(m)
            #p.monomi_numeratore.append(other)
            for m in self.monomi_denominatore:
                p.monomi_numeratore.append(m*other)
            for m in self.monomi_denominatore:
                p.append_denominator(m)
            return p
        else: #other is polinomio
            p = polinomio()
            for m in self.monomi_numeratore:
                for d in other.monomi_denominatore:
                    p.append_numerator(m*d)
            for m in other.monomi_numeratore:
                for d in self.monomi_denominatore:
                    p.append_numerator(m*d)
            for d in self.monomi_denominatore:
                p.append_denominator(d)
            for d in other.monomi_denominatore:
                p.append_denominator(d)
            return p

    def __sub__(self, other):
        if type(other) == monomio:
            p = polinomio()
            m.coefficiente = -m.coefficiente
            for m in self.monomi_numeratore:
                p.append_numerator(m)
            #p.monomi_numeratore.append(other)
            for m in self.monomi_denominatore:
                p.monomi_numeratore.append(m*other)
            for m in self.monomi_denominatore:
                p.append_denominator(m)
            return p
        else: #other is polinomio
            p = polinomio()
            for m in self.monomi_numeratore:
                for d in other.monomi_denominatore:
                    p.append_numerator(m*d)
            for m in other.monomi_numeratore:
                for d in self.monomi_denominatore:
                    dd = m*d
                    dd.coefficient = - dd.coefficient
                    p.append_numerator(dd)
            for d in self.monomi_denominatore:
                p.append_denominator(d)
            for d in other.monomi_denominatore:
                p.append_denominator(d)
            return p

    def __pow__(self, n):
        #self.coefficient **= n
        #self.letteral_part = self.letteral_part * n
        p = self*self
        for i in range(0,n):
            p*=self
        return p

    def __truediv__(self, other):
        #print("polinomio.__truediv__ NOT IMPLEMENTED")
        p = polinomio()
        if type(other) == monomio:
            numerator = monomio(1.0, '')
            p.append_numerator(numerator)
            p.append_denominator(other)
            return self*p
        
        else: #other is polinomio
            for m in other.monomi_numeratore:
                p.append_denominator(m)
            for m in other.monomi_denominatore:
                p.append_numerator(m)
            return self*p

    def replace(self, letter, other_poly):
        p = polinomio()
        print("n monomi:", len(self.monomi_numeratore))
        for m1 in self.monomi_numeratore:
            #if type(m1) == polinomio:
            #    p.append_numerator(m1.replace(letter, other_poly))
            #else:
            p.append_numerator(m1.replace(letter, other_poly))
        for m1 in self.monomi_denominatore:
            p.append_denominator(m1.replace(letter, other_poly))
            #else:
            #    p.append_denominator(ml.replace(letter, other_poly))
                        
        return p

    def sum_and_substract(self):
        p = polinomio()
        while len(self.monomi_numeratore) > 0:
            res = self.monomi_numeratore[0]
            del self.monomi_numeratore[0]

            if type(res) == polinomio:
                res.sum_and_substract()

            else:
                ii = 0
                while ii < len(self.monomi_numeratore):
                    if type(self.monomi_numeratore[ii]) == polinomio:
                        ii+=1
                        continue

                    if res == self.monomi_numeratore[ii]:
                        res += self.monomi_numeratore[ii]
                        del self.monomi_numeratore[ii]
                    else:
                        ii+=1
            p.append_numerator(res)

        while len(self.monomi_denominatore) > 0:
            res = self.monomi_denominatore[0]
            del self.monomi_denominatore[0]

            if type(res) == polinomio:
                res.sum_and_substract()

            else:
                ii = 0
                while ii < len(self.monomi_denominatore):
                    if type(self.monomi_denominatore[ii]) == polinomio:
                        ii+=1
                        continue
                    
                    if res == self.monomi_denominatore[ii]:
                        res += self.monomi_denominatore[ii]
                        del self.monomi_denominatore[ii]
                    else:
                        ii+=1
            p.append_denominator(res)
        
        for m in p.monomi_numeratore:
            self.monomi_numeratore.append(m)
        for m in p.monomi_denominatore:
            self.monomi_denominatore.append(m) 


    def __str__(self):
        self.sum_and_substract()
        res = ''
        res = ' '.join([str(x) for x in self.monomi_numeratore])
        if len(self.monomi_denominatore) > 0:
            res = '(' + res + ')/(' + ' '.join([str(x) for x in self.monomi_denominatore]) + ')'
        return '+' + res
        
    def __repr__(self):
        return str(self)
                
        
class monomio():
    coefficient = 0
    letteral_part = None
    def __init__(self, c, l):
        self.coefficient = c
        self.letteral_part = l

    def sort_letteral_part(self):
        letters_aggregated = {}
        for l in self.letteral_part:
            if not l in list(letters_aggregated.keys()):
                letters_aggregated[l] = ''    
            letters_aggregated[l] = letters_aggregated[l] + l
        self.letteral_part = ''
        for k in sorted(list(letters_aggregated.keys())):
            self.letteral_part += letters_aggregated[k]

    def __eq__(self, other):
        for l in self.letteral_part:
            if not self.letteral_part.count(l) == other.letteral_part.count(l):
                return False
        for l in other.letteral_part:
            if not self.letteral_part.count(l) == other.letteral_part.count(l):
                return False
        return True
    
    def __add__(self, other):
        if type(other) == polinomio:
            return other + self

        #si puo' sommare solo quando la parte letterale e' uguale tra i due monomi
        if self == other:
            #self.coefficient += other.coefficient
            return monomio(self.coefficient + other.coefficient, self.letteral_part)
        else:
            p = polinomio()
            p.append_numerator(self)
            p.append_numerator(other)
            return p

    def __sub__(self, other):
        if type(other) == polinomio:
            return other - self
            
        #si puo' sottrarre solo quando la parte letterale e' uguale tra i due monomi
        if self == other:
            #self.coefficient -= other.coefficient
            return monomio(self.coefficient - other.coefficient, self.letteral_part)
        else:
            p = polinomio()
            p.append_numerator(self)
            p.append_numerator(other)
            return p
            
    def __mul__(self, other):
        if type(other) == polinomio:
            p = polinomio()
            for m in other.monomi_numeratore:
                p.append_numerator(self*m)
            for m in other.monomi_denominatore:
                p.append_denominator(m)
            return p
        #self.coefficient *= other.coefficient
        #self.letteral_part += other.letteral_part
        return monomio(self.coefficient * other.coefficient, self.letteral_part + other.letteral_part)

    def __pow__(self, n):
        #self.coefficient **= n
        #self.letteral_part = self.letteral_part * n
        return monomio(self.coefficient**n, self.letteral_part * n)

    def __truediv__(self, other):
        if type(other) == polinomio:
            p = polinomio()
            for m in other.monomi_numeratore:
                p.append_denomiator(m)
            for m in other.monomi_denominatore:
                p.append_numerator(self*m)
            return p
        
        cof = self.coefficient
        let = self.letteral_part
        #self.coefficient /= other.coefficient
        cof /= other.coefficient
        for l in self.letteral_part:
            #self.letteral_part = self.letteral_part.replace(l, '', other.count(l))
            let = let.replace(l, '', other.letteral_part.count(l))
            other.letteral_part = other.letteral_part.replace(l, '')

        other.coefficient = 1
        m = monomio(cof, let)
        if len(other.letteral_part)>0:
            p = polinomio()
            p.append_numerator(m)
            p.append_denominator(other)
            return p
        return m

    def replace(self, letter, other):
        m_res = monomio(self.coefficient, self.letteral_part.replace(letter, ''))

        if type(other) == monomio:
            for i in range(0,self.letteral_part.count(letter)):
                m_res = m_res*other
            return m_res
        
        if type(other) == polinomio:
            for i in range(0,self.letteral_part.count(letter)):
                m_res = m_res*other
            return m_res
        return self

    def __str__(self):
        self.sort_letteral_part()
        
        if self.coefficient == 0:
            return ''
        sign = ('+' if self.coefficient>0 else '-')
        cof = str(abs(self.coefficient)) if self.coefficient != 1.0 else ''
        if self.coefficient == 1.0:
            if len(self.letteral_part) < 1:
                cof = '1'
        return  sign + cof + '*' + '*'.join([c for c in self.letteral_part])
    
    def __repr(self):
        return str(self)
        

p = (monomio(2,"x") + monomio(1,"y"))*monomio(-1,"y")
p.sum_and_substract()
print(p)

pc = polinomio()
#c = -X*X -Y*Y -a*X -b*Y
pc.append_numerator([ monomio(-1,"XX"), monomio(-1,"YY"), monomio(-1,"aX"), monomio(-1,"bY")])

pa = polinomio()
pa.append_numerator([ monomio(1,"aaBB") / monomio(1,"AA"), monomio(4,"bBC")/monomio(1,"AA"), monomio(-2, "abB")/monomio(1,"A"), monomio(4,"aC")/monomio(1,"A"), monomio(1,"bb"), monomio(-4,"c"), monomio(-4,"BBc")/monomio(1,"AA"), monomio(-4,"CC")/monomio(1,"AA")])
pa = pa.replace("c", pc) #+aaBB/AA -2abB/A +4aC/A +4BBa*X/AA +4a*X +4bBC/AA +bb +4X*X +4Y*Y +4b*Y +4BBX*X/AA +4BBY*Y/AA +4BBb*Y/AA -4CC/AA = 0 #equazione secondo grado calcoliamo il delta in a


#delta1a=BB/AA      
deltaa = monomio(1, 'BB') / monomio(1,'AA')
#delta1b=-2bB/A +4C/A +4BBX/AA +4X        
deltab = monomio(-2, 'bB') / monomio(1,'A') + monomio(4, 'C') / monomio(1,'A') + monomio(4, 'BBX') / monomio(1,'AA') + monomio(4,'X')
#delta1c=           +4bBC/AA                  +bb               +4X*X            +4Y*Y             +4b*Y             +4BBX*X/AA                            +4BBY*Y/AA                               +4BBb*Y/AA                          -4CC/AA
deltac = monomio(4, 'bBC') / monomio(1,'AA') + monomio(1,'bb') + monomio(4,'XX') + monomio(4,'YY') + monomio(4,'bY') + monomio(4,'BBXX') / monomio(1,'AA') + monomio(4,'BBYY') / monomio(1,'AA') + monomio(4,'BBbY') / monomio(1,'AA') -monomio(4,'CC') / monomio(1,'AA')
delta = deltab*deltab - monomio(4,'')*deltaa*deltac
#sol = (deltab*deltab - math.sqrt(delta))/(monomio(2,'')*deltaa)
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