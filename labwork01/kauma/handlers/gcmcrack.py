from field_element import FieldElement
from polyfield_element import PolyFieldElement
from utils.bitops import *
import random
from handlers.gfpolyops import *
from handlers.gcm import *

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
    n = (len(f.coefficients)-1) // d
    z = [ f ]

    while len(z) < n:
       
        h = random_poly(len(f.coefficients)-1)
        g = h.powmod((((q** d) - 1)  // 3), f) + PolyFieldElement([FieldElement(1)]).powmod(1, f)

        for u in z:
            if  len(u.coefficients) - 1 > d:
                j = PolyFieldElement.gcd(u, g)
            
                if not j.is_one() and (j != u):
                    z.remove(u)
                    z.append(j)
                    z.append(u // j)
    return sorted(z)


def random_poly(max_deg):
    
    rand_poly = []
    deg = random.randint(1, max_deg-1)
    for i in range (deg):
        poly = FieldElement(random.randint(1, (2**128)))
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



def gcm_crack(arguments):
    # Extrahiere und dekodiere den Nonce
    nonce = FieldElement.gcm_from_block(decode_base64(arguments.get("nonce")))

    # Extrahiere m1
    c1 = decode_base64(arguments["m1"]["ciphertext"])
    ad1 = decode_base64(arguments["m1"]["associated_data"])
    tag1 = decode_base64(arguments["m1"]["tag"])
    c1_org = [c1[i:i + 16] for i in range(0, len(c1), 16)]
    ad1_org = [ad1[i:i + 16] for i in range(0, len(ad1), 16)]


    # Extrahiere m2
    c2 = decode_base64(arguments["m2"]["ciphertext"])
    ad2 = decode_base64(arguments["m2"]["associated_data"])
    tag2 = decode_base64(arguments["m2"]["tag"])



    # Extrahiere m3
    c3 = decode_base64(arguments["m3"]["ciphertext"])
    ad3 = decode_base64(arguments["m3"]["associated_data"])
    tag3 = decode_base64(arguments["m3"]["tag"])

    c3_org = [c3[i:i + 16] for i in range(0, len(c3), 16)]
    ad3_org = [ad3[i:i + 16] for i in range(0, len(ad3), 16)]


    # Extrahiere Forgery
    cf = decode_base64(arguments["forgery"]["ciphertext"])
    adf = decode_base64(arguments["forgery"]["associated_data"])

    cf_org = [cf[i:i + 16] for i in range(0, len(cf), 16)]
    adf_org = [adf[i:i + 16] for i in range(0, len(adf), 16)]

    # GHASH-Polynom berechnen (T1 ⊕ T2 = GHASH Diff)
    # GHASH-Polynom berechnen

    L1 = (len(ad1) * 8).to_bytes(8, byteorder='big') + (len(c1) * 8).to_bytes(8, byteorder='big')
    L2 = (len(ad2) * 8).to_bytes(8, byteorder='big') + (len(c2) * 8).to_bytes(8, byteorder='big')
    L3 = (len(ad3) * 8).to_bytes(8, byteorder='big') + (len(c3) * 8).to_bytes(8, byteorder='big')
    LF = (len(adf) * 8).to_bytes(8, byteorder='big') + (len(cf) * 8).to_bytes(8, byteorder='big')

    while len(c1) % 16 != 0:
        c1 += b'\x00' 

    
    while len(c2) % 16 != 0:
        c2 += b'\x00'
        
    while len(ad1) % 16 != 0:
        ad1 += b'\x00'
    
    while len(ad2) % 16 != 0:
        ad2 += b'\x00'
    
    m1 = ad1 + c1 + L1 + tag1

    m2 = ad2 + c2 + L2 + tag2

    len_m1 = len(m1)

    len_m2 = len(m2)

    max_len = max(len(m1), len(m2))

    m1_padded = b'\x00' * (max_len - len_m1) + m1

    
    m2_padded =  b'\x00' * (max_len - len_m2) + m2 

    
    mh = xor_bytes(m1_padded, m2_padded)

    coeffs = [ FieldElement.gcm_from_block(mh[i:i+16]) for i in range(0, len(mh), 16)]

    coeffs.reverse()

    ghash_poly = PolyFieldElement(coeffs)

    ghash_poly_monic = divmod(ghash_poly, PolyFieldElement([ghash_poly.coefficients[-1]]))[0]
    
    canditates = anton_zassenhaus(ghash_poly_monic)

    for canditate in canditates:
        
        auth_candidate = bytes(FieldElement.gcm_to_block(canditate.coefficients[0].value))
        
        eky0 = xor_bytes(bytes(ghash(auth_candidate,ad1_org, c1_org,  L1 )),  tag1)
        auth_tag = xor_bytes(bytes(ghash(auth_candidate, ad3_org, c3_org, L3)), eky0) 
       
        if auth_tag == tag3:
            
            auth_tag_forge = xor_bytes(bytes(ghash(auth_candidate, adf_org, cf_org, LF)), eky0) 
            
            return {"tag": encode_base64(auth_tag_forge),"H": encode_base64(auth_candidate), "mask": encode_base64(eky0)}




def anton_zassenhaus(poly):

    zerospots = []
    square_free_poly = sff(poly)
   
    for factor, _  in square_free_poly:  
        distinct_degree_factorization = ddf(factor)
        for factor, exponent in distinct_degree_factorization:
            if exponent == len(factor.coefficients)-1:
                zerospots.append(factor)
            else: 
                equal_degree_factorization = edf(factor, 1) 
                for i in equal_degree_factorization:
                    zerospots.append(i)
    return zerospots



