import socket

def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  
    server_port = 8000  
    # add a comment 
    

    # bind the socket to a specific address and port
    server.bind((server_ip, server_port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip}:{server_port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    print("please enter a command you want to execute Type help for more info")
    # receive data from the client
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # convert bytes to string
        
        if request.lower() == "help":
            client_socket.send("help".encode("utf-8"))
            opcode = 100
            
        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == "bye":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("bye".encode("utf-8"))
            break

        print(f"Received: {request}")

        response = "accepted".encode("utf-8") # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)

    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()


run_server()
