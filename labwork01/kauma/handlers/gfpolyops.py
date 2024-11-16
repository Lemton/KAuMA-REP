from field_element import FieldElement
from polyfield import PolyFieldElement
from utils.conversions import encode_base64, decode_base64

def gfpoly_add(arguments):

    poly_a_b64coeffs = arguments.get("A", [])
    poly_b_b64coeffs = arguments.get("B", [])

    a_coeffs = [FieldElement(int.from_bytes(decode_base64(a), 'big')) for a in poly_a_b64coeffs]
    b_coeffs = [FieldElement(int.from_bytes(decode_base64(b),'big')) for b in poly_b_b64coeffs]


    poly_a = PolyFieldElement(a_coeffs)
    poly_b = PolyFieldElement(b_coeffs)

    result_poly = poly_a + poly_b

    result_encoded = [encode_base64(coeff.to_bytes()) for coeff in result_poly.coefficients]

    return {"S" : result_encoded}

def gfpoly_mul(arguments):

    poly_a_b64coeffs = arguments.get("A", [])
    poly_b_b64coeffs = arguments.get("B", [])

    a_coeffs = [FieldElement(int.from_bytes(decode_base64(a), 'big'),"gcm") for a in poly_a_b64coeffs]
    b_coeffs = [FieldElement(int.from_bytes(decode_base64(b),'big'),"gcm") for b in poly_b_b64coeffs]
    

    poly_a = PolyFieldElement(a_coeffs)
    poly_b = PolyFieldElement(b_coeffs)

    result_poly = poly_a * poly_b

    result_encoded = [encode_base64(coeff.to_bytes()) for coeff in result_poly.coefficients]

    return {"P" : result_encoded}

def gfpoly_pow(arguments):
    coeffs = arguments.get("A", [])
    k = arguments.get("k")
    
    a_coeffs = [FieldElement(int.from_bytes(decode_base64(a), 'big'),"gcm") for a in coeffs]
    
    

    
    polypow = PolyFieldElement(a_coeffs) ** k


    polypowencode = [encode_base64(coeff.to_bytes()) for coeff in polypow.coefficients]

    return {"Z": polypowencode}