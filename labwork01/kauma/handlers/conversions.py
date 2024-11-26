import base64

def poly2block(arguments):
    coefficients = arguments.get("coefficients", [])
    semantic = arguments.get("semantic", "")
    if semantic not in ("gcm", "xex"):
        raise ValueError("Keine bekannte Semantik")
    
    block = bytearray(16)
    for coeff in coefficients:
        if coeff < 0 or coeff >= 128:
            raise ValueError("Koeffizient muss im Bereich [0, 127] sein.")
        
        byte_pos = coeff // 8
        bit_pos = coeff % 8

        if semantic == "gcm":
            block[byte_pos] |= 1 << (7 - bit_pos)  # BIG-Endian
        else:  # "xex"
            block[byte_pos] |= 1 << bit_pos       # LITTLE-Endian
    
    return {"block": base64.b64encode(block).decode('utf-8')}

def block2poly(arguments):
    block_base64 = arguments.get("block", "")
    semantic = arguments.get("semantic", "")
    if semantic not in ("gcm", "xex"):
        raise ValueError("Keine bekannte Semantik")
    
    block = base64.b64decode(block_base64)
    if len(block) != 16:
        raise ValueError("Der Block muss genau 16 Bytes (128 Bit) lang sein.")
    
    coefficients = []
    for byte_index, byte_value in enumerate(block):
        for bit_pos in range(8):
            if semantic == "xex" and (byte_value & (1 << bit_pos)):
                coefficients.append(byte_index * 8 + bit_pos)
            elif semantic == "gcm" and (byte_value & (1 << (7 - bit_pos))):
                coefficients.append(byte_index * 8 + bit_pos)
    
    return {"coefficients": coefficients}
