import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
server_address = ("localhost", 12345)
sock.bind(server_address)

while True:
    print("\nWaiting to receive message")
    data, address = sock.recvfrom(4096)

    print("Received {} bytes from {}".format(len(data), address))
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print("Sent {} bytes back to {}".format(sent, address))
