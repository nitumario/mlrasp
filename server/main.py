"""
atunci cand clientul contacteaza serverul, ii trimite uuidul, apoi acesta ii trimite user&parola, clientul urmand sa uploadeze fisierele in ftp
"""

import os
import socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("127.0.0.1",9090))
serverSocket.listen()
while(True):
	(clientConnected, clientAddress) = serverSocket.accept()
	print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
	dataFromClient = clientConnected.recv(1024) #recieves the header
	print(dataFromClient.decode())
	x = dataFromClient.decode()
	datasave = open("datafromclient.txt", "w")
	datasave.write(x) #saves it to datafromclient.txt
	datasave.close()
	os.system("sudo bash main.sh")
	tempfile = open("tempdata.txt", "w")
	tempdata = tempfile.readlines()
	print("\n tempdata")
	clientConnected.send(tempdata.encode())
