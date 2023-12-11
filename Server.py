from re import DEBUG
import traceback
import socket
import os
from utils import *


DEBUG_MODE = True
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
            # request = receive_message(client_socket)
            request = client_socket.recv(BUFFER_SIZE)
            # check if request is valid
            if not request:
                continue
            # get the opcode
            opcode = request[:3]
            # transform the opcode in commange
            command = get_command(opcode)
            msg = f"opcode : {opcode}  - command {command}"
            print_content(msg, DEBUG_MODE)

            if command == "get":
                print_content("Request", DEBUG_MODE)
                print_content(request, DEBUG_MODE)
                # get the filename size
                filename_length_bin = request[3:8]
                filename_length = int(filename_length_bin, 2) - 1
                

                # get the filename
                filename_bin = request[8 : 8 + filename_length * 8]
   
                ## transform the filename in str
                filename = binary_to_string(filename_bin)

                filepath = "Server/" + filename
                try:
                    #  open the file
                    filesize = os.path.getsize(filepath)
                    with open(filepath, "rb") as file:
                        file_content = file.read()
                except FileNotFoundError:
                    # raise exception if something goes wrong
                    response_code = get_response_code("file not found")
                    response_code = response_code + b"00000"
                    client_socket.sendall(response_code)
                    continue

                response_code= get_response_code("get success")
                # make sure the size is 4 byte, careful if size exceed 1GB
                filesize = filesize.to_bytes(4, byteorder='big', signed=False)
                filesize = hex_to_binary(filesize)
                

                response = opcode + filename_length_bin + filename_bin + filesize
                client_socket.send(response)

                client_socket.send(file_content)
                continue

            elif command == "help":
                # pring request if debug mode is true
                print_content(request, DEBUG)

                # get the response code, already in bin
                response_code = get_response_code("help")

                response_content = get_help()
                # get the response help
                response_length = len(response_content)
                # transform it in bytes

                response_length_in_bytes = int_to_binary(response_length, 5)
                response = bytes(response_content, ENCODING)
                response = response_code + response_length_in_bytes + response
                client_socket.sendall(response)
                continue
            elif command == "put":
                print_content("request", DEBUG_MODE)
                print_content(request, DEBUG_MODE)
                # get the filename size
                filename_length_bin = request[3:8]
                filename_length = int(filename_length_bin, 2) - 1
                

                # get the filename
                filename_bin = request[8 : 8 + filename_length * 8]
   
                ## transform the filename in str
                filename = binary_to_string(filename_bin)
                # get the file size 
                filesize = request[8 + filename_length * 8 : ]
                filesize = binary_to_int(filesize)
                
                
                response_code = get_response_code("put success")
                ## pad the binary string to match header format
                response_code = response_code + b"00000"
                client_socket.sendall(response_code)

                filename = "Server/" + filename
                remaining_size = filesize
                file_content = b""
                while remaining_size > 0:
                    # Receive file content in chunks
                    chunk_size = min(remaining_size, BUFFER_SIZE)
                    file_content += client_socket.recv(chunk_size)
                    remaining_size -= chunk_size

                with open(filename, "wb") as file:
                        file.write(file_content)
                # send back the response
                response_code = get_response_code("put success")
                response_code = response_code + b"00000"
                client_socket.sendall(response_code)
                continue

            elif command == "change":
                ##TODO:needs to be fixed
                old_filename_length_bin = request[3:8]
                old_filename_length = int(old_filename_length_bin, 2) - 1
                new_filename_length_bin = request[
                    8 + old_filename_length * 8 : 13 + old_filename_length * 8
                ]
                new_filename_length = int(new_filename_length_bin, 2) - 1

                # Extracting the old and new filenames
                old_filename_bin = request[8 : 8 + old_filename_length * 8]
                new_filename_bin = request[
                    13
                    + old_filename_length * 8 : 13
                    + old_filename_length * 8
                    + new_filename_length * 8
                ]
                old_filename = "".join(
                    chr(int(old_filename_bin[i : i + 8], 2))
                    for i in range(0, len(old_filename_bin), 8)
                )
                new_filename = "".join(
                    chr(int(new_filename_bin[i : i + 8], 2))
                    for i in range(0, len(new_filename_bin), 8)
                )
                old_filename = "Server/" + old_filename
                new_filename = "Server/" + new_filename
                # Renaming the file
                os.rename(old_filename, new_filename)
                print(f"Changed file name from {old_filename} to {new_filename}")
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
    # As per requirement the string is shortened to not  exceeed 31 characters
    return "bye change get help put sumry"


run_server()
