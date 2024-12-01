from field_element import FieldElement
from polyfield_element import PolyFieldElement
from utils.bitops import decode_base64, encode_base64
import random

def ddf(f): 
    q = 2**128
    z = []
    d = 1 

    fstar = f.copy()

    X = PolyFieldElement([FieldElement(0), FieldElement(1)])

    while len(fstar.coefficients) >= 2 * d:
        
        h = X.powmod(q**d, fstar) + X.powmod(1,fstar)
        
        g = PolyFieldElement.gcd(h, fstar)
        
        if not g.is_one(): 
            z.append((g,d))
            fstar = fstar // g
        d+=1
    
    if not fstar.is_one():
        z.append((fstar,len(fstar.coefficients)-1))
    
    elif len(z) == 0:
        z.append((f,1))
    
    
    return sorted(z)



def edf(f, d):
    q = 2 ** 128
    n = (len(f.coefficients)-1) / d
    z = [ f ]
    while len(z) < n:
        h = random_poly(len(f.coefficients)-1)
        g = h.powmod((((q** d) - 1)  // 3), f) + PolyFieldElement([FieldElement(1)]).powmod(1, f)

        for u in z:
            if len(u.coefficients)-1 > d:
                j = PolyFieldElement.gcd(u, g)
                if not j.is_one() and (j != u):
                    # u is factored
                    z.remove(u)
                    z.append(j)
                    z.append(u // j)
    return sorted(z)


def random_poly(max_deg):
    rand_poly = []

    deg = random.randint(1, max_deg-1)
    for i in range (deg):
        poly = FieldElement(random.randint(1, 2**128))
        rand_poly.append(poly)
    
    return PolyFieldElement(rand_poly)




def sff(f):
        """
        Implementiert den Square-Free Factorization Algorithmus (SFF) im Galois-Feld GF(2^m).
        """
        # Berechne c = gcd(f, f')
        f_prime = f.differentiate()
        
        c = PolyFieldElement.gcd(f, f_prime)
        # f ← f / c
        
        f = f // c
        
        # Initialisiere z ← ∅ und e ← 1
        z = []
        e = 1
        
        # while f ≠ 1 do
        while not f.is_one():
            
            # y ← gcd(f, c)
            y = PolyFieldElement.gcd(f, c)
            # if f ≠ y then
            if f != y:
                # z ← z ∪ {(f / y, e)}
                z.append((f // y, e))
            # f ← y
            f = y
            # c ← c / y
            c = c // y
            # e ← e + 1
            e += 1

        
        # if c ≠ 1 then
        if not c.is_one():
            for f_star, e_star in sff(c.sqrt()):
                # z ← z ∪ {(f*, 2e*)}
                z.append((f_star, e_star*2))

        # return z
        return sorted(z)