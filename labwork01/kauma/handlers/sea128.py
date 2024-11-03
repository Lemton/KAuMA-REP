from utils.conversions import encode_base64, decode_base64, xor_bytes
from utils.crypto import aes128_encrypt, aes128_decrypt  


class SEA128Handler:
    def __init__(self):
        self.COFFEE_CONSTANT: bytes = bytes.fromhex("c0ffeec0ffeec0ffeec0ffeec0ffee11")

    def xor_with_coffee_constant(self, data: bytes) -> bytes:
        return xor_bytes(data, self.COFFEE_CONSTANT)

    def encrypt(self, key: bytes, plaintext: bytes) -> bytes:
        encrypted = aes128_encrypt(key, plaintext)
        sea_encrypted = self.xor_with_coffee_constant(encrypted)
        return sea_encrypted

    def decrypt(self, key: bytes, ciphertext: bytes) -> bytes:
        decrypted_xored = self.xor_with_coffee_constant(ciphertext)
        sea_decrypted = aes128_decrypt(key, decrypted_xored)
        return sea_decrypted

    def sea128(self, arguments: dict) -> dict:
        key = decode_base64(arguments['key'])
        input_data = decode_base64(arguments['input'])
        if arguments['mode'] == 'encrypt':
            output = encode_base64(self.encrypt(key, input_data))
            return {"output": output}
        elif arguments['mode'] == 'decrypt':
            output = encode_base64(self.decrypt(key, input_data))
            return {"output": output}
        else:
            raise ValueError("Invalid mode, must be 'encrypt' or 'decrypt'.")
