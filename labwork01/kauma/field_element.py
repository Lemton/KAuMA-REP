from utils.conversions import reverse_bit_order
from utils.conversions import encode_base64
class FieldElement:

    MODULO = (1 << 128) | (1 << 7) | (1 << 2) | (1 << 1) | 1

    def __init__(self, value, semantic=None):
        self.value = value % self.MODULO
        self.semantic = semantic

    def __xor__(self, other):
        
        if isinstance(other, FieldElement):
            new_value = self.value ^ other.value
        elif isinstance(other, int):
            new_value = self.value ^ other
        else:
            raise TypeError("Unsupported type for XOR operation")

        return FieldElement(new_value % self.MODULO)


    def __mul__(self, other):

        if not isinstance(other, FieldElement):
            raise TypeError("Multiplication is only supported between FieldElement instances")

        X = int(self)
        Y = int(other)
        
        
        if self.semantic == "gcm":
            X = int.from_bytes(reverse_bit_order(X.to_bytes(16, byteorder='big')), byteorder='little')
            Y = int.from_bytes(reverse_bit_order(Y.to_bytes(16, byteorder='big')), byteorder='little')

        elif self.semantic == "xex":
            
            pass

        z = 0
        V: int = X
        for i in range(128):
            if (Y >> i) & 0x1 == 1:
                z ^= V  
            
            
            if (V >> 127) & 0x1 == 0:
                V <<= 1
            else:
                V = (V << 1) ^ self.MODULO  

        result = FieldElement(z, self.semantic)
        
        if self.semantic == "gcm":
            result.value = int.from_bytes(reverse_bit_order(result.value.to_bytes(16, byteorder='big')), byteorder='little')

         

        return result
    
    def inverse(self):
       

        if self.value == 0:
            raise ZeroDivisionError("Cannot invert zero in a finite field")
    
        
        return self ** (2**128 - 2)

    def __floordiv__(self, other):
        if not isinstance(other, FieldElement):
            raise TypeError("Division is only supported between FieldElement instances")

        if self.semantic != other.semantic:
            raise ValueError("Field elements must have the same semantic for division")

        
        X = int(self)
        Y = int(other)

        if self.semantic == "gcm":
            
            X = int.from_bytes(reverse_bit_order(X.to_bytes(16, byteorder='big')), byteorder='little')
            Y = int.from_bytes(reverse_bit_order(Y.to_bytes(16, byteorder='big')), byteorder='little')

        
        inv_Y = FieldElement(Y, self.semantic).inverse()  
        Z = FieldElement(X, self.semantic) * inv_Y  

        if self.semantic == "gcm":
            
            Z.value = int.from_bytes(reverse_bit_order(Z.value.to_bytes(16, byteorder='big')), byteorder='little')

        return Z

    def __add__(self, other):
        if not isinstance(other, FieldElement):
            raise TypeError("Addition is only supported between FieldElement instances")

        new_value = self.value ^ other.value
        return FieldElement(new_value, self.semantic)   

    def __pow__(self, exponent):
    
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")

        result = FieldElement(1, self.semantic)  
        base = self

        while exponent > 0:
            if exponent % 2 == 1:
                result = result * base  
            base = base * base 
            exponent //= 2  

        return result

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
        return f"FieldElement({encode_base64(self.value.to_bytes(16, byteorder="big"))}))"
