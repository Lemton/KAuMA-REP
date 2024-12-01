from field_element import FieldElement
from polyfield_element import PolyFieldElement
from utils.bitops import decode_base64, encode_base64

def gfpoly_add(arguments):
    poly_a_b64coeffs = arguments.get("A", [])
    poly_b_b64coeffs = arguments.get("B", [])

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    a_coeffs = [FieldElement.gcm_from_block(decode_base64(a)) for a in poly_a_b64coeffs]
    b_coeffs = [FieldElement.gcm_from_block(decode_base64(b)) for b in poly_b_b64coeffs]

    # Erstellung der PolyFieldElemente
    poly_a = PolyFieldElement(a_coeffs)
    poly_b = PolyFieldElement(b_coeffs)

    # Polynomaddition
    result_poly = poly_a + poly_b

    # Ergebnis zurück in Base64-Blöcke umwandeln
    result_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in result_poly.coefficients]

    return {"S": result_encoded}


def gfpoly_mul(arguments):
    poly_a_b64coeffs = arguments.get("A", [])
    poly_b_b64coeffs = arguments.get("B", [])

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    a_coeffs = [FieldElement.gcm_from_block(decode_base64(a)) for a in poly_a_b64coeffs]
    b_coeffs = [FieldElement.gcm_from_block(decode_base64(b)) for b in poly_b_b64coeffs]

    # Erstellung der PolyFieldElemente
    poly_a = PolyFieldElement(a_coeffs)
    poly_b = PolyFieldElement(b_coeffs)

    # Polynom-Multiplikation
    result_poly = poly_a * poly_b

    # Ergebnis zurück in Base64-Blöcke umwandeln
    result_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in result_poly.coefficients]

    return {"P": result_encoded}

def gfpoly_pow(arguments):
    coeffs = arguments.get("A", [])
    k = arguments.get("k", 0)

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    a_coeffs = [FieldElement.gcm_from_block(decode_base64(a)) for a in coeffs]

    # Erstellung des PolyFieldElements und Potenzierung
    polypow = PolyFieldElement(a_coeffs) ** k

    # Ergebnis zurück in Base64-Blöcke umwandeln
    polypow_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in polypow.coefficients]


    return {"Z": polypow_encoded}


def gfpoly_divmod(arguments):
    poly_a_b64coeffs = arguments.get("A", [])
    poly_b_b64coeffs = arguments.get("B", [])

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    a_coeffs = [FieldElement.gcm_from_block(decode_base64(a)) for a in poly_a_b64coeffs]
    b_coeffs = [FieldElement.gcm_from_block(decode_base64(b)) for b in poly_b_b64coeffs]

    # Erstellung der PolyFieldElemente
    poly_a = PolyFieldElement(a_coeffs)
    poly_b = PolyFieldElement(b_coeffs)

    # Polynom-Division
    quotient, remainder = divmod(poly_a, poly_b)

    # Ergebnisse zurück in Base64-Blöcke umwandeln
    quotient_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in quotient.coefficients]
    remainder_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in remainder.coefficients]

    return {
        "Q": quotient_encoded,
        "R": remainder_encoded
    }

def gfpoly_powmod(arguments):
    poly_a_b64coeffs = arguments.get("A", [])
    poly_m_b64coeffs = arguments.get("M", [])
    k = arguments.get("k", 0)

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    a_coeffs = [FieldElement.gcm_from_block(decode_base64(a)) for a in poly_a_b64coeffs]
    m_coeffs = [FieldElement.gcm_from_block(decode_base64(m)) for m in poly_m_b64coeffs]

    # Erstellung der PolyFieldElemente
    poly_a = PolyFieldElement(a_coeffs)
    poly_m = PolyFieldElement(m_coeffs)

    # Aufruf der powmod-Methode
    result_poly = poly_a.powmod(k, poly_m)

    # Ergebnis zurück in Base64-Blöcke umwandeln
    result_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in result_poly.coefficients]

    return {"Z": result_encoded}

def gfpoly_sort(arguments):
    
    polys = arguments.get("polys", [])

    # Wandelt die Base64-codierten Polynome in PolyFieldElement-Objekte um
    poly_list = [
        PolyFieldElement([
            FieldElement.gcm_from_block(decode_base64(coeff))
            for coeff in poly_base64
        ])
        for poly_base64 in polys
    ]

    # Sortiere die Polynome direkt basierend auf der `__lt__`-Methode
    sorted_polys = sorted(poly_list)

    # Kodiert die sortierten Polynome zurück in Base64
    sorted_polys_encoded = [
        [
            encode_base64(FieldElement.gcm_to_block(coeff.value))
            for coeff in poly.coefficients
        ]
        for poly in sorted_polys
    ]

    return {"sorted_polys": sorted_polys_encoded}

