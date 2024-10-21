import base64

class PolynomialHandler:
    """Handler für die Umwandlung eines Polynoms in einen 16-Byte-Binärblock."""
    
    @staticmethod
    def poly2block(arguments):
        coefficients = arguments.get("coefficients", [])
        semantic = arguments.get("semantic", "")

        if semantic != "xex":
            raise ValueError(f"Unbekannte Semantik: {semantic}")
        
        block = bytearray(16)

        # Umwandlung der Koeffizienten in Little-Endian-Reihenfolge
        for coeff in coefficients:
            if coeff < 0 or coeff >= 128:
                raise ValueError("Koeffizient muss im Bereich [0, 127] sein.")
            
            # Setze den Koeffizienten auf die richtige Position im 16-Byte-Block
            # coeff gibt die Position des Bits an (Polynompotenzen)
            byte_pos = coeff // 8  # Position im Bytearray
            bit_pos = coeff % 8    # Position im Byte

            # Setze das Bit an der entsprechenden Position (Little Endian)
            block[byte_pos] |= (1 << bit_pos)

        # Den 16-Byte-Block in Base64 kodieren und zurückgeben
        block_base64 = base64.b64encode(block).decode('utf-8')

        return {"block": block_base64}
