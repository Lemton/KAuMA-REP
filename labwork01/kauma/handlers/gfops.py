from field_element import FieldElement
import base64

def gfmul(arguments):
    """
    Führt die Galois-Field-Multiplikation (GFMUL) aus, basierend auf der Semantik (GCM oder XEX).
    """
    block_a_base64 = arguments.get("a")
    block_b_base64 = arguments.get("b")
    semantic = arguments.get("semantic", "")

    # Dekodiere die Base64-Blöcke in Bytes
    block_a_bytes = base64.b64decode(block_a_base64)
    block_b_bytes = base64.b64decode(block_b_base64)

    if semantic == "gcm":
        # Erstelle FieldElemente mit der GCM-Semantik
        field_a = FieldElement.gcm_from_block(block_a_bytes)
        field_b = FieldElement.gcm_from_block(block_b_bytes)

        # Galois-Feld-Multiplikation durchführen
        result = field_a * field_b

        # Konvertiere das Ergebnis zurück in Bytes mit der GCM-Semantik
        result_block_bytes = FieldElement.gcm_to_block(result.value)

    elif semantic == "xex":
        # Erstelle FieldElemente mit der XEX-Semantik
        field_a = FieldElement.xex_from_block(block_a_bytes)
        field_b = FieldElement.xex_from_block(block_b_bytes)

        # Galois-Feld-Multiplikation durchführen
        result = field_a * field_b

        # Konvertiere das Ergebnis zurück in Bytes mit der XEX-Semantik
        result_block_bytes = FieldElement.xex_to_block(result.value)

    else:
        raise ValueError("Diese Semantik ist nicht bekannt")

    # Ergebnis zurück in Base64 kodieren
    result_block_base64 = base64.b64encode(result_block_bytes).decode("utf-8")
    return {"product": result_block_base64}

def gfdiv(arguements):
    block_a_base64 = arguements.get("a")
    block_b_base64 = arguements.get("b")

    block_a_bytes = base64.b64decode(block_a_base64)
    block_b_bytes = base64.b64decode(block_b_base64)
    
    counter = FieldElement.gcm_from_block(block_a_bytes)
    nominator = FieldElement.gcm_from_block(block_b_bytes)

    result_int = counter / nominator

    result_block_bytes = FieldElement.gcm_to_block(result_int)

    result = base64.b64encode(result_block_bytes).decode("utf-8")
    return {"q": result}

