from field_element import FieldElement
from utils.conversions import decode_base64, encode_base64


class PolyFieldElement:

    def __init__(self, coefficients):
    
        self.coefficients = coefficients

    def __add__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type Polyfield")
        
        max_len = max(len(self.coefficients), len(other.coefficients))
        result_coefficients = []

        for i in range(max_len):
            coeff_a = self.coefficients[i] if i < len(self.coefficients) else FieldElement(0)
            coeff_b = other.coefficients[i] if i < len(other.coefficients) else FieldElement(0)
            result_coefficients.append(coeff_a + coeff_b)

        return PolyFieldElement(result_coefficients)         
    
    def __mul__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")

        
        result_length = len(self.coefficients) + len(other.coefficients) - 1
        result_coefficients = [FieldElement(0) for _ in range(result_length)]

        
        for i, coeff_a in enumerate(self.coefficients):
            for j, coeff_b in enumerate(other.coefficients):
                
                product = coeff_a * coeff_b

                result_coefficients[i + j] = result_coefficients[i + j] + product

        
        while len(result_coefficients) > 1 and result_coefficients[-1] == FieldElement(0):
            result_coefficients.pop()

        return PolyFieldElement(result_coefficients)



       
    
    
