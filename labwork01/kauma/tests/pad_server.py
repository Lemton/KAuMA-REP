import socket
import struct

def check_padding(data):
    # Assumes data is already decrypted plaintext
    if not data:
        return False
    padding_value = data[-1]
    if padding_value < 1 or padding_value > 16:
        return False
    # Check if the padding bytes are correct
    return data[-padding_value:] == bytes([padding_value]) * padding_value

def handle_client(client_socket):
    try:
        # Receive the initial 16-byte ciphertext
        ciphertext = client_socket.recv(16)
        if len(ciphertext) != 16:
            client_socket.close()
            return

        while True:
            # Receive 2-byte length field in little endian
            length_field = client_socket.recv(2)
            if len(length_field) != 2:
                break
            l = struct.unpack('<H', length_field)[0]  # Convert to integer
            if l == 0:
                break  # Terminate connection if l == 0

            # Receive l * 16 bytes of Q-blocks
            q_blocks = client_socket.recv(l * 16)
            if len(q_blocks) != l * 16:
                break

            # Process each Q-block and check padding
            responses = []
            for i in range(l):
                block = q_blocks[i * 16:(i + 1) * 16]
                # For demonstration, assume "decryption" step happens here
                # In real-world usage, replace this with actual decryption logic
                decrypted_block = block  # Dummy logic; replace with actual decryption
                if check_padding(decrypted_block):
                    responses.append(0x01)  # Correct padding
                else:
                    responses.append(0x00)  # Incorrect padding

            # Send l-byte response back to client
            client_socket.send(bytes(responses))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Padding Oracle Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server.close()

if __name__ == "__main__":
    HOST = "0.0.0.0"  # Listen on all available interfaces
    PORT = 18652
    start_server(HOST, PORT)
