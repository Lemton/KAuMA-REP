from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from field_element import FieldElement
from handlers.gfmul import gcm_gfmul


def aes128_encrypt(key: bytes, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def aes128_decrypt(key: bytes, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def gcm_encrypt(algorithm, nonce, key, plaintext, ad):
    from handlers.sea128 import SEA128Handler
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
        
        ciphertext_block = bytes([p ^ y for p, y in zip(plaintext_block, y_i)])
        ciphertext_blocks.extend(ciphertext_block)
        counter += 1
    
    L = (len(ad) * 8).to_bytes(8, byteorder='big') + (len(ciphertext_blocks) * 8).to_bytes(8, byteorder='big')
    ghash_result = ghash(authkey, ad, ciphertext_blocks, L)

    if algorithm == "sea128":
        y0_encrypted = sea128.encrypt(key, y0)
    elif algorithm == "aes128":
        y0_encrypted = aes128_encrypt(key, y0)

    auth_tag = bytes([y ^ g for y, g in zip(y0_encrypted, ghash_result)])
    
    return {
        "ciphertext": ciphertext_blocks,
        "tag": auth_tag,
        "L": L,
        "H": authkey
    }


def gcm_decrypt(algorithm, nonce, key, ciphertext, ad, tag):
    from handlers.sea128 import SEA128Handler
    
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
        
        plaintext_block = bytes([c ^ y for c, y in zip(ciphertext_block, y_i)])
        plaintext_blocks.extend(plaintext_block)
        counter += 1

    L = (len(ad) * 8).to_bytes(8, byteorder='big') + (len(ciphertext) * 8).to_bytes(8, byteorder='big')
    ghash_result = ghash(authkey, ad, ciphertext_blocks, L)

    if algorithm == "sea128":
        y0_encrypted = sea128.encrypt(key, y0)
    elif algorithm == "aes128":
        y0_encrypted = aes128_encrypt(key, y0)

    computed_tag = bytes([y ^ g for y, g in zip(y0_encrypted, ghash_result)])
    authentic = computed_tag == tag

    return {"authentic": authentic,"plaintext": plaintext_blocks}


def ghash(auth_key, associated_data, ciphertext_blocks, L):
    ghash_result = FieldElement(0)
    auth_key_bytes = auth_key if isinstance(auth_key, bytes) else auth_key.to_bytes(16, byteorder='big')
    
    
    for i in range(0, len(associated_data), 16):
        block = associated_data[i:i + 16]
        block = block.ljust(16, b'\x00')
        block_fe = FieldElement(int.from_bytes(block, byteorder='big'))
        ghash_result ^= block_fe
        ghash_result = FieldElement(int.from_bytes(gcm_gfmul(ghash_result.to_bytes(16, byteorder='big'), auth_key_bytes), byteorder='big'))
    
    
    for i in range(0, len(ciphertext_blocks), 16):
        block = ciphertext_blocks[i:i + 16]
        block = block.ljust(16, b'\x00')
        block_fe = FieldElement(int.from_bytes(block, byteorder='big'))
        ghash_result ^= block_fe
        ghash_result = FieldElement(int.from_bytes(gcm_gfmul(ghash_result.to_bytes(16, byteorder='big'), auth_key_bytes), byteorder='big'))
    
    
    L_fe = FieldElement(int.from_bytes(L, byteorder='big'))
    ghash_result ^= L_fe
    ghash_result = FieldElement(int.from_bytes(gcm_gfmul(ghash_result.to_bytes(16, byteorder='big'), auth_key_bytes), byteorder='big'))

    return ghash_result.to_bytes(16, byteorder='big')
