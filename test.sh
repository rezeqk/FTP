#!/bin/bash



# Create Client : with args 
# Include dbug flag?? 
#
#
run_test() {
    # Function body
    echo "Please Enter the Server's port"
    read port 
    ip_address="127.0.0.1"

    # run  Server with argument ip_address as argument 
    python3 Server/Server.py $ip_address


    #Run client Command 
    python3 Client/Client.py $ip_address $port  
    
  done
} 
