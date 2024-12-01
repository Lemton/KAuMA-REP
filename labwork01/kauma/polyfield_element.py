from field_element import FieldElement
from itertools import zip_longest
import copy

class PolyFieldElement:

    def __init__(self, coefficients):
        
        self.coefficients = coefficients

    def __add__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")
    
        # XOR zwischen den Koeffizienten
        result_coefficients = [
            coeff_a ^ coeff_b for coeff_a, coeff_b in zip_longest(
                self.coefficients, other.coefficients, fillvalue=FieldElement(0)
            )
        ]
        return PolyFieldElement(self.remove_leading_zeros(result_coefficients))
    
    def __mul__(self, other):
        if not isinstance(other, PolyFieldElement):
            raise TypeError("Operand must be of type PolyFieldElement")
        
        result_length = len(self.coefficients) + len(other.coefficients) - 1
        result_coefficients = [FieldElement(0)] * result_length

        for i, coeff_a in enumerate(self.coefficients):
            if coeff_a == FieldElement(0):
                continue  # Überspringe 0-Multiplikationen
            for j, coeff_b in enumerate(other.coefficients):
                result_coefficients[i + j] ^= coeff_a * coeff_b  # XOR statt Addition im GF(2^n)

        return PolyFieldElement(self.remove_leading_zeros(result_coefficients))
    
    def __floordiv__(self, other):
        
        quotient, _ = divmod(self,other)
        return quotient

    def __pow__(self, exponent):
        
        
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")
        if exponent == 0:
            return PolyFieldElement([FieldElement(1)])
        if exponent == 1:
            return self

        result = PolyFieldElement([FieldElement(1)])
        base = self.copy()

        while exponent:
            if exponent & 1:  # Prüfe das niedrigstwertige Bit
                result = result * base
            base = base * base
            exponent >>= 1  # Schiebe die Bits nach rechts (Division durch 2)

        return result
    
    def __divmod__(self, other):
        
        
        if other.is_zero():
            raise ZeroDivisionError("Cannot divide by zero polynomial")

        # Kopiere die Koeffizienten des Dividenden
        remainder = self.coefficients[:]
        quotient = [FieldElement(0)] * (len(remainder) - len(other.coefficients) + 1)

        
        divisor_leading_coeff = other.coefficients[-1]

        if divisor_leading_coeff == FieldElement(0):
            raise ZeroDivisionError("Leading coefficient of divisor is zero")




        while len(remainder) >= len(other.coefficients):
            
            
            # Gradunterschied zwischen Divisor und aktuellem Rest
            degree_diff = len(remainder) - len(other.coefficients)
            # Führender Term der Division (Rest / Divisor-Leading-Coeff)
            leading_term = remainder[-1] / divisor_leading_coeff
            quotient[degree_diff] = leading_term

            # Subtrahiere (Divisor * leading_term) vom Rest
            for i in range(len(other.coefficients)):
                remainder[i + degree_diff] ^= other.coefficients[i] * leading_term

          

            # Entferne führende Null
            while len(remainder) > 1 and remainder[-1] == FieldElement(0):
                remainder.pop()

            if remainder[-1] == FieldElement(0):
                break
        # Entferne führende Null im Quotienten (falls nötig)
        while len(quotient) > 1 and quotient[-1] == FieldElement(0):
            quotient.pop()

        if len(quotient) == 0:
            quotient = [FieldElement(0)]    

        return PolyFieldElement(quotient), PolyFieldElement(remainder)

    def powmod(self, exponent, modulus):

        if exponent < 0:
            raise ValueError("Exponent must be non-negative")


        # Startwert für das Ergebnis ist das neutrale Element (1)
        result = PolyFieldElement([FieldElement(1)])
        base = self.copy()

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

        # Verwende die optimierte divmod-Implementierung
        _, remainder = divmod(self, other)
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

    def __lt__(self, other):

        if not isinstance(other, PolyFieldElement):
            return NotImplemented

        # Vergleich nach Grad
        if len(self.coefficients) != len(other.coefficients):
            return len(self.coefficients) < len(other.coefficients)

        # Lexikografischer Vergleich der Koeffizienten von höchster Potenz zu niedrigster
        for coeff_self, coeff_other in zip(
            reversed(self.coefficients), reversed(other.coefficients)
        ):
            if coeff_self != coeff_other:
                return coeff_self.value < coeff_other.value

        # Wenn beide Polynome vollständig gleich sind, ist keins kleiner
        return False
    
        
    def gcd(a, b):
        
        while not b.is_zero():
            if b.coefficients[-1] == FieldElement(0):
                raise ValueError("Leading coefficient of divisor is zero during GCD computation.")
            b_leading_coeff = b.coefficients[-1]
            b = PolyFieldElement([coeff / b_leading_coeff for coeff in b.coefficients])
            a, b = b, a % b  # Modulo-Operation
        return a

    def differentiate(self):
        diff = self.copy()
        result = diff.coefficients

        if len(diff.coefficients) == 1:
            result = [FieldElement(0)]

        else:
            result.pop(0)

            for i in range(1,len(result), 2):
                result[i] = FieldElement(0)

        result = diff.remove_leading_zeros(result)

        return PolyFieldElement(result)

    
    def sqrt(self):
        
        result = []
        for i, coeff in enumerate(self.coefficients):
            if i % 2 == 0:
                result.append(coeff.sqrt())
            else:
                pass
        
        return PolyFieldElement(result)

    def is_one(self):
        return len(self.coefficients) == 1 and self.coefficients[0] == FieldElement(1)

    def is_zero(self):
     
        return all(coeff == FieldElement(0) for coeff in self.coefficients)


    def __repr__(self):
        return f"PolyFieldElement(coefficients={self.coefficients})"
    

    def copy(self):
        
        return PolyFieldElement(self.coefficients.copy())
    
    