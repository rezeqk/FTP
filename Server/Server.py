import socket
import sys

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    server.bind((server_ip, server_port))
    server.listen(0)
    print(f"Server listening on {server_ip}:{server_port}")

    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:
        request = client_socket.recv(1024).decode("utf-8")
        if not request:
            continue

        if len(request) < 3:  # Ensure the request has an opcode
            print("Error: Invalid request.")
            continue

        opcode = request[:3]
        print("OPCODE =", opcode)

        if opcode == "000":  # Put command
            # Receive and process the filename
            filename_length_bin = request[3:8]
            filename_length = int(filename_length_bin, 2) - 1
            filename_bin = request[8:8 + filename_length * 8]
            filename = ''.join(chr(int(filename_bin[i:i+8], 2)) for i in range(0, len(filename_bin), 8))
            print(f"Receiving file: {filename}")
            client_socket.send("Filename received.".encode("utf-8"))

            # Receive and write the file content
            file_content = client_socket.recv(1024)
            with open(filename, 'wb') as file:
                file.write(file_content)
            print(f"File {filename} received and saved.")
            client_socket.send("File data received.".encode("utf-8"))

        if opcode == "010":  # Change command
            old_filename_length_bin = request[3:8]
            old_filename_length = int(old_filename_length_bin, 2) - 1
            new_filename_length_bin = request[8 + old_filename_length * 8:13 + old_filename_length * 8]
            new_filename_length = int(new_filename_length_bin, 2) - 1

            old_filename_bin = request[8:8 + old_filename_length * 8]
            new_filename_bin = request[13 + old_filename_length * 8:13 + old_filename_length * 8 + new_filename_length * 8]

            old_filename = ''.join(chr(int(old_filename_bin[i:i+8], 2)) for i in range(0, len(old_filename_bin), 8))
            new_filename = ''.join(chr(int(new_filename_bin[i:i+8], 2)) for i in range(0, len(new_filename_bin), 8))

            print(f"Changing file name from {old_filename} to {new_filename}")
        if opcode == "100":  # Help command
            # Send help response or handle it here
            response = ("Help information:\n"
                            "  put <filename> - Upload a file\n"
                            "  get <filename> - Download a file\n"
                            "  change <filename>  <new filename> - Change a file\n"
                            "  summary - Get a summary\n"
                            "  bye - Exit the program")
            client_socket.send(response.encode("utf-8"))
            continue
        elif opcode in ["000", "001", "010", "011"]:  # Other commands
            # Process the filename
            if len(request) < 13:  # Ensure the request has enough data for filename
                print("Error: Incomplete request for filename.")
                continue

            filename_length_bin = request[3:8]
            filename_length = int(filename_length_bin, 2) - 1  # Subtract 1 for the added 1 in client
            filename_bin = request[8:8 + filename_length * 8]
            filename = ''.join(chr(int(filename_bin[i:i+8], 2)) for i in range(0, len(filename_bin), 8))
            print(f"Filename: {filename}")


        if request.lower() == "bye":
            client_socket.send("bye".encode("utf-8"))
            break

        response = "accepted".encode("utf-8")
        client_socket.send(response)

    client_socket.close()
    print("Connection to client closed")
    server.close()

run_server()