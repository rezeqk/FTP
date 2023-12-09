import traceback
import socket
import os
import sys
from utils import * 


server_ip = "127.0.0.1"
server_port = PORT


def run_server():
    # create a socket object
    server = create_socket("TCP")
    # make sure socket is reusable when closed 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    # bind server to port and address
    server.bind((server_ip, server_port))
    # listen for incoming connections
    server.listen(0)
    print(f"Server listening on {server_ip}:{server_port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    try:
        while True:
            request = receive_message(client_socket)
            # check if request is valid
            if not request:
                continue
            # get the opcode 
            opcode = request[:3]
            # transform the opcode in commange 
            command = get_command(opcode)
            print(f"opcode : {opcode}  - command {command}")
            if command == "get":
                print(request)
                filename_length_bin = request[3:8]
                filename_length = int(filename_length_bin, 2) - 1
                # get the filename
                filename_bin = request[8:8 + filename_length * 8]

                ## transform the filename in 
                filename = ''.join(chr(int(filename_bin[i:i+8], 2)) for i in range(0, len(filename_bin), 8))
                filename = "Server/" + filename
                print(f"Sending file: {filename}")
                client_socket.send("Filename received.".encode("utf-8"))
                send_message(client_socket, "Filename received")

                # Send the file content
                with open(filename, 'rb') as file:
                    file_content = file.read()
                client_socket.send(file_content)
                print(f"File {filename} sent.")
                client_socket.send("File data sent.".encode("utf-8"))
                continue

            if command == "help": 
                ##TODO : SEND RESPONSE CODE 
                print(request)
                response = get_help()
                send_message(client_socket, response)
                continue
            if command == "put":
                print(request)
                filename_length_bin = request[3:8]
                filename_length = int(filename_length_bin, 2) - 1
                # get the filename
                filename_bin = request[8:8 + filename_length * 8]

                ## transform the filename in 
                filename = ''.join(chr(int(filename_bin[i:i+8], 2)) for i in range(0, len(filename_bin), 8))
                filename = "Server/" + filename
                print(f"Receiving file: {filename}")
                client_socket.send("Filename received.".encode("utf-8"))
                send_message(client_socket, "Filename received")

                # Receive and write the file content
                file_content = client_socket.recv(BUFFER_SIZE)
               # file_content = file_content.decode(ENCODING)
                #file_content = receive_message(client_socket)
                with open(filename, 'wb') as file:
                    file.write(file_content)
                print(f"File {filename} received and saved.")
                client_socket.send("File data received.".encode("utf-8"))

           
            if command == "change":
            ##TODO:needs to be fixed
             filename_length_bin = request[3:8]
             filename_length = int(filename_length_bin, 2) - 1
             # Get the filename
             filename_bin = request[8:8 + filename_length * 8]

              # Transform the filename into a string
             filename = ''.join(chr(int(filename_bin[i:i+8], 2)) for i in range(0, len(filename_bin), 8))

                # Assuming the old and new filenames are concatenated in `filename`
             old_filename, new_filename = filename.split(" ", 1)
             old_filename_full = "Server/" + old_filename
             new_filename_full = "Server/" + new_filename

             os.rename(old_filename_full, new_filename_full)
             print(f"Changed file name from {old_filename_full} to {new_filename_full}")
             client_socket.send("File name changed successfully.".encode("utf-8"))


    except (socket.error, OSError) as e:
        print(f"Error with sockets: {e}")
        traceback.print_exc()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        if server is not None:
            print("Closing Server")
            server.close()
        if client_socket is not None:
            print("Closing Client")
            client_socket.close()



# return all the information about commands and what not 
def get_help():
    return ("Help information:\n"
            "  put <filename> - Upload a file\n"
            "  get <filename> - Download a file\n"
            "  change <filename> - Change a file\n"
            "  summary - Get a summary\n"
            "  bye - Exit the program")




run_server()
