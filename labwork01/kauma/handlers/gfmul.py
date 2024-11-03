from utils.conversions import encode_base64, decode_base64 , reverse_bit_order 
from field_element import FieldElement

def gfmul(arguments):
    block_a_base64 = arguments.get("a")
    block_b_base64 = arguments.get("b")
    semantic = arguments.get("semantic", "")
    block_a_bytes = decode_base64(block_a_base64)
    block_b_bytes = decode_base64(block_b_base64)

    
    if semantic == "gcm":
        block_a_reversed = reverse_bit_order(block_a_bytes)
        block_b_reversed = reverse_bit_order(block_b_bytes)
        
        block_a = FieldElement(int.from_bytes(block_a_reversed, byteorder='big'))
        block_b = FieldElement(int.from_bytes(block_b_reversed, byteorder='big'))

    elif semantic == "xex":
        block_a = FieldElement(int.from_bytes(block_a_bytes, byteorder='little'))
        block_b = FieldElement(int.from_bytes(block_b_bytes, byteorder='little'))
    else:
        raise ValueError("Diese Semantic ist nicht bekannt")

    result_block = block_a * block_b

    if semantic == "gcm":
        result_bytes = result_block.to_bytes(byteorder='big')

    elif semantic == "xex":
        result_bytes = result_block.to_bytes(byteorder='little')   
    else:
        raise ValueError("Diese Semantic ist nicht bekannt")

    result_block_base64 = encode_base64(result_bytes)

    return {"product": result_block_base64}


def calculate_galois_index(i, j, semantic):
    """Berechnet die Galois-Feld-Position basierend auf der Semantik."""
    if semantic == "gcm":
        # GCM-Mapping: alpha^(8 * i + 7 - j)
        return 8 * i + (7 - j)
    elif semantic == "xex":
        # XEX-Mapping: alpha^(8 * i + j)
        return 8 * i + j
    else:
        raise ValueError("Unbekannte Semantik: Muss 'gcm' oder 'xex' sein.")