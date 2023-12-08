import socket 
PORT = 9001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'
ERROR_MESSAGE = "Invalid inputs, type help to get help"
OPCODES = {
       "put": "000",
       "get": "001",
       "change": "010",
       "summary": "011",
       "help": "100"
}


RESPONSE_CODES={}
# given a string opcode return a binary opcode
def get_opcode(opcode: str) -> bytes:
    opcode = opcode.lower()
    opcode_in_bin = OPCODES.get(opcode, "")

    # TODO : return opcode in actual bytes
    # return bytes(opcode_in_bin, "utf-8")
    return opcode_in_bin

# given a binary opcode return a string opcode
def get_command(opcode):
    for string_opcode, binary_opcode in OPCODES.items():
        if(opcode == binary_opcode): return string_opcode
    return ""


#given a file name return the length in binary
def get_filename_length(file_name):
    filename_length = len(file_name)+1
    filename_length = format(filename_length, "b").zfill(5)
    return filename_length

def string_to_binary(string):
    result =  ''.join(format(ord(i), '08b') for i in string)
    # Converts the binary sequence string to bytes using UTF-8 encoding.
    return result



## Sockect functions
def create_socket(protocol="TCP"):
    protocol.capitalize()
    if(protocol == "TCP"):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else :
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(endpoint : socket.socket, request : str) -> None:
   try:
    endpoint.send(request.encode(ENCODING)[:BUFFER_SIZE])
    #TODO : Implement a way to send actual bytes 
    #    request = b"binary:" + request
    #    endpoint.send(request[:BUFFER_SIZE])
   except socket.error as e:
       print(f"Error sending message: {e}")
       raise

def receive_message(endpoint : socket) -> str:
   try:
       response = endpoint.recv(BUFFER_SIZE)
       # Check if the response starts with the marker "binary:"
       if response.startswith(b"binary:"):
           ### remove the marker
           binary_data = response[len(b"binary:"):]
           # transform marker to string 
           return binary_data
       else:
           return response.decode(ENCODING)
   except socket.error as e:
       print(f"Error receiving message: {e}")
       raise

def create_file(file_name : str, file_path: str):
    full_path = f"{file_path}/{file_name}"
    try:
        with open(full_path, 'w'):
            pass  # This creates an empty file
        print(f"File '{file_name}' created successfully at '{full_path}'.")
    except Exception as e:
        print(f"Error creating file: {e}")



