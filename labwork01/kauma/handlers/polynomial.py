import base64

class PolynomialHandler:
    """Handler für die Umwandlung eines Polynoms in einen 16-Byte-Binärblock."""
    
    @staticmethod
    def poly2block(arguments):
        coefficients = arguments.get("coefficients", [])      
        block = bytearray(16)

        for coeff in coefficients:
            if coeff < 0 or coeff >= 128:
                raise ValueError("Koeffizient muss im Bereich [0, 127] sein.")
            
            byte_pos = coeff // 8  # Position im Bytearray
            bit_pos = coeff % 8    # Position im Byte

            # (Little Endian)
            block[byte_pos] |= (1 << bit_pos)
        block_base64 = base64.b64encode(block).decode('utf-8')

        return {"block": block_base64}

    def block2poly(arguments):
        block_base64 = arguments.get("block", "")
        
        block = base64.b64decode(block_base64)
        
        if len(block) != 16:
            raise ValueError("Der Block muss genau 16 Bytes (128 Bit) lang sein.")
        
        coefficients = []


        for byte_index, byte_value in enumerate(block):
            for bit_pos in range(8):
                if byte_value & (1 << bit_pos):
                    coefficient = byte_index * 8 + bit_pos
                    coefficients.append(coefficient)
        
        for coeff in coefficients:
            if coeff < 0 or coeff >= 128:
                raise ValueError("Koeffizient muss im Bereich [0, 127] sein.")
            

        return {"coefficients": coefficients}
