from field_element import FieldElement

class PolyFieldElement:

    def __init__(self, coefficients):
        
        self.coefficients = coefficients

    def __add__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")

        # Auffüllen mit Null-Elementen
        len_diff = len(self.coefficients) - len(other.coefficients)
        if len_diff > 0:
            other_coefficients = other.coefficients + [FieldElement(0)] * len_diff
            self_coefficients = self.coefficients
        else:
            self_coefficients = self.coefficients + [FieldElement(0)] * abs(len_diff)
            other_coefficients = other.coefficients

        # Elementweise Addition
        result_coefficients = [
            coeff_a ^ coeff_b for coeff_a, coeff_b in zip(self_coefficients, other_coefficients)
        ]

        # Entferne führende Nullen
        result_coefficients = self.remove_leading_zeros(result_coefficients)
        return PolyFieldElement(result_coefficients)
    
    def __mul__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")

        result_length = len(self.coefficients) + len(other.coefficients) - 1
        result_coefficients = [FieldElement(0)] * result_length

        for i, coeff_a in enumerate(self.coefficients):
            for j, coeff_b in enumerate(other.coefficients):
                result_coefficients[i + j] += coeff_a * coeff_b

        # Entferne führende Nullen
        result_coefficients = self.remove_leading_zeros(result_coefficients)
        return PolyFieldElement(result_coefficients)

    def __pow__(self, exponent):
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")
        if exponent == 0:
            return PolyFieldElement([FieldElement(1)])
        if exponent == 1:
            return self

        result = PolyFieldElement([FieldElement(1)])
        base = self

        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2

        return result
    
    def __divmod__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")

        if all(coeff == FieldElement(0) for coeff in other.coefficients):
            raise ZeroDivisionError("Cannot divide by a zero polynomial")

        quotient = []
        remainder = self.coefficients[:]

        divisor_degree = len(other.coefficients) - 1
        divisor_leading_coeff = other.coefficients[-1]

        while len(remainder) >= len(other.coefficients):
            degree_diff = len(remainder) - len(other.coefficients)
            leading_term = remainder[-1] / divisor_leading_coeff

            # Erstelle das Polynom des aktuellen Quotienten-Terms
            term_coefficients = [FieldElement(0)] * degree_diff + [leading_term]
            term_poly = PolyFieldElement(term_coefficients)

            # Aktualisiere den Quotienten
            quotient = [leading_term] + quotient

            # Subtrahiere (term_poly * other) von remainder
            remainder_poly = PolyFieldElement(remainder)
            remainder = (remainder_poly + (term_poly * other)).coefficients

            # Entferne führende Nullen im Rest
            while len(remainder) > 1 and remainder[-1] == FieldElement(0):
                remainder.pop()

        # Erstelle PolyFieldElemente für Quotient und Rest
        quotient_poly = PolyFieldElement(quotient)
        remainder_poly = PolyFieldElement(remainder)

        # Rückgabe als Tupel
        return quotient_poly, remainder_poly

    def powmod(self, exponent, modulus):

        if not isinstance(modulus, PolyFieldElement):
            raise TypeError("Modulus must be of type PolyFieldElement")

        if exponent < 0:
            raise ValueError("Exponent must be non-negative")

        # Startwert für das Ergebnis ist das neutrale Element (1)
        result = PolyFieldElement([FieldElement(1)])
        base = self

        # Square-and-Multiply Algorithmus
        while exponent > 0:
            if exponent % 2 == 1:
                
                result = (result * base) % modulus

            
            base = (base * base) % modulus
            exponent //= 2

        return result

    def __mod__(self, other):

        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")

        quotient, remainder = divmod(self, other)
        return remainder

    def __eq__(self, other):
        if not isinstance(other, PolyFieldElement):
            return False
        return self.coefficients == other.coefficients

    def to_bytes(self):
        return b''.join([coeff.to_bytes() for coeff in self.coefficients])

    @staticmethod
    def from_bytes(byte_data, coeff_size=16):
        coeffs = [FieldElement(int.from_bytes(byte_data[i:i+coeff_size], 'big'))
                for i in range(0, len(byte_data), coeff_size)]
        return PolyFieldElement(coeffs)


    def remove_leading_zeros(self, coefficients):
     
        while len(coefficients) > 1 and coefficients[-1] == FieldElement(0):
            coefficients.pop()
        return coefficients



    def __repr__(self):
        return f"PolyFieldElement(coefficients={self.coefficients})"