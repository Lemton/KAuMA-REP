import binascii
from utils.bitops import reverse_bit_order
import base64

class FieldElement:

    MODULO = (1 << 128) | (1 << 7) | (1 << 2) | (1 << 1) | 1

    def __init__(self, value):
        self.value = value
        
    def __xor__(self, other):
        return FieldElement(self.value ^ int(other))

    def __mul__(self, other):
    
        if not isinstance(other, FieldElement):
            raise TypeError("Multiplication is only supported between FieldElement instances")

        X = self.value
        Y = other.value
        result = 0

        while Y:
            # Wenn das niedrigste Bit von Y gesetzt ist, addiere X zu result
            if Y & 1:
                result ^= X

            # Verschiebe X um 1 Bit nach links und reduziere mit MODULO, falls nötig
            if X & (1 << 127):  # Prüfen, ob das höchste Bit von X gesetzt ist
                X = (X << 1) ^ self.MODULO
            else:
                X <<= 1

            # Verschiebe Y um 1 Bit nach rechts
            Y >>= 1

        return FieldElement(result)
        
    def __invert__(self):
       
        if self.value == 0:
            raise ZeroDivisionError("Cannot invert zero in a finite field")

        r0, r1 = self.MODULO, self.value  # Initialisiere Restwerte
        t0, t1 = 0, 1  # Initialisiere Koeffizienten für das Inverse

        while r1 != 0:
            # Gradunterschied zwischen r0 und r1 berechnen
            if r0 < r1:
                r0, r1 = r1, r0  # Sicherstellen, dass r0 >= r1
                t0, t1 = t1, t0

            q = r0.bit_length() - r1.bit_length()

            # Schutz vor negativen Shifts
            if q < 0:
                raise ValueError("Unexpected negative shift count during inverse computation")

            # Aktualisiere Reste und Koeffizienten
            r0, r1 = r1, r0 ^ (r1 << q)
            t0, t1 = t1, t0 ^ (t1 << q)

            # Prüfen, ob r1 Null wird, um Endlosschleifen zu vermeiden
            if r1 == 0:
                break

        # Prüfen, ob ggT 1 ist
        if r0 != 1:
            raise ZeroDivisionError("No multiplicative inverse exists")

        return FieldElement(t0)


    def __truediv__(self, other):
        """
        Überlädt den /-Operator, um die Division von Feld-Elementen zu ermöglichen.
        """
        if not isinstance(other, FieldElement):
            raise TypeError("Division is only supported between FieldElement instances")
        
        inv = ~other
        # Division ist definiert als Multiplikation mit dem Inversen
        return self * inv 


    def __add__(self, other):
        if not isinstance(other, FieldElement):
            raise TypeError("Addition is only supported between FieldElement instances")

        new_value = self.value ^ other.value
        return FieldElement(new_value)   

    def __pow__(self, exponent):
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")

        if exponent == 0:
            return FieldElement(1)
        
        if exponent == 1:
            return self
        
        result = FieldElement(1)
        base = self

        while exponent > 0:
            if exponent & 1:
                result *= base
            base *= base
            exponent >>= 1

        return result
    
    
    def sqrt(self):
        
        return self ** (2**127)

    def __str__(self):
        return f"{int(self)}"
    
    def __int__(self):
         return self.value
    
    def from_bytes(self):
         return self.value.from_bytes(byteorder = "big", length = 16)


    def to_bytes(self, length = 16, byteorder='big'):
         return self.value.to_bytes(length, byteorder)

    def __eq__(self, other):
        return ((int(self)-int(other)) % self.MODULO) == 0
    
    
    def __repr__(self):
        # Assuming the value is an integer; adjust if your implementation differs
        return f"FieldElement({base64.b64encode((self.value.to_bytes(16, byteorder="big")))}))"


   
    @staticmethod
    def gcm_from_block(block):
       
        int_value = int.from_bytes(reverse_bit_order(block), byteorder='little')
        return FieldElement(int_value)


    @staticmethod
    def gcm_to_block(integer_value):
        
        reversed_bytes = reverse_bit_order(integer_value.to_bytes(16, byteorder='little'))
        return reversed_bytes
    
    @staticmethod
    def xex_from_block(block):

        if len(block) != 16:
            raise ValueError("XEX-Blöcke müssen genau 16 Bytes lang sein.")
        int_value = int.from_bytes(block, byteorder='little')
        return FieldElement(int_value)

    @staticmethod
    def xex_to_block(int_value):
 
        bytes_data = int_value.to_bytes(16, byteorder='little')
        return bytes_data 
