import socket

SUCCESS = 1
ERROR = 0
PORT = 9001
BUFFER_SIZE = 1024
ENCODING = "utf-8"
ERROR_MESSAGE = "Invalid inputs, type help to get help"
OPCODES = {"put": "000", "get": "001", "change": "010", "summary": "011", "help": "100"}


RESPONSE_CODES = {
    "get success": "001",
    "put success": "000",
    "summary success": "010",
    "file not found": "011",
    "unkown request": "100",
    "unsuccesful change": "101",
    "help response": "110",
}


# given a response code
def get_response_code(code: str) -> bytes:
    response = RESPONSE_CODES.get(code, "")
    return bytes(response, ENCODING)


# given a string opcode return a binary opcode,
def get_opcode(opcode: str) -> bytes:
    opcode = opcode.lower()
    opcode_in_bin = OPCODES.get(opcode, "")
    return bytes(opcode_in_bin, ENCODING)


# given a binary opcode return a string opcode
def get_command(opcode: bytes) -> str:
    opcode_str = opcode.decode(ENCODING)
    for string_opcode, binary_opcode in OPCODES.items():
        if opcode_str == binary_opcode:
            return string_opcode
    return ""


# given a file name return the length in binary
def get_filename_length(file_name: str) -> bytes:
    filename_length = len(file_name) + 1
    filename_length = format(filename_length, "b").zfill(5)
    return filename_length


# give an integer transform it into binary using the specified number of bits
def int_to_binary(number: int, n_bits: int) -> bytes:
    length_in_bin = format(number, "b")
    bits = len(length_in_bin)
    if bits < n_bits:
        # if the number of bits is less than 5 pad with extra 0 on the left
        return bytes(length_in_bin.zfill(n_bits - bits), ENCODING)
    else:
        return bytes(length_in_bin, ENCODING)


def binary_to_int(binary_number: bytes, n_bits: int) -> int:
    binary_string = "".join(format(byte, "08b") for byte in binary_number)
    binary_string = binary_string[:n_bits]
    return int(binary_string, 2)


def string_to_binary(string: str) -> bytes:
    # Converts the binary sequence string to bytes using UTF-8 encoding.
    binary_string = " ".join(format(ord(x), "b") for x in string)
    return bytes(binary_string, ENCODING)


def binary_to_string(binary_data: bytes) -> str:
    """
    Convert a bytes object containing binary data to a string.
    """
    # Convert the bytes object to a binary string
    binary_string = "".join(format(byte, "08b") for byte in binary_data)
    print(binary_string)
    print(type(binary_string))

    # Remove spaces from the binary string
    binary_string = binary_string.replace(" ", "")

    # Split the binary string into 8-bit segments
    segments = [binary_string[i : i + 8] for i in range(0, len(binary_string), 8)]
    print(segments)
    print(type(segments))

    # Convert each 8-bit segment to an integer and then to a character
    result = "".join(chr(int(segment, 2)) for segment in segments)
    print(result)
    return result


## Sockect functions
def create_socket(protocol="TCP"):
    protocol.capitalize()
    if protocol == "TCP":
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(endpoint: socket.socket, request: str) -> None:
    try:
        endpoint.send(request.encode(ENCODING)[:BUFFER_SIZE])
        # TODO : Implement a way to send actual bytes
        #    request = b"binary:" + request
        #    endpoint.send(request[:BUFFER_SIZE])
    except socket.error as e:
        print(f"Error sending message: {e}")
        raise


def receive_message(endpoint: socket.socket) -> str:
    try:
        response = endpoint.recv(BUFFER_SIZE)
        # Check if the response starts with the marker "binary:"
        if response.startswith(b"binary:"):
            ### remove the marker
            binary_data = response[len(b"binary:") :]
            # transform marker to string
            return binary_data
        else:
            return response.decode(ENCODING)
    except socket.error as e:
        print(f"Error receiving message: {e}")
        raise


def create_file(file_name: str, file_path: str):
    full_path = f"{file_path}/{file_name}"
    try:
        with open(full_path, "w"):
            pass  # This creates an empty file
        print(f"File '{file_name}' created successfully at '{full_path}'.")
    except Exception as e:
        print(f"Error creating file: {e}")


def print_content(content: object, debug=False):
    """custom print function that only print if the debug flag is on"""
    if debug is True:
        print(content)
