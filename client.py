import socket
import json
from sage.coding.source_coding.huffman import Huffman, frequency_table
from sage.all import ZZ

HOST = '127.0.0.1'
PORT = 12345


    
# helping method to convert python tuple to list
def convert_tuple_to_list(t):
    return ''.join([ str(i) for i in t])

# helping method to create client socket using specific HOST, PORT
def socket_connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    client_socket.connect(server_address)

    return client_socket

# helping method for Huffman code
def huffman_compression(message):
    # create the frequency table from message
    f_table = frequency_table(message)

    # create Huffman using the frequency table
    huffman = Huffman(f_table)

    # return compressed message
    return (huffman.encode(message), f_table)


def main():
    # This is the client socket to talk with the server
    client_socket = socket_connect()

    # Read from the input file
    with open("input_file.txt", "r") as file:
        message = file.read()

    # Compress message from file using Huffman code from sagemath
    compressed_message, f_table = huffman_compression(message)
    print("Compressed message using Huffman Code (from sagemath):", compressed_message, len(compressed_message))

    data_to_send = {
        "message": compressed_message,
        "parameters": [f_table]
    }

    json_data = json.dumps(data_to_send)

    client_socket.sendall(json_data.encode('utf-8'))

    response = client_socket.recv(1024)
    response_data = json.loads(response.decode('utf-8'))
    print("Server Response:", response_data['message'])

if __name__ == "__main__":
     main()