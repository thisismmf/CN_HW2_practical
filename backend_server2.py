import socket

# Define the host and port on which the backend server will listen for requests
HOST = '127.0.0.1'  # Loopback address for localhost
PORT = 8001  # Example port, you can change this as needed


def handle_client_connection(client_socket):
    """
    Function to handle incoming client connections
    """
    # Receive data from the client
    request = client_socket.recv(1024).decode('utf-8')

    # Process the request (replace this with your own processing logic)
    response = "Hello from the backend server! Your request: " + request

    # Send the response back to the client
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


def start_server():
    """
    Function to start the backend server
    """
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen(5)
        print(f"Backend server listening on {HOST}:{PORT}")

        # Server loop: accept incoming connections and handle them
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Handle the client connection in a separate thread (optional)
            handle_client_connection(client_socket)


if __name__ == "__main__":
    start_server()
