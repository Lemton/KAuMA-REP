from field_element import FieldElement
from polyfield_element import PolyFieldElement
from utils.bitops import decode_base64, encode_base64
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
        poly = FieldElement(random.randint(1, (2**128)//2))
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
    c1 = split_into_blocks(decode_base64(arguments["m1"]["ciphertext"]))
    ad1 = split_into_blocks(decode_base64(arguments["m1"]["associated_data"]))
    tag1 = FieldElement.gcm_from_block(decode_base64(arguments["m1"]["tag"]))

    # Extrahiere m2
    c2 = split_into_blocks(decode_base64(arguments["m2"]["ciphertext"]))
    ad2 = split_into_blocks(decode_base64(arguments["m2"]["associated_data"]))
    tag2 = FieldElement.gcm_from_block(decode_base64(arguments["m2"]["tag"]))

    # Extrahiere m3
    c3 = split_into_blocks(decode_base64(arguments["m3"]["ciphertext"]))
    ad3 = split_into_blocks(decode_base64(arguments["m3"]["associated_data"]))
    tag3 = FieldElement.gcm_from_block(decode_base64(arguments["m3"]["tag"]))

    # Extrahiere Forgery
    cf = split_into_blocks(decode_base64(arguments["forgery"]["ciphertext"]))
    adf = split_into_blocks(decode_base64(arguments["forgery"]["associated_data"]))

    # GHASH-Polynom berechnen (T1 ⊕ T2 = GHASH Diff)
    # GHASH-Polynom berechnen
    t_diff = tag1 ^ tag2
    coefficients = [
        u1 ^ u2 for u1, u2 in zip(c1 + compute_length_block(ad1, c1), c2 + compute_length_block(ad2, c2))
    ]
    ghash_poly = construct_polynomial(coefficients, t_diff)

    # Faktorisierung: SFF → DDF → EDF
    # Schritt 1: Square-Free Factorization (SFF)
    square_free_factors = sff(ghash_poly)  

    square_free_polys = [factor for factor, _ in square_free_factors]

    # Schritt 2: Distinct-Degree Factorization (DDF)
    distinct_degree_factors = []
    for poly in square_free_polys:
        if isinstance(poly, PolyFieldElement):
            distinct_degree_factors.extend(ddf(poly))
            print(distinct_degree_factors)
        else:
            raise TypeError(f"Ungültiger Typ in square_free_polys: {type(poly)}")

    # Schritt 3: Equal-Degree Factorization (EDF)
    equal_degree_factors = []
    for poly, degree in distinct_degree_factors:
        print(degree)     
        equal_degree_factors.extend(edf(poly, degree))
       
    # H-Kandidaten sammeln (nur lineare Faktoren)
    h_candidates = [
        -factor.coefficients[0]
        for factor in equal_degree_factors
        if factor.degree() == 1
    ]

    # Validierung der H-Kandidaten
    for h_candidate in h_candidates:
        ek_y0 = tag1 ^ compute_ghash(ad1, c1, nonce, h_candidate)
        if validate_h_candidate(h_candidate, ek_y0, ad3, c3, nonce, tag3):
            # Authentifizierungsmaske (Ek(y0)) und Fälschungstag berechnen
            forgery_tag = compute_forgery_tag(adf, cf, nonce, h_candidate, ek_y0)
            return {
                "H": encode_base64(FieldElement.gcm_to_block(h_candidate.value)),
                "mask": encode_base64(FieldElement.gcm_to_block(ek_y0.value)),
                "tag": encode_base64(FieldElement.gcm_to_block(forgery_tag.value))
            }

    # Kein gültiger Kandidat gefunden
    raise ValueError("Kein gültiger H-Kandidat gefunden.")

def construct_polynomial(coefficients, t_diff):
    """Erstellt ein Polynom aus den XORed-Ciphertext-Blöcken und T-Differenz."""
    return PolyFieldElement(coefficients + [t_diff])

def compute_length_block(ad_blocks, c_blocks):
    """Berechnet den L-Block basierend auf den Längen der Daten."""
    ad_length = len(ad_blocks) * 128  # Länge in Bits
    c_length = len(c_blocks) * 128  # Länge in Bits
    return [FieldElement((ad_length << 64) | c_length)]

def validate_h_candidate(h_candidate, ek_y0, ad3, c3, nonce, tag3):
    """Prüft, ob ein H-Kandidat gültig ist."""
    computed_tag = compute_ghash(ad3, c3, nonce, h_candidate) ^ ek_y0
    return computed_tag == tag3

def compute_forgery_tag(adf, cf, nonce, h, ek_y0):
    """Berechnet den Tag für die gefälschte Nachricht."""
    return compute_ghash(adf, cf, nonce, h) ^ ek_y0

def compute_ghash(ad_blocks, c_blocks, nonce, h):
    """Berechnet das GHASH-Tag."""
    l_block = compute_length_block(ad_blocks, c_blocks)
    ghash_input = ad_blocks + c_blocks + l_block
    ghash_result = FieldElement(0)
    for block in ghash_input:
        ghash_result ^= block
        ghash_result *= h
    return ghash_result



def split_into_blocks(data):
    return [FieldElement.gcm_from_block(data[i:i+16]) for i in range(0, len(data), 16)]
