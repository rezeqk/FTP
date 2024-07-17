# FTP Project

A simple File Transfer Protocol (FTP) implementation using Python, supporting both TCP and UDP protocols.

## Project Structure

The project consists of the following key components:

- `client.py`: The client-side application allowing users to connect to the server and perform file operations.
- `server.py`: The server-side application handling client requests and executing file operations.
- `utils.py`: A utility module containing helper functions and constants used by both client and server.
- `README.md`: This documentation file.

## Features

- **TCP and UDP Support**: Clients can choose between TCP and UDP for communication with the server.
- **File Operations**: The application supports various file operations:
  - `put`: Upload a file to the server.
  - `get`: Download a file from the server.
  - `change`: Rename a file on the server.
  - `summary`: Perform a statistical summary of the contents of a file on the server.
  - `help`: Request information about available commands.
  - `bye`: Terminate the client session.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ftp-project.git
   cd ftp-project
   ```
2. Ensure all dependencies are installed (if any).

### Running the Server

To start the server, run the following command:

```sh
python server.py
```

The server will start listening for client connections on the specified IP address and port.

### Running the Client

To start the client, run the following command:

```sh
python client.py
```

The client will prompt you to select the protocol (TCP or UDP) and then connect to the server.

## Usage

Once connected, the client can perform various commands as described below:

### Commands

- `put <filename>`: Upload a file to the server.
- `get <filename>`: Download a file from the server.
- `change <old_filename> <new_filename>`: Rename a file on the server.
- `summary <filename>`: Get a summary (minimum, maximum, average) of the contents of a file on the server.
- `help`: Get information about available commands.
- `bye`: Terminate the client session.

### Example Usage

Upload a File:
```sh
put example.txt
```

Download a File:
```sh
get example.txt
```

Rename a File:
```sh
change example.txt new_example.txt
```

Get File Summary:
```sh
summary numbers.txt
```

Request Help:
```sh
help
```

Terminate the Session:
```sh
bye
```

## Error Handling

The application includes error handling for common issues such as file not found, invalid commands, and socket errors. Appropriate error messages are displayed to the user to help diagnose problems.

## Debug Mode

Both client and server have a debug mode enabled which prints detailed information about the requests and responses. This can be controlled by setting the `DEBUG_MODE` variable to `True` or `False`.

## Contributions

Contributions are welcome! If you find any issues or have suggestions for improvements, please create a pull request or raise an issue on the project repository.
