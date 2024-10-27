import base64
from handlers.sea128 import SEA128Handler
from handlers.GaloisField128 import GaloisField128Handler



class FDEHandler:
    
    @staticmethod
    def xex(arguments):

        if arguments['mode'] == 'encrypt':
            return {"output": FDEHandler.xexencrypt(arguments)}
        elif arguments['mode'] == 'decrypt':
            return {"output": FDEHandler.xexdecrypt(arguments)}
        else:
            raise ValueError("Invalid mode, must be 'encrypt' or 'decrypt'.")

    def xexencrypt(arguments):
        
        tweak = arguments.get('tweak')
        key1n2 = arguments.get('key')
        plaintext = arguments.get('input')
    
        tweakdecode = base64.b64decode(tweak)

        key1, key2 = FDEHandler.decodeKey_Split(key1n2)    
        tocipherblocks = FDEHandler.decodeInput_Split(plaintext) 
        iv_bytes = SEA128Handler.sea128encrypt(key2, tweakdecode)
        CipherBlocks = bytearray()

        for block in tocipherblocks:
            block1 = bytearray()
            for i in range(0,16):
                block1.append(block[i] ^ iv_bytes[i])

            block1 = bytes(block1)
            
            block1_SEA = SEA128Handler.sea128encrypt(key1, block1)

            block1_Ciph = bytearray()
            for i in range(0,16):
                block1_Ciph.append(block1_SEA[i] ^ iv_bytes[i])

            CipherBlocks.extend(block1_Ciph)
            
            
            
            iv = int.from_bytes(iv_bytes, byteorder='little')
            iv = GaloisField128Handler.galois_multiplication(iv, 2)
            iv_bytes = iv.to_bytes(length=16, byteorder='little')    

        CipherBlocks = base64.b64encode(CipherBlocks).decode('utf-8')
        output = ''.join(CipherBlocks)
        
        return output

    def xexdecrypt(arguments):
        
        tweak = arguments.get('tweak')
        key1n2 = arguments.get('key')
        plaintext = arguments.get('input')
    
        tweakdecode = base64.b64decode(tweak)

        key1, key2 = FDEHandler.decodeKey_Split(key1n2)    
        tocipherblocks = FDEHandler.decodeInput_Split(plaintext) 
        iv_bytes = SEA128Handler.sea128encrypt(key2, tweakdecode)
        CipherBlocks = bytearray()

        for block in tocipherblocks:
            block1 = bytearray()
            for i in range(0,16):
                block1.append(block[i] ^ iv_bytes[i])

            block1 = bytes(block1)
            
            block1_SEA = SEA128Handler.sea128decrypt(key1, block1)

            block1_Ciph = bytearray()
            for i in range(0,16):
                block1_Ciph.append(block1_SEA[i] ^ iv_bytes[i])

            CipherBlocks.extend(block1_Ciph)
            
            
            
            iv = int.from_bytes(iv_bytes, byteorder='little')
            iv = GaloisField128Handler.galois_multiplication(iv, 2)
            iv_bytes = iv.to_bytes(length=16, byteorder='little')    

        CipherBlocks = base64.b64encode(CipherBlocks).decode('utf-8')
        output = ''.join(CipherBlocks)
        
        return output
    
    def decodeKey_Split(keystr):

        key = base64.b64decode(keystr)

        
        if len(key) != 32:
            raise ValueError("Der dekodierte Schlüssel ist nicht genau 256 Bit groß.")
        
        key1 = key[:16]
        key2 = key[16:]

        return key1,key2
    
    def decodeInput_Split(input):
        block_size = 16
        inputdecoded = base64.b64decode(input)
        blocks = [inputdecoded[i:i + block_size]for i in range(0, len(inputdecoded),block_size)]

        return blocks

        
        
        