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

        z = 0
        V = X

        while Y:
            if Y & 1:
                z ^= V
            
            if V & (1 << 127):  # Prüfen des höchsten Bits
                V = (V << 1) ^ self.MODULO
            else:
                V <<= 1
            
            Y >>= 1  # Rechts-Shift für Y
        
        return FieldElement(z)
        
    def __invert__(self):
        """
        Überlädt den ~-Operator, um das multiplikative Inverse des Feld-Elements zu berechnen.
        """
        if self.value == 0:
            raise ZeroDivisionError("Cannot invert zero in a finite field")
        return self ** (2 ** 128 - 2)

    def __truediv__(self, other):
        """
        Überlädt den /-Operator, um die Division von Feld-Elementen zu ermöglichen.
        """
        if not isinstance(other, FieldElement):
            raise TypeError("Division is only supported between FieldElement instances")
        
        # Division ist definiert als Multiplikation mit dem Inversen
        return self * ~other


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

        # Hier wird angenommen, dass die Quadratwurzel im Galois-Feld durch Potenzierung berechnet wird
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
        """
        Wandelt einen 16-Byte-Block (als Bytes) direkt in ein FieldElement für die GCM-Semantik um.
        """
        if len(block) != 16:
            raise ValueError("GCM-Blöcke müssen genau 16 Bytes lang sein.")
        int_value = int.from_bytes(reverse_bit_order(block), byteorder='little')
        return FieldElement(int_value)


    @staticmethod
    def gcm_to_block(integer_value):
        
        reversed_bytes = reverse_bit_order(integer_value.to_bytes(16, byteorder='little'))
        return reversed_bytes
    
    @staticmethod
    def xex_from_block(block):
        """
        Wandelt einen 16-Byte-Block (als Bytes) direkt in ein FieldElement für die XEX-Semantik um.
        """
        if len(block) != 16:
            raise ValueError("XEX-Blöcke müssen genau 16 Bytes lang sein.")
        int_value = int.from_bytes(block, byteorder='little')
        return FieldElement(int_value)

    @staticmethod
    def xex_to_block(int_value):
        """
        Encodiert einen FieldElement-Wert in einen 16-Byte-XEX-Block.
        """
        bytes_data = int_value.to_bytes(16, byteorder='little')
        return bytes_data 
