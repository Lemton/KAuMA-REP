from handlers.sea128 import *
from utils.conversions import encode_base64, decode_base64, xor_bytes
from field_element import FieldElement

class FDEHandler:
    def __init__(self):
        self.sea128 = SEA128Handler()
        self.galois_multiplier = FieldElement(2)  # Multiplikator für Galois-Feld

    def xex(self, arguments):
        if arguments['mode'] == 'encrypt':
            return {"output": self.encrypt(arguments)}
        elif arguments['mode'] == 'decrypt':
            return {"output": self.decrypt(arguments)}
        else:
            raise ValueError("Invalid mode, must be 'encrypt' or 'decrypt'.")

    def encrypt(self, arguments):
        tweak_base64 = arguments.get('tweak')
        concatenated_keys_base64 = arguments.get('key')
        plaintext_base64 = arguments.get('input')

        tweak = decode_base64(tweak_base64)
        key1, key2 = self.split_keys(concatenated_keys_base64)
        plaintext_blocks = self.split_input_into_blocks(plaintext_base64)

        iv_encrypted = self.sea128.encrypt(key2, tweak)
        encrypted_blocks = bytearray()

        
        iv = FieldElement(int.from_bytes(iv_encrypted, byteorder='little'))

        for plaintext_block in plaintext_blocks:
            
            xored_block = xor_bytes(plaintext_block, iv.to_bytes(byteorder='little'))
            encrypted_block = self.sea128.encrypt(key1, xored_block)
            final_encrypted_block = xor_bytes(encrypted_block, iv.to_bytes(byteorder='little'))
            encrypted_blocks.extend(final_encrypted_block)

            
            iv *= self.galois_multiplier

        return encode_base64(encrypted_blocks)

    def decrypt(self, arguments):
        tweak_base64 = arguments.get('tweak')
        concatenated_keys_base64 = arguments.get('key')
        ciphertext_base64 = arguments.get('input')

        tweak = decode_base64(tweak_base64)
        key1, key2 = self.split_keys(concatenated_keys_base64)
        ciphertext_blocks = self.split_input_into_blocks(ciphertext_base64)

        iv_encrypted = self.sea128.encrypt(key2, tweak)
        decrypted_blocks = bytearray()

        
        iv = FieldElement(int.from_bytes(iv_encrypted, byteorder='little'))

        for ciphertext_block in ciphertext_blocks:
            
            xored_block = xor_bytes(ciphertext_block, iv.to_bytes(byteorder='little'))
            decrypted_block = self.sea128.decrypt(key1, xored_block)
            final_decrypted_block = xor_bytes(decrypted_block, iv.to_bytes(byteorder='little'))
            decrypted_blocks.extend(final_decrypted_block)

            
            iv *= self.galois_multiplier

        return encode_base64(decrypted_blocks)

    def split_keys(self, concatenated_keys_base64):
        """Teilt den 256-Bit-Schlüssel in zwei 128-Bit-Schlüssel auf."""
        concatenated_keys = decode_base64(concatenated_keys_base64)
        if len(concatenated_keys) != 32:
            raise ValueError("Der dekodierte Schlüssel muss genau 256 Bit lang sein.")
        return concatenated_keys[:16], concatenated_keys[16:]

    def split_input_into_blocks(self, input_data_base64):
        """Teilt die Eingabedaten in 128-Bit-Blöcke auf."""
        block_size = 16
        input_data = decode_base64(input_data_base64)
        return [input_data[i:i + block_size] for i in range(0, len(input_data), block_size)]
