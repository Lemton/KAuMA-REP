from utils.conversions import reverse_bit_order

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


    def __add__(self, other):
         return FieldElement(self.value ^ other.value)

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