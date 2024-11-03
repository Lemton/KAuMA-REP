from utils.conversions import encode_base64, decode_base64, reverse_bit_order
from field_element import FieldElement


def gfmul(arguments):
    block_a_base64 = arguments.get("a")
    block_b_base64 = arguments.get("b")
    semantic = arguments.get("semantic", "")
    
    # Dekodiere die Blöcke von Base64 in Bytes
    block_a_bytes = decode_base64(block_a_base64)
    block_b_bytes = decode_base64(block_b_base64)

    if semantic == "gcm":
        # GCM-Semantik: Bits in jedem Byte umkehren, dann als Big-Endian interpretieren
        block_a_reversed = reverse_bit_order(block_a_bytes)
        block_b_reversed = reverse_bit_order(block_b_bytes)
        
        # Konvertiere die umgekehrten Bytes in FieldElement
        block_a = FieldElement(int.from_bytes(block_a_reversed, byteorder='little'))
        block_b = FieldElement(int.from_bytes(block_b_reversed, byteorder='little'))

    elif semantic == "xex":
        # XEX-Semantik: Interpretiere die Bytes direkt als Little-Endian
        block_a = FieldElement(int.from_bytes(block_a_bytes, byteorder='little'))
        block_b = FieldElement(int.from_bytes(block_b_bytes, byteorder='little'))
    else:
        raise ValueError("Diese Semantik ist nicht bekannt")

    # Multipliziere die beiden FieldElemente im Galois-Feld
    result_block = block_a * block_b

    # Konvertiere das Ergebnis zurück in Bytes
    if semantic == "gcm":
        # GCM: Ergebnis in Big-Endian konvertieren und die Bits jedes Bytes umkehren
        result_bytes = reverse_bit_order(result_block.to_bytes(16, byteorder='little'))
    elif semantic == "xex":
        # XEX: Ergebnis in Little-Endian konvertieren, ohne Bit-Umkehrung
        result_bytes = result_block.to_bytes(16, byteorder='little')
    else:
        raise ValueError("Diese Semantik ist nicht bekannt")

    # Kodierung des Ergebnisses in Base64
    result_block_base64 = encode_base64(result_bytes)

    return {"product": result_block_base64}
