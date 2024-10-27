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
    def sea128encrypt(key, plaintext):

        encrypted = SEA128Handler.aes128_encrypt(key, plaintext)

        sea_encrypted = SEA128Handler.xor_with_coffee_constant(encrypted)
        
        return sea_encrypted

    @staticmethod	
    def sea128decrypt(key, ciphertext):
        
        decrypted_xored = SEA128Handler.xor_with_coffee_constant(ciphertext)
        
        sea_decrypted = SEA128Handler.aes128_decrypt(key, decrypted_xored)
        
        return sea_decrypted

    def sea128(arguments):
        key = base64.b64decode(arguments['key'])
        input = base64.b64decode(arguments['input'])
        if arguments['mode'] == 'encrypt':
            output = base64.b64encode(SEA128Handler.sea128encrypt(key, input)).decode('utf-8')
            return {"output": output}
        elif arguments['mode'] == 'decrypt':
            output = base64.b64encode(SEA128Handler.sea128decrypt(key, input)).decode('utf-8')
            return {"output": output}
        else:
            raise ValueError("Invalid mode, must be 'encrypt' or 'decrypt'.")



        
