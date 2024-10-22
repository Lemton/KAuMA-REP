import base64

class GaloisField128Handler:

    REDUCTION_POLYNOMIAL = (1 << 128) | (1 << 7) | (1 << 2) | (1 << 1) | 1

    @staticmethod
    def galois_multiplication(X: int, Y: int) -> int:
        z = 0
        V : int = X
        for i in range(128):
            
            if (Y >> i) & 0x1 == 1:
               
                z = z^V 
                
            if (V >> 127) & 0x1 == 0 :
                
                V <<= 1
                
            else:

                V = ( V << 1 ) ^ GaloisField128Handler.REDUCTION_POLYNOMIAL
                
            
        return z
    
    @staticmethod
    def gfmul(arguments):
        
        print(arguments)

        block_a_base64 = arguments.get("a")
        block_b_base64 = arguments.get("b")

        block_a = base64.b64decode(block_a_base64)
        block_b = base64.b64decode(block_b_base64)

        # Wandle die Blöcke in Integer um
        block_a_int = int.from_bytes(block_a, byteorder='little')
        block_b_int = int.from_bytes(block_b, byteorder='little')

    
        result_block = GaloisField128Handler.galois_multiplication(block_a_int, block_b_int)
        

        result_bytes = result_block.to_bytes(16, byteorder='little')
        
        result_block_base64 = base64.b64encode(result_bytes).decode('utf-8')

        return {"product": result_block_base64}
