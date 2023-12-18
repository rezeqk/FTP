#Name: Rezeq Khader ID:26777538
#Name: Shami Ivan Senga ID:40228447

import traceback
import socket
from utils import *
import os
import sys

DEFAULT_SERVER_IP = "127.0.0.1"
DEFAULT_PORT = 20000
DEFAULT_DEBUG_MODE = False
# Port you are connecting to
server_port = PORT
DEBUG_MODE = False




# Check if there are command-line arguments
if len(sys.argv) >= 3:
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
else:
    # Use default values if not provided
    server_ip = DEFAULT_SERVER_IP
    server_port = DEFAULT_PORT

# Check for the debug flag (0 means OFF, 1 means ON)
debug_flag = DEFAULT_DEBUG_MODE
if len(sys.argv) >= 4:
    debug_flag = bool(int(sys.argv[3]))


    
ADDR = (server_ip, server_port)

def run_client():
    while True:
        protocol = input("Select 1 for TCP and 2 for UDP\n")
        if protocol == "1":
            set_protocol("TCP")
            client = create_socket(PROTOCOL)
            client.connect((server_ip, server_port))
            print(f"Client listening at : {server_port}")

            break
        elif protocol == "2":
            set_protocol("UDP")
            client = create_socket("UDP")
            print(get_protocol())
            break
        else:
            print("put something else")
            continue

  
