from utils.conversions import encode_base64, decode_base64, xor_bytes
from field_element import FieldElement
from utils.crypto import gcm_encrypt, gcm_decrypt

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
