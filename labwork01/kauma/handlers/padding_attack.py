import socket
import struct
import base64
from utils.conversions import decode_base64

def padding_oracle(arguments):
    hostname = arguments.get("hostname")
    port = arguments.get("port")
    iv = decode_base64(arguments.get("iv"))
    ciphertext = decode_base64(arguments.get("ciphertext"))

    plaintext = padding_oracle_attack(hostname, port, iv, ciphertext)
    print({"plaintext": base64.b64encode(plaintext).decode()})

def connect_to_server(hostname, port, initial_ciphertext, q_blocks):
    """Connects to the padding oracle server, sends data, and receives responses."""
    with socket.create_connection((hostname, port)) as sock:
        
        data_to_send = initial_ciphertext + struct.pack('<H', len(q_blocks)) + b''.join(q_blocks)
        sock.sendall(data_to_send)

        response = sock.recv(len(q_blocks))
        return response

def padding_oracle_attack(hostname, port, iv, ciphertext):
    """Performs the padding oracle attack to decrypt the given ciphertext."""
    block_size = 16  
    ciphertext_blocks = [iv] + [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    decrypted = bytearray()

    for block_index in range(1, len(ciphertext_blocks)):
        current_block = ciphertext_blocks[block_index]
        previous_block = bytearray(ciphertext_blocks[block_index - 1])
        intermediate = bytearray(block_size)
        decrypted_block = bytearray(block_size)

        for byte_index in range(block_size - 1, -1, -1):
            padding_value = block_size - byte_index

            # Modify bytes for expected padding
            for i in range(byte_index + 1, block_size):
                previous_block[i] = intermediate[i] ^ padding_value

            # Try each byte value
            found = False
            for guess in range(256):
                original_byte = previous_block[byte_index]
                previous_block[byte_index] = guess

                # Send modified data and receive response
                try:
                    response = connect_to_server(hostname, port, current_block, [bytes(previous_block)])
                    if response[0] == 1:  # Valid padding
                        print(f"Found valid padding for byte_index {byte_index}: guess {guess}")
                        intermediate[byte_index] = guess ^ padding_value
                        decrypted_block[byte_index] = intermediate[byte_index] ^ original_byte
                        found = True
                        break
                except Exception as e:
                    print(f"Error communicating with server: {e}")
                    continue

                # Restore original byte if guess was incorrect
                previous_block[byte_index] = original_byte

        if not found:
            raise Exception(f"Failed to find valid padding byte at byte index {byte_index}.")

        decrypted.extend(decrypted_block)

    return decrypted
