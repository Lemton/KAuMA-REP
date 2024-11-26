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
