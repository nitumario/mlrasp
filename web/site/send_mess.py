import socket
import ftplib
print('you are uploading')
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("192.168.0.9",9090))
data = input("Spune-i ceva server-ului? ")
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode())
