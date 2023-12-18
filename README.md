---

# Client-Server File Transfer Application

## Overview

This is a simple client-server file transfer application implemented in Python. The application supports both TCP and UDP protocols for communication between the client and server.

## Usage

### Server

The server is responsible for handling client requests and managing file operations. To run the server, execute the `server.py` script:

```bash
python server.py [debug_mode]
```

The server will listen for incoming connections on the specified IP address and port.

### Client

The client interacts with the server to perform various file-related operations. To run the client, execute the `client.py` script:

```bash
python client.py [server_ip] [server_port] [debug_mode]
```

- `server_ip` (Optional): The IP address of the server. Default is "127.0.0.1".
- `server_port` (Optional): The port on which the server is listening. Default is 20000.
- `debug_mode` (Optional): Set to 1 for debug mode, 0 otherwise. Default is 0.

#### Available Commands:

- `help`: Get information about available commands.
- `get <filename>`: Download a file from the server.
- `put <filename>`: Upload a file to the server.
- `change <old_filename> <new_filename>`: Change the name of a file on the server.
- `summary <filename>`: Retrieve statistical summary (min, max, average) of numeric data from a file on the server.
- `bye`: Disconnect from the server and exit the client.
