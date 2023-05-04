import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("127.0.0.1",9090))
data = "Hello Server!"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode())