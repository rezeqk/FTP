import socket
import sys

arguments = sys.argv


def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Server you are connecting to 
    server_ip = arguments[1]
    # Port you are connecting to 
    server_port = int(arguments[2])
     
    server_ip = arguments[1]
    server_port = int(arguments[2])
 
    client.connect((server_ip, server_port))
    print(f"Client listening at : {server_port}")

    while True:
        # input message and send it to the server
        msg = input("Enter message: ")
        client.send(msg.encode("utf-8")[:1024])

        # receive message from the server
        response = client.recv(1024)
        response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "closed":
            break

        print(f"Received: {response}")

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()
