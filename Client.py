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
                response = client.recv(BUFFER_SIZE).decode()
                print(response)

                response_code = response[:3]
                if response_code == "110":
                    data_length = response[3:8]
                    received_data = response[8:]
                    msg_to_print = f"Received packet: Response code : {response_code} - Data length : {data_length}\n{received_data}"
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

                # get the length in bytes
                old_filename_length = get_filename_length(inputs[1])
                new_filename_length = get_filename_length(inputs[2])

                # get the file names in bytes
                old_filename_binary = string_to_binary(inputs[1])
                new_filename_binary = string_to_binary(inputs[2])
                request = (
                    opcode
                    + old_filename_length
                    + old_filename_binary
                    + new_filename_length
                    + new_filename_binary
                )
                ## HANDLE THE LOGIC OF SUMMARY
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
                print(response_code == get_response_code("put success"))
                print(response_code, get_response_code("put success"))

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

                # get the length in bytes
                filename_length = get_filename_length(inputs[1])

                # get filename in bytes
                filename_binary = string_to_binary(inputs[1])
                request = opcode + filename_length + filename_binary

                # send request for getting a file
                send_message(client, request)
                response = client.recv(BUFFER_SIZE)
                response = client.recv(BUFFER_SIZE)

                # if request accepted
                # get the filename and content
                filename = "Client/" + inputs[1]
                try:
                    #  open the file
                    with open(filename, "wb") as file:
                        file.write(response)
                except FileNotFoundError:
                    # raise exception if something goes wrong
                    print("File not found.")
                    continue

                continue

                ##TODO: eeds to be fixed
            elif command == "change":  # Change command
                opcode = get_opcode(command)
                old_filename_length = get_filename_length(inputs[1])
                new_filename_length = get_filename_length(inputs[2])

                # get the file names in bytes
                old_filename_binary = string_to_binary(inputs[1])
                new_filename_binary = string_to_binary(inputs[2])
                request = (
                    opcode
                    + old_filename_length
                    + old_filename_binary
                    + new_filename_length
                    + new_filename_binary
                )
                client.send(request.encode("utf-8"))

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
