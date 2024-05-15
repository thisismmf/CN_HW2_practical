import socket

# Function to handle client requests
def handle_client(client_socket):
    try:
        # Receive data from the client
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            # Process the request (echo back in this example)
            client_socket.sendall(data)
    except Exception as e:
        print(f"Error handling client request: {str(e)}")
    finally:
        client_socket.close()

# Function to start the backend server
def start_backend_server():
    # Create a TCP socket
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a port
    backend_socket.bind(('localhost', 8080))  # You can change the IP and port as needed

    # Listen for incoming connections
    backend_socket.listen(5)
    print("Backend server is listening on port 8080...")

    # Accept incoming connections and handle client requests
    while True:
        client_socket, address = backend_socket.accept()
        print(f"Connection from {address}")
        # Handle the client request in a separate thread
        handle_client(client_socket)

# Start the backend server
start_backend_server()
