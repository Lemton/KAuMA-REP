class FieldElement:

    MODULO = (1 << 128) | (1 << 7) | (1 << 2) | (1 << 1) | 1

    def __init__(self, value):
        self.value = value % self.MODULO

    def __xor__(self, other):
        
        if isinstance(other, FieldElement):
            new_value = self.value ^ other.value
        elif isinstance(other, int):
            new_value = self.value ^ other
        else:
            raise TypeError("Unsupported type for XOR operation")

        return FieldElement(new_value % self.MODULO)


    def __mul__(self, other):
        if isinstance(other, FieldElement):
            Y = other.value
        elif isinstance(other, int):
            Y = other
        else:
            raise TypeError("Multiplikation ist nur zwischen einem FieldElement und einem FieldElement oder Integer definiert")

        X = int(self)
        Y = int(other)
        
        z = 0
        V : int = X
        for i in range(128):
            
            if (Y >> i) & 0x1 == 1:
               
                z = z^V 
                
            if (V >> 127) & 0x1 == 0 :
                
                V <<= 1
                
            else:

                V = ( V << 1 ) ^ self.MODULO
                
            
        return FieldElement(z)

    def __str__(self):
        return f"{int(self)}"
    
    def __int__(self):
         return self.value

    def from_bytes(self):
         
         return self.value.from_bytes(byteorder = "big", length = 16)


    def to_bytes(self):
         return self.value.to_bytes(16, byteorder = 'little')

    def __eq__(self, other):
        	return ((int(self)-int(other)) % self.MODULO) == 0