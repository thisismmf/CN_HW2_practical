import socket

def send_request(message):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the load balancer
    client_socket.connect(('localhost', 8888))  # Use the IP and port of the load balancer

    try:
        # Send the request to the load balancer
        client_socket.sendall(message.encode())

        # Receive and print the response
        response = client_socket.recv(4096)
        print("Response:", response.decode())

    except Exception as e:
        print(f"Error sending request: {str(e)}")

    finally:
        # Close the socket
        client_socket.close()

# Test the load balancer by sending multiple requests
if __name__ == "__main__":
    # Test messages
    messages = ["Hello from Client 1", "Hello from Client 2", "Hello from Client 3"]

    for message in messages:
        print("Sending:", message)
        send_request(message)
