from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

class SEA128Handler:
    COFFEE_CONSTANT = bytes.fromhex("c0ffeec0ffeec0ffeec0ffeec0ffee11")

    @staticmethod
    def aes128_encrypt(key, data):
        
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def aes128_decrypt(key, data):
        
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()

    @staticmethod
    def xor_with_coffee_constant(data):
        
        return bytes(a ^ b for a, b in zip(data, SEA128Handler.COFFEE_CONSTANT))

    @staticmethod
    def sea128encrypt(arguments):
        
        key = base64.b64decode(arguments['key'])
        plaintext = base64.b64decode(arguments['input'])
        
        encrypted = SEA128Handler.aes128_encrypt(key, plaintext)
        
        sea_encrypted = SEA128Handler.xor_with_coffee_constant(encrypted)
        
        return base64.b64encode(sea_encrypted).decode('utf-8')

    @staticmethod	
    def sea128decrypt(arguments):
        
        key = base64.b64decode(arguments['key'])
        ciphertext = base64.b64decode(arguments['input'])
        
        decrypted_xored = SEA128Handler.xor_with_coffee_constant(ciphertext)
        
        decrypted = SEA128Handler.aes128_decrypt(key, decrypted_xored)
        
        return base64.b64encode(decrypted).decode('utf-8')

    def sea128(arguments):
        if arguments['mode'] == 'encrypt':
            return {"output": SEA128Handler.sea128encrypt(arguments)}
        elif arguments['mode'] == 'decrypt':
            return {"output": SEA128Handler.sea128decrypt(arguments)}
        else:
            raise ValueError("Invalid mode, must be 'encrypt' or 'decrypt'.")




        
