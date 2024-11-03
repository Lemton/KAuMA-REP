from utils.conversions import encode_base64, decode_base64  # Nutze die Hilfsfunktionen
from field_element import FieldElement

def gfmul(arguments):
    block_a_base64 = arguments.get("a")
    block_b_base64 = arguments.get("b")

    # Dekodiere die Blöcke von Base64 in Bytes und erstelle FieldElement-Objekte
    block_a = FieldElement(int.from_bytes(decode_base64(block_a_base64), byteorder='little'))
    block_b = FieldElement(int.from_bytes(decode_base64(block_b_base64), byteorder='little'))

    # Multipliziere die FieldElement-Objekte
    result_block = block_a * block_b

    # Konvertiere das Ergebnis in Base64 und gebe es zurück
    result_block_base64 = encode_base64(result_block.to_bytes())

    return {"product": result_block_base64}
