import traceback
import os
import socket
import sys
from utils import * 

# Server you are connecting to 
server_ip = "127.0.0.1"
# Port you are connecting to 
server_port = PORT

    
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
            # if the request is bye or help send the opcode
            if command == "bye" :
                client.close()
                break
            

            if command == "help": 
                # get opcode in bytes
                opcode = get_opcode(command)
                # get opcode  in binary 
                send_message(client, opcode)

                # get response
                response = receive_message(client)
                print(f"Received response : {response}")
                continue


            # the request is something else check_inputs, if iputs are not valid, restart the loop
            if inputs_are_not_valid(inputs):
                print(ERROR_MESSAGE)
                continue

            # HANDLE SUMMARY REQUEST
            elif (command == "summary"):
                # get opcode in bytes
                opcode = get_opcode(command)

                # get the length in bytes 
                old_filename_length = get_filename_length(inputs[1])
                new_filename_length = get_filename_length(inputs[2])

                # get the file names in bytes 
                old_filename_binary = string_to_binary(inputs[1])
                new_filename_binary = string_to_binary(inputs[2])
                request = opcode + old_filename_length + old_filename_binary + new_filename_length + new_filename_binary
                ## HANDLE THE LOGIC OF SUMMARY 
                continue

            # HANDLE GET
            elif  command == "put" :
                # get opcode in bytes
                opcode = get_opcode(command)

                # get the length in bytes 
                filename_length = get_filename_length(inputs[1])
                
                # get filename in bytes
                filename_binary = string_to_binary(inputs[1])
                request = opcode + filename_length + filename_binary
                
                # send request for getting a file 
                send_message(client, request)
                response = receive_message(client)
                print(f"Response from server : {response}")

                # if request accepted 
                # get the filename and content 
                filename = "Client/" + inputs[1]
                try:
                    #  open the file
                    with open(filename, 'rb') as file:
                        file_content = file.read()
                except FileNotFoundError:
                    # raise exception if something goes wrong 
                    print("File not found.")
                    continue
                
                file_content = file_content.decode(ENCODING)
                send_message(client, file_content)
                # client.send(file_content)

                response = receive_message(client)
                print(f"Response from server : {response}")

                continue

            
            # HANDLE PUT 
            elif  command == "get" :
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
                    with open(filename, 'wb') as file:
                        file.write(response)
                except FileNotFoundError:
                    # raise exception if something goes wrong 
                    print("File not found.")
                    continue

                continue

                ##TODO: needs to be fixed
            elif command == "change":  # Change command
                opcode = get_opcode(command)
                old_filename_length = get_filename_length(inputs[1])
                new_filename_length = get_filename_length(inputs[2])

                # get the file names in bytes 
                old_filename_binary = string_to_binary(inputs[1])
                new_filename_binary = string_to_binary(inputs[2])
                request = opcode + old_filename_length + old_filename_binary + new_filename_length + new_filename_binary
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
    request =""


run_client()
