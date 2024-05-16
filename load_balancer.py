import socket
import threading
import time

# Global variables for server list, current server index, and lock for thread safety
SERVER_LIST = [("127.0.0.1", 8000), ("127.0.0.1", 8001), ("127.0.0.1", 8002)]  # Example list of backend servers
CURRENT_SERVER_INDEX = 0
LOCK = threading.Lock()


def handle_client_connection(client_socket):
    """
    Function to handle incoming client connections
    """
    global CURRENT_SERVER_INDEX

    # Acquire lock for thread safety when accessing CURRENT_SERVER_INDEX
    with LOCK:
        # Get the next server from the list using Round Robin algorithm
        server_address = SERVER_LIST[CURRENT_SERVER_INDEX]
        CURRENT_SERVER_INDEX = (CURRENT_SERVER_INDEX + 1) % len(SERVER_LIST)

    # Log the request forwarding
    print(f"Forwarding request to server at {server_address}")

    # Connect to the selected backend server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(server_address)

    # Forward the client request to the backend server
    request = client_socket.recv(1024)
    server_socket.send(request)

    # Receive the response from the backend server
    response = server_socket.recv(1024)

    # Send the response back to the client
    client_socket.send(response)

    # Close the sockets
    server_socket.close()
    client_socket.close()


def health_check():
    """
    Function to perform health checks on backend servers
    """
    while True:
        # Iterate through the server list and check the health of each server
        for server_address in SERVER_LIST:
            try:
                # Attempt to connect to the server
                health_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                health_socket.connect(server_address)
                health_socket.close()
                print(f"Server at {server_address} is healthy")
            except:
                # If connection fails, remove the server from the list
                print(f"Server at {server_address} is unreachable. Removing from the list.")
                with LOCK:
                    SERVER_LIST.remove(server_address)

        # Wait for a specified interval before performing the next health check
        time.sleep(60)


def start_load_balancer():
    """
    Function to start the load balancer
    """
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lb_socket:
        # Bind the socket to the localhost and a port
        lb_socket.bind(('127.0.0.1', 9000))  # Example port, you can change this as needed

        # Listen for incoming connections
        lb_socket.listen(5)
        print("Load balancer listening on port 9000...")

        # Start the health check thread
        health_thread = threading.Thread(target=health_check)
        health_thread.daemon = True  # Set the thread as a daemon so it terminates when the main program exits
        health_thread.start()

        # Main server loop: accept incoming connections and handle them
        while True:
            # Accept a client connection
            client_socket, client_address = lb_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Handle the client connection in a separate thread (optional)
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
            client_thread.start()


if __name__ == "__main__":
    start_load_balancer()