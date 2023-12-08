import traceback
import socket
import sys



# get argument
arguments = sys.argv


def run_server():
    try:
        # create a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = arguments[1]
        server_port = int(arguments[2])

        
        # bind the socket to a specific address and port
        server.bind((server_ip, server_port))

        # listen for incoming connections
        server.listen(0)
        print(f"Server listening on {server_ip}:{server_port}")

        # accept incoming connections
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        # receive data from the client
        while True:
            request = client_socket.recv(1024)
            request = request.decode("utf-8") # convert bytes to string
            recieved = list(request)
            # opcode = recieved[0] + recieved[1] + recieved[2]
            # text = ""
            # if opcode == "000":
            #     text = "put"
            # elif opcode == "001":
            #     text = "get"
            # elif opcode == "010":
            #     text = "change"
            # elif opcode == "011":
            #     text = "summary"
            # elif opcode == "100":
            #     text = "help"
            # print(text)
            # 
            # bins = recieved[8:]
            # result = ""
            # for i in range(8, len(bins), 8):
            #     binc = bins[i:i + 8]
            #     list_to_str = ''.join(map(str, binc))
            #     num = int(list_to_str, 2)
            #     result += chr(num)
            # print(result)


            if request.lower() == "bye":
              
                client_socket.send("bye".encode("utf-8"))
                break

            print(f"Received: {request}")

            response = "accepted".encode("utf-8") # convert string to bytes
            # convert and send accept response to the client
            client_socket.send(response)


    except (socket.error, OSError) as e:
       print(f"Error with sockets: {e}")
       traceback.print_exc()
    finally:
       if server is not None:
           server.close()
run_server()
