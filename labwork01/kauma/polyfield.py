from field_element import FieldElement
from utils.conversions import decode_base64, encode_base64


class PolyFieldElement:

    def __init__(self, coefficients):
    
        self.coefficients = coefficients
        
    def __add__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")
        
        max_len = max(len(self.coefficients), len(other.coefficients))
        result_coefficients = []

        for i in range(max_len):
            coeff_a = self.coefficients[i] if i < len(self.coefficients) else FieldElement(0)
            coeff_b = other.coefficients[i] if i < len(other.coefficients) else FieldElement(0)
            
            result = coeff_a ^ coeff_b
            
            result_coefficients.append(result)

        while len(result_coefficients) > 1 and result_coefficients[-1] == FieldElement(0):
            result_coefficients.pop()

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

    def __pow__(self, exponent):
        
        if exponent == 0:
                return FieldElement(1)


        base = self

        result = base  

        for i in range(1,exponent):
            result = result * base
            for coeff in result.coefficients:
                coeff.semantic = "gcm"

        '''

        while exponent > 1:
            print(exponent)
            if exponent % 2 == 1:
                result = result * base  
                for coeff in result.coefficients:
                    coeff.semantic = "gcm"
            base = base * base  
            for coeff in base.coefficients:
                    coeff.semantic = "gcm"

            exponent //= 2

        '''
        
        
        result.coefficients = self._remove_leading_zeros(result.coefficients)
        return result

    def _remove_leading_zeros(self, coefficients):
     
        while len(coefficients) > 1 and coefficients[-1] == FieldElement(0):
            coefficients.pop()
        return coefficients



    def __repr__(self):
        return f"PolyFieldElement(coefficients={self.coefficients})"


