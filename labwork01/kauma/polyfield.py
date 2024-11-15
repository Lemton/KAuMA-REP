from field_element import FieldElement


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
        
    
