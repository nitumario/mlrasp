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
dataFromServer = dataFromServer.decode()
datasave = open("header.txt", "w")
datasave.write(dataFromServer)
datasave.close
print(dataFromServer)
import paramiko
 
with paramiko.SSHClient() as ssh:
    ssh.load_system_host_keys()
    ssh.connect("192.168.1.24", username="test", password="toor")
 
    sftp = ssh.open_sftp()

    sftp.chdir('/incoming')
