from utils.bitops import encode_base64, decode_base64, xor_bytes
from field_element import FieldElement
from utils.aes128 import aes128_encrypt, aes128_decrypt
from handlers.sea128 import SEA128Handler


class GCMHandler: 

    def __init__(self):
        pass
        
    def gcm_encrypt_action(self,arguments): 
        algorithm = arguments.get("algorithm", "")
        nonce = decode_base64(arguments.get("nonce"))
        key = decode_base64(arguments.get("key"))
        plaintext = decode_base64(arguments.get("plaintext"))
        ad = decode_base64(arguments.get("ad"))

        
        result = gcm_encrypt(algorithm, nonce, key, plaintext, ad)
        
        result["ciphertext"] = encode_base64(result["ciphertext"])
        result["tag"] = encode_base64(result["tag"])
        result["L"] = encode_base64(result["L"])
        result["H"] = encode_base64(result["H"])
        
        return result

    
    def gcm_decrypt_action(self, arguments):
        algorithm = arguments.get("algorithm", "")
        nonce = decode_base64(arguments.get("nonce"))
        key = decode_base64(arguments.get("key"))
        ciphertext = decode_base64(arguments.get("ciphertext"))
        ad = decode_base64(arguments.get("ad"))
        tag = decode_base64(arguments.get("tag"))

        
        result = gcm_decrypt(algorithm, nonce, key, ciphertext, ad, tag)
        
        result["plaintext"] = encode_base64(result["plaintext"])
        
        return result



def gcm_encrypt(algorithm, nonce, key, plaintext, ad):
    if algorithm == "sea128":
        sea128 = SEA128Handler()
        authkey = sea128.encrypt(key, b'\x00' * 16)        
    elif algorithm == "aes128":
        authkey = aes128_encrypt(key, b'\x00' * 16)
    else: 
        raise ValueError("Kein bekannter Algorithmus")
    
    y0 = nonce + (1).to_bytes(4, byteorder='big')

    plaintext_blocks = [plaintext[i:i + 16] for i in range(0, len(plaintext), 16)]
    ciphertext_blocks = bytearray()
    
    counter = 2
    for plaintext_block in plaintext_blocks:
        if algorithm == "sea128":
            y_i = sea128.encrypt(key, nonce + counter.to_bytes(4, byteorder='big'))
        elif algorithm == "aes128":
            y_i = aes128_encrypt(key, nonce + counter.to_bytes(4, byteorder='big'))
        
        ciphertext_block = bytearray([p ^ y for p, y in zip(plaintext_block, y_i)])
        ciphertext_blocks.extend(ciphertext_block)
        counter += 1
    
    L = (len(ad) * 8).to_bytes(8, byteorder='big') + (len(ciphertext_blocks) * 8).to_bytes(8, byteorder='big')
    ghash_result = ghash(authkey, [ad[i:i+16] for i in range(0, len(ad), 16)], [ciphertext_blocks[i:i+16] for i in range(0, len(ciphertext_blocks), 16)], L)

    if algorithm == "sea128":
        y0_encrypted = sea128.encrypt(key, y0)
    elif algorithm == "aes128":
        y0_encrypted = aes128_encrypt(key, y0)

    auth_tag = bytearray([y ^ g for y, g in zip(y0_encrypted, ghash_result)])
    
    return {
        "ciphertext": ciphertext_blocks,
        "tag": auth_tag,
        "L": L,
        "H": authkey
    }


def gcm_decrypt(algorithm, nonce, key, ciphertext, ad, tag):

    if algorithm == "sea128":
        sea128 = SEA128Handler()
        authkey = sea128.encrypt(key, b'\x00' * 16)        
    elif algorithm == "aes128":
        authkey = aes128_encrypt(key, b'\x00' * 16)
    else: 
        raise ValueError("Kein bekannter Algorithmus")
    
    y0 = nonce + (1).to_bytes(4, byteorder='big')

    ciphertext_blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
    plaintext_blocks = bytearray()
    
    counter = 2
    for ciphertext_block in ciphertext_blocks:
        if algorithm == "sea128":
            y_i = sea128.encrypt(key, nonce + counter.to_bytes(4, byteorder='big'))
        elif algorithm == "aes128":
            y_i = aes128_encrypt(key, nonce + counter.to_bytes(4, byteorder='big'))
        
        plaintext_block = bytearray([c ^ y for c, y in zip(ciphertext_block, y_i)])
        plaintext_blocks.extend(plaintext_block)
        counter += 1

    L = (len(ad) * 8).to_bytes(8, byteorder='big') + (len(ciphertext) * 8).to_bytes(8, byteorder='big')
    ghash_result = ghash(authkey, [ad[i:i+16] for i in range(0, len(ad), 16)], ciphertext_blocks, L)

    if algorithm == "sea128":
        y0_encrypted = sea128.encrypt(key, y0)
    elif algorithm == "aes128":
        y0_encrypted = aes128_encrypt(key, y0)

    computed_tag = bytearray([y ^ g for y, g in zip(y0_encrypted, ghash_result)])
    authentic = computed_tag == tag

    return {"authentic": authentic, "plaintext": plaintext_blocks}


def ghash(auth_key, associated_data, ciphertext_blocks, L):
    """
    Implementiert die GHASH-Funktion basierend auf der Galois-Feld-Arithmetik.
    Nutzt die Methoden `gcm_from_block` von FieldElement direkt mit den Bytes.
    """
    # Erstelle das initiale GHASH-Ergebnis als FieldElement
    ghash_result = FieldElement(0)

    # Auth-Key in ein FieldElement mit GCM-Semantik konvertieren
    auth_key_fe = FieldElement.gcm_from_block(auth_key)

    # Verarbeitung der Associated Data (AD)
    for block in associated_data:
        # Padding und Konvertierung in ein FieldElement
        padded_block = block + b'\x00' * (16 - len(block))
        block_fe = FieldElement.gcm_from_block(padded_block)

        # XOR und Multiplikation
        ghash_result ^= block_fe
        ghash_result *= auth_key_fe

    # Verarbeitung der Ciphertext-Blöcke
    for block in ciphertext_blocks:
        # Padding und Konvertierung in ein FieldElement
        padded_block = block + b'\x00' * (16 - len(block))
        block_fe = FieldElement.gcm_from_block(padded_block)

        # XOR und Multiplikation
        ghash_result ^= block_fe
        ghash_result *= auth_key_fe

    # Verarbeitung des L-Werts
    L_fe = FieldElement.gcm_from_block(L)
    ghash_result ^= L_fe
    ghash_result *= auth_key_fe

    # Konvertiere das Endergebnis in Bytes
    return FieldElement.gcm_to_block(ghash_result)


