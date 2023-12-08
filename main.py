import subprocess

print("Please Enter the Server's port")
port = input()
ip_address = "127.0.0.1"

print("Running Server and Client scripts in parallel")

# Run the Server script
server_process = subprocess.Popen(["python3", "Server/Server.py", ip_address, port], stdout=subprocess.PIPE)

# Run the Client script
client_process = subprocess.Popen(["python3", "Client/Client.py", ip_address, port], stdout=subprocess.PIPE)

# Wait for both processes to complete
server_output, server_error = server_process.communicate()
client_output, client_error = client_process.communicate()

# Print the output of both scripts
if server_output:
   print(server_output.decode())
if client_output:
   print(client_output.decode())
