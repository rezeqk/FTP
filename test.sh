#!/bin/bash

echo "Please Enter the Server's port"
read port 
ip_address="127.0.0.1"

# Check if a session with the name "server_session" already exists
if tmux has-session -t server_session 2>/dev/null; then
 echo "A session named 'server_session' already exists. Killing it..."
 tmux kill-session -t server_session
fi

# Start a new tmux session and run the Server script
unset TMUX
tmux new-session -d -s server_session "python3 Server/Server.py $ip_address $port

# Check if the session was created successfully
if ! tmux has-session -t server_session 2>/dev/null; then
 echo "Failed to create session 'server_session'"
 exit 1
fi

# Split the window and run the Client script
tmux split-window -h "python3 Client/Client.py $ip_address $port

# Attach to the session
tmux attach-session -t server_session

# Continuously check if the programs are running
while true; do
 # Check if the Server script is running
 if ! tmux has-session -t server_session 2>/dev/null; then
 echo "Server script is not running"
 break
 fi

 # Check if the Client script is running
 if ! tmux has-session -t server_session 2>/dev/null; then
 echo "Client script is not running"
 break
 fi

 # Sleep for a while before checking again
 sleep 1
done

# Kill all panes except the current one
tmux kill-pane -a

# Return to a normal terminal
exit
