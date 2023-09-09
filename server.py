import socket
import json

from sage.coding.source_coding.huffman import Huffman, frequency_table
from sage.all import ZZ

HOST = '127.0.0.1'
PORT = 12345

def socket_listening():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Our server listens on host: {HOST} and port '{PORT}'")
    return server_socket


def huffman_decompression(message, f_table):
    huffman = Huffman(f_table)

    # return message
    return huffman.decode(message)


def main():
    server_socket = socket_listening()
    
    connection, client_address = server_socket.accept()


    try:
        while True:
            data = connection.recv(1024)

            if not data:
                break
            
            received_data = json.loads(data.decode('utf-8'))

            compressed_message = received_data['message']
            parameters = received_data['parameters']

            f_table = parameters[0]

            message = huffman_decompression(compressed_message, f_table)

            # data to send back to client
            response_data = {
                "message": message
            }

            response_json = json.dumps(response_data)
            connection.sendall(response_json.encode('utf-8'))
            
    finally:
        connection.close()
        server_socket.close()

    print("Server completed the task. Goodbye!")

if __name__ == "__main__":
     main()
