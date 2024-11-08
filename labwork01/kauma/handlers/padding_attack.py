import socket
import struct
from utils.conversions import encode_base64, decode_base64

BLOCK_SIZE = 16
TIMEOUT = 10.0
BATCH_SIZE = 64

class PaddingOracleClient:
    def __init__(self, target_host, target_port):
        self.connection = socket.create_connection((target_host, target_port), timeout=TIMEOUT)
    
    def initialize(self, initial_block):
        if len(initial_block) != BLOCK_SIZE:
            raise ValueError("Initial block must be exactly 16 bytes")
        self.connection.sendall(initial_block)
    
    def query(self, blocks):
        try:
            packed_data = struct.pack('<H', len(blocks)) + b''.join(blocks)
            self.connection.sendall(packed_data)
            response = self.connection.recv(len(blocks))
            if not response:
                raise ConnectionError("Empty response received from server.")
            return response
        except BrokenPipeError:
            self.close()
            raise ConnectionError("Connection broken. Ensure the server is running and reachable.")
    
    def close(self):
        self.connection.close()


class BlockDecryptor:
    def __init__(self, cipher_block, previous_block, oracle_client):
        self.cipher_block = cipher_block
        self.previous_block = bytearray(previous_block)
        self.oracle_client = oracle_client
        self.decrypted_intermediate = bytearray(BLOCK_SIZE)
        self.decrypted_plaintext = bytearray(BLOCK_SIZE)
        self.padding_position = BLOCK_SIZE - 1
        self.padding_value = 1

    def brute_force_candidates(self):
        return [self.previous_block[:self.padding_position] + bytes([candidate]) + self.previous_block[self.padding_position + 1:] for candidate in range(256)]

    def valid_responses(self, batch):
        responses = self.oracle_client.query(batch)
        return [batch[i] for i, result in enumerate(responses) if result == 0x01]

    def resolve_ambiguity(self, candidates):
        altered_candidates = [c[:self.padding_position - 1] + bytes([c[self.padding_position - 1] ^ 0xFF]) + c[self.padding_position:] for c in candidates]
        return self.valid_responses(altered_candidates)

    def find_valid_byte(self):
        while True:
            for batch_start in range(0, 256, BATCH_SIZE):
                batch = self.brute_force_candidates()[batch_start: batch_start + BATCH_SIZE]
                candidates = self.valid_responses(batch)
                
                if len(candidates) == 1:
                    return candidates[0]
                elif len(candidates) > 1:
                    resolved_candidates = self.resolve_ambiguity(candidates)
                    if resolved_candidates:
                        return resolved_candidates[0]

    def decrypt_block(self):
        self.oracle_client.initialize(self.cipher_block)

        while self.padding_position >= 0:
            candidate = self.find_valid_byte()
            self.decrypted_intermediate[self.padding_position] = candidate[self.padding_position] ^ self.padding_value
            self.decrypted_plaintext[self.padding_position] = self.decrypted_intermediate[self.padding_position] ^ self.previous_block[self.padding_position]
            self.padding_position -= 1
            self.padding_value += 1
            for i in range(1, self.padding_value):
                self.previous_block[-i] = self.decrypted_intermediate[-i] ^ self.padding_value
        
        return bytes(self.decrypted_plaintext)


def decrypt_ciphertext(arguments):
    host, port = arguments.get("hostname"), arguments.get("port")
    iv, ciphertext = decode_base64(arguments.get("iv")), decode_base64(arguments.get("ciphertext"))

    decrypted_text = bytearray()
    cipher_blocks = [iv] + [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    
    for index in range(1, len(cipher_blocks)):
        oracle_client = PaddingOracleClient(host, port)
        decryptor = BlockDecryptor(cipher_blocks[index], cipher_blocks[index - 1], oracle_client)
        
        try:
            decrypted_text.extend(decryptor.decrypt_block())
        except Exception as e:
            print(f"Error decrypting block {index}: {e}")
            oracle_client.close()
            raise
        
        oracle_client.close()

    
    return {"plaintext": encode_base64(bytes(decrypted_text))}
