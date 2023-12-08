import socket
import sys

arguments = sys.argv
def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

def get_opcode (opcode_command):
    # TODO:  lower capital get GET Get
    opcode_command = opcode_command.lower()
    
    opcode = ""
    if opcode_command == "put":
        opcode = "000"
    elif opcode_command == "get":
        opcode = "001"
    elif opcode_command == "change":
        opcode = "010"
    elif opcode_command == "summary":
        opcode = "011"
    elif opcode_command == "help":
        opcode = "100"
    return opcode

def get_filename_length(file_name):
    filename_length = len(file_name)+1
    filename_length = format(filename_length, "b").zfill(5)
    return filename_length

def strings_to_binary(file_name):
    return ''.join(format(ord(i), '08b') for i in file_name)


def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Server you are connecting to 
    server_ip = "127.0.0.1"
    # Port you are connecting to 
    server_port = 8000
   
 
    client.connect((server_ip, server_port))
    print(f"Client listening at : {server_port}")

    while True:
        msg = input("Enter message: ")
        inputs = msg.split(" ")
        opcode = get_opcode(inputs[0])

        if opcode == "010":  # Change command
            if len(inputs) < 3:
                print("Error: Change command requires two filenames.")
                continue
            old_filename_length = get_filename_length(inputs[1])
            new_filename_length = get_filename_length(inputs[2])
            old_filename_binary = strings_to_binary(inputs[1])
            new_filename_binary = strings_to_binary(inputs[2])
            request = opcode + old_filename_length + old_filename_binary + new_filename_length + new_filename_binary
        
        elif opcode == "100":  # Help command
            request = opcode
            client.send(request.encode("utf-8")[:1024])

        elif opcode == "000":  # Put command
            if len(inputs) < 2:
                print("Error: Missing filename.")
                continue
            filename = inputs[1]
            try:
                with open(filename, 'rb') as file:
                    file_content = file.read()
                filename_length = get_filename_length(filename)
                filename_binary = strings_to_binary(filename)
                request = opcode + filename_length + filename_binary
                client.send(request.encode("utf-8")[:1024])
                client.send(file_content)
            except FileNotFoundError:
                print("File not found.")
        
        elif opcode == "001":  # Get command
            if len(inputs) < 2:
                print("Error: Missing filename.")
                continue
            filename = inputs[1]
            filename_length = get_filename_length(filename)
            filename_binary = strings_to_binary(filename)
            request = opcode + filename_length + filename_binary
            client.send(request.encode("utf-8")[:1024])

            # Receive file content from server
            
            
            file_content = client.recv(1024)
            file_content.decode("utf-8") 
            
            # Save received content to a file
            with open(filename, 'wb') as file:
                file.write(file_content)
            print(f"File {filename} received and saved.")

        elif opcode == "":  # Bye command
            request = "bye"
            client.send(request.encode("utf-8")[:1024])
            break

        else:
            if len(inputs) < 2:
                print("Error: Missing filename.")
                continue
            filename_length = get_filename_length(inputs[1])
            filename_binary = strings_to_binary(inputs[1])
            request = opcode + filename_length + filename_binary
            client.send(request.encode("utf-8")[:1024])

        # receive message from the server
        response = client.recv(1024)
        response = response.decode("utf-8")
        if response.lower() == "bye":
            break
        print(f"Received: {response}")

    client.close()
    print("Connection to server closed")

run_client()
