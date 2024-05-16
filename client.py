import socket
import time


def send_request(index:int):
    """
    Function to send a request to the load balancer
    """
    # Connect to the load balancer
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.connect(('127.0.0.1', 9000))  # Connect to localhost and port 9000

    # Send a sample request
    request = bytes(f"Sample request number, {index}", 'utf-8')
    lb_socket.send(request)

    # Receive the response from the load balancer
    response = lb_socket.recv(1024)
    print("Response from load balancer:", response.decode('utf-8'))

    # Close the socket
    lb_socket.close()


if __name__ == "__main__":
    # Number of requests to send
    num_requests = 10

    # Send multiple requests
    for i in range(num_requests):
        print(f"Sending request {i + 1}")
        send_request(i+1)
        # Pause for a short interval between requests
        time.sleep(1)