def gfpoly_gcd(arguments):

    poly_a_b64coeffs = arguments.get("A", [])
    poly_b_b64coeffs = arguments.get("B", [])

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    a_coeffs = [FieldElement.gcm_from_block(decode_base64(a)) for a in poly_a_b64coeffs]
    b_coeffs = [FieldElement.gcm_from_block(decode_base64(b)) for b in poly_b_b64coeffs]

    # Erstellung der PolyFieldElemente
    poly_a = PolyFieldElement(a_coeffs)
    poly_b = PolyFieldElement(b_coeffs)

    # Berechnung des ggT
    gcd_poly = PolyFieldElement.gcd(poly_a, poly_b)

    # Normierung des Ergebnisses zu einem monischen Polynom
    leading_coeff = gcd_poly.coefficients[-1]
    monic_gcd = PolyFieldElement([coeff / leading_coeff for coeff in gcd_poly.coefficients])

    # Ergebnis zurück in Base64-Blöcke umwandeln
    gcd_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in monic_gcd.coefficients]

    return {"G": gcd_encoded}


def gfpoly_make_monic(arguments):
    poly_a_b64coeffs = arguments.get("A", [])

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    a_coeffs = [FieldElement.gcm_from_block(decode_base64(a)) for a in poly_a_b64coeffs]

    # Erstellung des PolyFieldElements
    poly_a = PolyFieldElement(a_coeffs)

    # Führenden Koeffizienten extrahieren
    leading_coeff = poly_a.coefficients[-1]

    # Normierung des Polynoms
    monic_poly = PolyFieldElement([coeff / leading_coeff for coeff in poly_a.coefficients])

    # Ergebnis zurück in Base64-Blöcke umwandeln
    monic_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in monic_poly.coefficients]

    return {"A*": monic_encoded}

def gfpoly_sqrt(arguments):
    poly_q_b64coeffs = arguments.get("Q", [])

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    q_coeffs = [FieldElement.gcm_from_block(decode_base64(q)) for q in poly_q_b64coeffs]

    # Erstellung des PolyFieldElements
    poly_q = PolyFieldElement(q_coeffs)

    # Berechnung der Quadratwurzel
    sqrt_poly = poly_q.sqrt()

    # Ergebnis zurück in Base64-Blöcke umwandeln
    sqrt_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in sqrt_poly.coefficients]

    return {"S": sqrt_encoded}

def gfpoly_diff(arguments):
    poly_f_b64coeffs = arguments.get("F", [])

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    f_coeffs = [FieldElement.gcm_from_block(decode_base64(f)) for f in poly_f_b64coeffs]

    # Erstellung des PolyFieldElements
    poly_f = PolyFieldElement(f_coeffs)

    # Berechnung der Ableitung
    derived_poly = poly_f.differentiate()

    # Ergebnis zurück in Base64-Blöcke umwandeln
    derived_encoded = [encode_base64(FieldElement.gcm_to_block(coeff.value)) for coeff in derived_poly.coefficients]

    return {"F'": derived_encoded}


def gfpoly_factor_sff(arguments):
    poly_f_b64coeffs = arguments.get("F")

    # Umwandlung der Koeffizienten von Base64 zu FieldElementen
    f_coeffs = [FieldElement.gcm_from_block(decode_base64(f)) for f in poly_f_b64coeffs]

    # Erstellung des PolyFieldElements
    poly_f = PolyFieldElement(f_coeffs)
    
    # Square-Free Factorization durchführen
    factors = sff(poly_f)

    return {
        "factors": [
            {
                "factor": [
                    encode_base64(FieldElement.gcm_to_block(coeff.value))
                    for coeff in factor.coefficients
                ],
                "exponent": multiplicity
            }
            for factor, multiplicity in factors
        ]
    }

def sff(f):
        """
        Implementiert den Square-Free Factorization Algorithmus (SFF) im Galois-Feld GF(2^m).
        """
        # Berechne c = gcd(f, f')
        f_prime = f.differentiate()
        print(f"f_prime{f_prime}")
        c = PolyFieldElement.gcd(f, f_prime)
        # f ← f / c
        print(f"f: {f}")
        f = f // c
        print(f"c: {c}")
        # Initialisiere z ← ∅ und e ← 1
        z = []
        e = 1
        print(f)
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
            print("go")
            for f_star, e_star in sff(c.sqrt()):
                # z ← z ∪ {(f*, 2e*)}
                z.append((f_star, e_star*2))

        # return z
        return sorted(z)