# Checking the socket type
    if client.type == socket.SOCK_DGRAM:
        print("The socket is a UDP socket.")
    elif client.type == socket.SOCK_STREAM:
        print("The socket is a TCP socket.")



    try:
        while True:
            msg = input("Enter message: ")
            # get messages
            inputs = msg.split(" ")

            command = inputs[0]
            # if request is bye  terminate
            if command == "bye":
                client.close()
                break

            # if request is help send opcode
            if command == "help":
                # get opcode in binary
                opcode = get_opcode(command)

                request = opcode
                send_message(client, request, ADDR)

                # get response
                response,_ = receive_message(client)
                response_code = response[:3]
                print("Response_code",response_code)
                print_content(response, DEBUG_MODE)
                if response_code == get_response_code("help"):
                    data_length = response[3:8]
                    received_data = response[8:]
                    msg_to_print = f"Received packet: Response code : {response_code} - Data length : {data_length}\nData: {received_data}"
                    print(f" response : {response_code},  data :  {received_data}")
                    print_content(msg_to_print, DEBUG_MODE)
                else:
                    print_content("Error getting the help", DEBUG_MODE)


                continue
            

            # the request is something else check_inputs, if iputs are not valid, restart the loop
            if inputs_are_not_valid(inputs):
                print(ERROR_MESSAGE)
                continue

            # HANDLE SUMMARY REQUEST
            if command == "summary":
                # get opcode in bytes
                opcode = get_opcode(command)

                # get the filename_length
                filename_length = len(inputs[1]) + 1
                # TODO : check filename length, should not exceed 31 characters
                # transfom the length in binary
                filename_length = int_to_binary(filename_length, 5)

                # get filename in bytes
                filename_binary = string_to_binary(inputs[1])

                request = opcode + filename_length + filename_binary
                print_content("Request", DEBUG_MODE)
                print_content(request, DEBUG_MODE)

                send_message(client, request)

                response = receive_message(client)[0]
                response_code = response[:3]
                filename_length = response[3:8]
                filename_length = int(filename_length, 2) - 1

                # get the filename
                filename_bin = response[8 : 8 + filename_length * 8]
                ## transform the filename in str
                filename = binary_to_string(filename_bin)

                # get the file size
                start = 8 + filename_length * 8
                end = start + 24  # file size is always 32 bits
                filesize = response[start:end]
                filesize = binary_to_int(filesize)
                print("filesize",filesize)
                header = response[:end]
                print_content("Response", DEBUG_MODE)
                print_content(header, DEBUG_MODE)
                print(response)

                # handle the response
                if response_code == get_response_code("summary success"):
                    filename = "Client/" + filename
                    remaining_size = filesize
                    print(response, response[end: ])
                    file_content  = response[end + 8 :]
                    remaining_size -= len(file_content)

                    print(file_content)
                    while remaining_size > 0:
                        # Receive file content in chunks
                        chunk_size = min(remaining_size, BUFFER_SIZE)
                        file_content += receive_message(client, chunk_size)
                        remaining_size -= chunk_size
                    with open(filename, "wb") as file:
                        # write to file
                        file.write(file_content)
                        print(file_content)
                elif response_code == get_response_code("file not found"):
                    print("Error : file not found please try again")
                    continue
                else:
                    print("Unknown issue could not send the request")
                    continue
                print("Summary downloaded succesfully")
                continue

            # HANDLE GET
            elif command == "put":
                # get opcode in bytes
                opcode = get_opcode(command)

                # get the filename_length
                filename_length = len(inputs[1]) + 1
                # TODO : check filename length, should not exceed 31 characters
                # transfom the length in binary
                filename_length = int_to_binary(filename_length, 5)

                # get filename in bytes
                filename_binary = string_to_binary(inputs[1])

                # get the filenmae
                filepath = "Client/" + inputs[1]

                try:
                    #  open the file
                    # get the files size
                    filesize = os.path.getsize(filepath)
                    with open(filepath, "rb") as file:
                        file_content = file.read()
                except FileNotFoundError:
                    # raise exception if something goes wrong
                    print("File not found.")
                    continue

                # make sure the size is 4 byte, careful if size exceed 1GB
                filesize = filesize.to_bytes(4, byteorder="big", signed=False)
                filesize = hex_to_binary(filesize)

                request = opcode + filename_length + filename_binary + filesize
                print_content("Request", DEBUG_MODE)
                print_content(request, DEBUG_MODE)

                # Ensure the size is exactly 4 bytes
                # send request for uploading a file
                send_message(client, request, ADDR)
                
                
                response,_ = receive_message(client)
                print_content(response, DEBUG_MODE)
                response_code = response[:3]

                if response_code == get_response_code("put success"):
                    send_message(client, file_content, ADDR)
                else:
                    print("Server issue, could not send the file")

                response = receive_message(client)
                print_content(response, DEBUG_MODE)
                print("File uploaded succesfully")
                continue
            # HANDLE PUT
            elif command == "get":
                # get opcode in bytes
                opcode = get_opcode(command)

                # get the filename_length
                filename_length = len(inputs[1]) + 1
                # TODO : check filename length, should not exceed 31 characters
                # transfom the length in binary
                filename_length_bin = int_to_binary(filename_length, 5)

                # get filename in bytes
                filename_binary = string_to_binary(inputs[1])

                request = opcode + filename_length_bin + filename_binary

                # send request for getting a file
                send_message(client, request,ADDR)
                response = receive_message(client)[0]
                print_content(response, DEBUG_MODE)
                response_code = response[:3]
                if response_code == get_response_code("file not found"):
                    print_content("Error : File not found", DEBUG_MODE)
                    continue

                start = 8 + filename_length * 8
                end = start + 24  # file size is always 32 bits
                filesize = response[start:end]
                filesize = binary_to_int(filesize)
                header = response[:end]
                print_content("Response", DEBUG_MODE)
                print_content(header, DEBUG_MODE)


                # handle the response
                if response_code == get_response_code("get success"):
                    filename = "Client/" + inputs[1]
                    remaining_size = filesize
                    file_content = b""
                    file_content += response[end:]
                    remaining_size -= len(file_content)
                    while remaining_size > 0:
                        # Receive file content in chunks
                        chunk_size = min(remaining_size, BUFFER_SIZE)
                        file_content += client.recv(chunk_size)
                        remaining_size -= chunk_size

                    with open(filename, "wb") as file:
                        # write to file
                        file.write(file_content)
                        print_content("File dowloaded succesfully")
                elif response_code == get_response_code("file not found"):
                    print("Error : file not found please try again")
                    continue
                else:
                    print("Connection issue could not send the request")
                    continue
                continue

            elif command == "change":
                # get opcode in bytes
                opcode = get_opcode(command)

                # get the filename_length
                old_filename_length = len(inputs[1]) + 1
                new_filename_length = len(inputs[2]) + 1

                # TODO : check filename length, should not exceed 31 characters
                # transfom the length in binary
                old_filename_length = int_to_binary(old_filename_length, 5)
                new_filename_length = int_to_binary(new_filename_length, 5)

                # get filename in bytes
                old_filename = string_to_binary(inputs[1])
                new_filename = string_to_binary(inputs[2])

                request = (
                    opcode
                    + old_filename_length
                    + old_filename
                    + new_filename_length
                    + new_filename
                )
                send_message(client, request)
                response = receive_message(client)
                print_content(f"Response {response}", DEBUG_MODE)
                print("File name changed succesfully")

    except (socket.error, OSError) as e:
        print(f"Error with sockets: {e}")
        traceback.print_exc()
    except KeyboardInterrupt as e:
        print("Keyboard interrupt : {e}")

    finally:
        # close connection socket with the client
        if client is not None:
            print("Closing connection to client")
            client.close()


# return true if inputs
def inputs_are_not_valid(inputs):
    opcode = inputs[0].lower()
    if opcode == "change" and len(inputs) < 3:
        return True
    elif opcode in ["get", "put", "summary"] and len(inputs) < 2:
        return True
    else:
        return False


def generate_request_string(inputs):
    opcode = inputs[0].lower()
    request = ""


run_client()
