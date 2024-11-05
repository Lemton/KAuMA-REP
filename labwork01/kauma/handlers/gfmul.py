from utils.conversions import encode_base64, decode_base64, reverse_bit_order
from field_element import FieldElement


def gfmul(arguments):
    block_a_base64 = arguments.get("a")
    block_b_base64 = arguments.get("b")
    semantic = arguments.get("semantic", "")
    
    
    block_a_bytes = decode_base64(block_a_base64)
    block_b_bytes = decode_base64(block_b_base64)



    if semantic == "gcm":
        
        result_bytes = gcm_gfmul(block_a_bytes, block_b_bytes)

    elif semantic == "xex":
        
        result_bytes = xex_gfmul(block_a_bytes, block_b_bytes)
    else:
        raise ValueError("Diese Semantik ist nicht bekannt")
   
    result_block_base64 = encode_base64(result_bytes)

    return {"product": result_block_base64}


def gcm_gfmul(block_a_bytes, block_b_bytes):
    
    block_a_reversed = reverse_bit_order(block_a_bytes)
    block_b_reversed = reverse_bit_order(block_b_bytes)
    
    
    block_a = FieldElement(int.from_bytes(block_a_reversed, byteorder='little'))
    block_b = FieldElement(int.from_bytes(block_b_reversed, byteorder='little'))

    result_block = block_a * block_b

    result_bytes = reverse_bit_order(result_block.to_bytes(16, byteorder='little'))

    return result_bytes

def xex_gfmul(block_a_bytes, block_b_bytes):
    
    block_a = FieldElement(int.from_bytes(block_a_bytes, byteorder='little'))
    block_b = FieldElement(int.from_bytes(block_b_bytes, byteorder='little'))

    result_block = block_a * block_b

    result_bytes = result_block.to_bytes(16, byteorder='little')

    return result_bytes