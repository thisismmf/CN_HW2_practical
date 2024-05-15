import socket
import threading
import time

# Define the configuration file path
CONFIG_FILE = "config.txt"

# Function to read server configurations from the config file
def read_config():
    servers = []
    with open(CONFIG_FILE, "r") as file:
        for line in file:
            ip, port = line.strip().split(":")
            servers.append((ip, int(port)))
    return servers

# Function to perform health checks on backend servers
def check_server(server):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(300)  # Adjust timeout as needed
        s.connect(server)
        s.close()
        return True
    except Exception as e:
        print(f"Error checking server {server}: {str(e)}")
        return False

# Function to periodically check the health of backend servers
def health_check():
    while True:
        for server in list(backend_servers):
            if not check_server(server):
                print(f"Server {server} is not responding. Removing from the list.")
                backend_servers.remove(server)
        time.sleep(10)  # Adjust the interval as needed

# Function to handle client requests
def handle_client(client_socket, server):
    server_ip, server_port = server
    try:
        # Connect to the backend server
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((server_ip, server_port))

        # Forward the client request to the backend server
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            backend_socket.sendall(data)

        # Receive response from the backend server and send it back to the client
        while True:
            data = backend_socket.recv(4096)
            if not data:
                break
            client_socket.sendall(data)

    except Exception as e:
        print(f"Error handling client request: {str(e)}")

    finally:
        client_socket.close()
        backend_socket.close()

# Function to start the load balancer
def start_load_balancer():
    # Create a TCP socket
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a port
    lb_socket.bind(('localhost', 8888))  # You can change the IP and port as needed

    # Listen for incoming connections
    lb_socket.listen(5)
    print("Load balancer is listening on port 8888...")

    # Start the health check thread
    health_check_thread = threading.Thread(target=health_check)
    health_check_thread.daemon = True
    health_check_thread.start()

    # Accept incoming connections and forward requests to backend servers
    while True:
        client_socket, address = lb_socket.accept()
        print(f"Connection from {address}")

        # Round Robin logic to forward requests to backend servers
        server = backend_servers.pop(0)
        backend_servers.append(server)

        # Handle the client request in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, server))
        client_thread.start()

# Read server configurations from the config file
backend_servers = read_config()

# Start the load balancer
start_load_balancer()
