import socket

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

    server_ip = input("Enter IP Address:")
    print("IP address is: " + server_ip)
    
    server_port = int(input("Enter Port Number:"))
    print("Your Port Number is:" + str(server_port))
 
    client.connect((server_ip, server_port))

    while True:
        # input message and send it to the server
        msg = input("Enter message: ")
        inputs = msg.split(" ")
        opcode = get_opcode(inputs[0])
        filename_length = get_filename_length(inputs[1])
        filename_binary = strings_to_binary(inputs[1])
        request = opcode + filename_length + filename_binary
        print(request)

        client.send(request.encode("utf-8")[:1024])

        # receive message from the server
        response = client.recv(1024)
        response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "bye":
            break

        print(f"Received: {response}")

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()
