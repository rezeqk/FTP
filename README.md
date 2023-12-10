# FTP protocol

- FTP client contacts FTP server at port 21 using TCP
- client authorized over control connection
- client sends commands over control connection
- when server recieves file transfer command, server opens another TCP `Data`
  connection for file to client
- After transfering file, server closes connection
- if needed anothe

# TODO

- [ ] Make sure server can connect to multiple client <sub>
- [ ] implement udp connection
- [ ] fix the change function
- [ ] text
- [ ] text
