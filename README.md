# FTP protocol

- FTP client contacts FTP server at port 21 using TCP
- client authorized over control connection
- client sends commands over control connection
- when server recieves file transfer command, server opens another TCP `Data`
  connection for file to client
- After transfering file, server closes connection
- if needed anothe

# TODO

- [x] Make sure server can connect to multiple client <sub>
- [x] implement udp connection
- [x] fix the change function
- [x] implement byte transfer
- [x] need a way to send to client or server an error if something bad occru
