from re import DEBUG
import traceback
import socket
import os
from utils import *
from threading import Thread


DEBUG_MODE = True
server_ip = "127.0.0.1"
server_port = PORT
PROTOCOL = "TCP"


def main():
    # Create a thread for TCP server
    tcp_thread = Thread(target=run_tcp_server)
    # Start TCP server thread
    tcp_thread.start()

    # Create a thread for UDP server
    udp_thread = Thread(target=run_udp_server)
    # Start UDP server thread
    udp_thread.start()

    # Wait for both threads to finish
    tcp_thread.join()
    udp_thread.join()


def run_tcp_server():
    # create a socket object
    server = create_socket("TCP")
    # make sure socket is reusable when closed
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind server to port and address
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")
    try:
        while True:
            # accept incoming connections
            client_socket, client_address = server.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            # Create a new thread to handle this connection
            Thread(target=handle_client, args=(client_socket,)).start()
    # listen for incoming connections
    except (socket.error, OSError) as e:
        print(f"Error with sockets: {e}")
        traceback.print_exc()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        if server is not None:
            print("Closing Server")
            server.close()


def run_udp_server():
    # create a socket object
    server = create_socket("UDP")
    # bind server to port and address
    server.bind((server_ip, server_port))
    print(f"Server listening on {server_ip}:{server_port}")
    handle_client(server)


# return all the information about commands and what not
def get_help():
    # As per teacher's requirement the string is shortened to not  exceeed 31 characters
    return "bye change get help put summary"


def handle_client(client_socket: socket.socket):
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
                    send_message(client_socket, response_code)
                    continue

                response_code = get_response_code("get success")
                # make sure the size is 4 byte, careful if size exceed 1GB
                filesize = filesize.to_bytes(4, byteorder="big", signed=False)
                filesize = hex_to_binary(filesize)

                response = opcode + filename_length_bin + filename_bin + filesize
                send_message(client_socket, response)

                send_message(client_socket, file_content)
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
                send_message(client_socket, response)
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
                filesize = request[8 + filename_length * 8 :]
                filesize = binary_to_int(filesize)

                response_code = get_response_code("put success")
                ## pad the binary string to match header format
                response_code = response_code + b"00000"
                send_message(client_socket, response_code)

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
                send_message(client_socket, response_code)
                continue

            elif command == "change":
                print_content("Request", DEBUG_MODE)
                print_content(request, DEBUG_MODE)

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
                try:
                    # Attempt to rename the file
                    os.rename(old_filename, new_filename)
                    print_content(
                        f"Changed file name from {old_filename} to {new_filename}",
                        DEBUG_MODE,
                    )

                    # If successful, send a success response
                    # put and change have the same res code
                    response_code = get_response_code("put success")
                    response_code = response_code + b"00000"
                    send_message(client_socket, response_code)
                    continue
                except FileNotFoundError:
                    # If the file is not found, send an error response
                    error_response = get_response_code("file not found")
                    error_response = error_response + b"00000"
                    send_message(client_socket, error_response)
                    continue
                except Exception as e:
                    # Handle other exceptions as needed
                    print(f"An error occurred: {e}")
                    # Send an appropriate error response
                    error_response = get_response_code("unscesfull change")
                    error_response = error_response + b"00000"
                    send_message(client_socket, error_response)
                    continue
            elif command == "summary":
                print_content("request", DEBUG_MODE)
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
                    with open(filepath, "r") as file:
                        file_content = file.read()
                except FileNotFoundError:
                    # raise exception if something goes wrong
                    response_code = get_response_code("file not found")
                    response_code = response_code + b"00000"
                    send_message(client_socket, response_code)
                    continue

                # perfom the statical analysis
                numbers = file_content.split(",")
                numbers = [int(num) for num in numbers]

                minimum = min(numbers)

                # Calculate the maximum
                maximum = max(numbers)

                # Calculate the average
                average = sum(numbers) / len(numbers)
                response_data = (
                    f"Minimum : {minimum}\nMaximum : {maximum}\nAverage{average}"
                )

                # write to the file
                # open file
                new_filename = "Summary: " + filename
                new_path = "Server/" + new_filename
                # Open the file in write mode
                with open(new_path, "w") as file:
                    # Write the response data to the file
                    file.write(response_data)

                response_code = get_response_code("summary success")
                # make sure the size is 4 byte, careful if size exceed 1GB
                filesize = os.path.getsize(new_path)
                filesize = filesize.to_bytes(4, byteorder="big", signed=False)
                filesize = hex_to_binary(filesize)

                # new filename
                filename_length = len(new_filename) + 1
                filename_length = int_to_binary(filename_length, 5)

                new_filename = string_to_binary(new_filename)
                response = response_code + filename_length + new_filename + filesize
                send_message(client_socket, response)

                send_message(client_socket, response_data.encode(ENCODING))

    except (socket.error, OSError) as e:
        print(f"Error with sockets: {e}")
        traceback.print_exc()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        if client_socket is not None:
            print("Closing Client")
            client_socket.close()


if __name__ == "__main__":
    main()
