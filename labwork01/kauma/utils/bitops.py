import base64

def xor_bytes(data1, data2):
    
    return bytes(map(lambda x: x[0] ^ x[1], zip(data1, data2)))

def reverse_bit_order(byte_array):
    
    REVERSE_LOOKUP = [int('{:08b}'.format(i)[::-1], 2) for i in range(256)]
    
    return bytearray(REVERSE_LOOKUP[byte] for byte in byte_array)

def encode_base64(data):
    return base64.b64encode(data).decode('utf-8')

def decode_base64(data):
    return base64.b64decode(data)