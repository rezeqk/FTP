import traceback
import socket
from utils import * 
import os

# Server you are connecting to
server_ip = "127.0.0.1"
# Port you are connecting to
server_port = PORT
DEBUG_MODE = True


def run_client():
    # create a socket object
    client = create_socket("TCP")

    # connect to server
    client.connect((server_ip, server_port))
    print(f"Client listening at : {server_port}")

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
                client.sendall(request)

                # get response
                response = client.recv(BUFFER_SIZE)
                response_code = response[:3]

                if response_code == get_response_code("help"):
                    data_length = response[3:8]
                    received_data = response[8:]
                    msg_to_print = f"Received packet: Response code : {response_code} - Data length : {data_length}\nData: {received_data}"
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
                print_content("Request",DEBUG_MODE)
                print_content(request, DEBUG_MODE)

                client.send(request)

                response = client.recv(BUFFER_SIZE)
                response_code = response[:3]
                filename_length= response[3:8]
                filename_length = int(filename_length, 2) - 1

                # get the filename
                filename_bin = response[8 : 8 + filename_length * 8]
                ## transform the filename in str
                filename = binary_to_string(filename_bin)

                # get the file size
                start = 8 + filename_length * 8
                end = start + 24 # file size is always 32 bits 
                filesize = response[start:end]
                filesize = binary_to_int(filesize)
                header = response[:end]
                print_content("Response", DEBUG_MODE)
                print_content(header,DEBUG_MODE)

                # handle the response
                if response_code == get_response_code("summary success"):
                    filename = "Client/" + filename
                    remaining_size = filesize
                    file_content = b""
                    file_content +=response[end:]
                    remaining_size -= len(file_content)

                    while remaining_size > 0:
                        # Receive file content in chunks
                        chunk_size = min(remaining_size, BUFFER_SIZE)
                        file_content += client.recv(chunk_size)
                        remaining_size -= chunk_size

                    with open(filename, "wb") as file:
                            # write to file
                            file.write(file_content)
                            print_content("Summary successful")
                elif response_code == get_response_code("file not found"):
                    print("Error : file not found please try again")
                    continue
                else :
                    print("Unknown issue could not send the request")
                    continue
                continue
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
                filesize = filesize.to_bytes(4, byteorder='big', signed=False)
                filesize = hex_to_binary(filesize)
                

                request = opcode + filename_length + filename_binary + filesize
                print_content("Request",DEBUG_MODE)
                print_content(request, DEBUG_MODE)

                # Ensure the size is exactly 4 bytes
                # send request for uploading a file
                client.sendall(request)

                response = client.recv(BUFFER_SIZE)
                print_content(response, DEBUG_MODE)
                response_code = response[:3]

                if response_code == get_response_code("put success"):
                    client.sendall(file_content)
                else :
                    print("Server issue, could not send the file")

                response = client.recv(BUFFER_SIZE).decode()
                print_content(response, DEBUG_MODE)
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
                client.sendall(request)
                response = client.recv(BUFFER_SIZE)
                response_code = response[:3]
        
                start = 8 + filename_length * 8
                end = start + 24 # file size is always 32 bits 
                filesize = response[start:end]
                filesize = binary_to_int(filesize)
                header = response[:end]
                print_content("Response", DEBUG_MODE)
                print_content(header,DEBUG_MODE)

                # handle the response
                if response_code == get_response_code("get success"):
                    filename = "Client/" + inputs[1]
                    remaining_size = filesize
                    file_content = b""
                    file_content +=response[end:]
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
                else :
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
                old_filename_length = int_to_binary(old_filename_length,5)
                new_filename_length = int_to_binary(new_filename_length,5)


                # get filename in bytes
                old_filename = string_to_binary(inputs[1])
                new_filename = string_to_binary(inputs[2])


                request = opcode + old_filename_length+old_filename + new_filename_length + new_filename
                client.send(request)
                response = client.recv(BUFFER_SIZE)
                print_content(f"Response {response}", DEBUG_MODE)

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
