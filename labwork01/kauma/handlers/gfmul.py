import base64
from field_element import FieldElement



def gfmul(arguments):

    block_a_base64 = arguments.get("a")
    block_b_base64 = arguments.get("b")

    block_a = base64.b64decode(block_a_base64)
    block_b = base64.b64decode(block_b_base64)

    # Wandle die Blöcke in Integer um
    block_a_int = FieldElement(int.from_bytes(block_a, byteorder='little'))
    block_b_int = FieldElement(int.from_bytes(block_b, byteorder='little'))


    result_block = block_a_int * block_b_int
    

    result_bytes = result_block.to_bytes()
    
    result_block_base64 = base64.b64encode(result_bytes).decode('utf-8')

    return {"product": result_block_base64}
