import base64

def poly2block(arguments):
    coefficients = arguments.get("coefficients", [])      
    semantic = arguments.get("semantic","")
    block = bytearray(16)


    for coeff in coefficients:
        if coeff < 0 or coeff >= 128:
            raise ValueError("Koeffizient muss im Bereich [0, 127] sein.")
        
        byte_pos = coeff // 8  # Position im Bytearray
        bit_pos = coeff % 8    # Position im Byte

        if semantic == "gcm":
            block[byte_pos] |= (1<< (7-bit_pos))        #BIG-Endian
        elif semantic == "xex":
            block[byte_pos] |= (1 << bit_pos)           #LITTLE-Endian
        else:
            raise ValueError("keine bekannte Semantik")
    block_base64 = base64.b64encode(block).decode('utf-8')

    return {"block": block_base64}

def block2poly(arguments):
    block_base64 = arguments.get("block", "")
    semantic = arguments.get("semantic", "")
    
    block = base64.b64decode(block_base64)
    
    if len(block) != 16:
        raise ValueError("Der Block muss genau 16 Bytes (128 Bit) lang sein.")
    
    coefficients = []


    for byte_index, byte_value in enumerate(block):
        for bit_pos in range(8):
            if semantic == "xex":
                if byte_value & (1 << bit_pos):
                    coefficient = byte_index * 8 + bit_pos
                    coefficients.append(coefficient)
            elif semantic == "gcm":
                if byte_value & (1 << (7 - bit_pos)):
                    coefficient = byte_index * 8 + bit_pos
                    coefficients.append(coefficient)
            else:
                raise ValueError("Keine bekannte Semantic")

    for coeff in coefficients:
        if coeff < 0 or coeff >= 128:
            raise ValueError("Koeffizient muss im Bereich [0, 127] sein.")
        

    return {"coefficients": coefficients}

def reverse_bit_order(byte_array):
    reversed_bytes = bytearray()
    for byte in byte_array:
        reversed_byte = int('{:08b}'.format(byte)[::-1], 2)
        reversed_bytes.append(reversed_byte)
    return reversed_bytes




def xor_bytes(data1, data2):
    return bytes(a ^ b for a,b in zip(data1, data2) )

def encode_base64(data):
    return base64.b64encode(data).decode('utf-8')

def decode_base64(data):
    return base64.b64decode(data)