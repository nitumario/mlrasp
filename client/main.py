import socket
import ftplib
import os
import uuid
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S") #get the time and date
print('you are uploading')
hostname=socket.gethostname()   
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("192.168.1.24",9090)) #connect to server
data = "{ \n" + socket.gethostbyname(hostname) + "\n SCOPE:upload \n" + dt_string + "\n" + str(uuid.uuid1()) +  "\n }" # creates the header
datasave = open("header.txt", "w")
datasave.write("{ \n" + socket.gethostbyname(hostname) + "\n SCOPE:upload \n" + dt_string + "\n" + str(uuid.uuid1()) +  "\n }") #saves it in header.txt
datasave.close
clientSocket.send(data.encode()) #send the header
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode())
