import socket
import ftplib
import os
import uuid
from datetime import datetime
import paramiko

# Get the current date and time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("You are uploading at", dt_string)

# Get the hostname and create a socket
hostname = socket.gethostname()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.1.24", 9090))  # Connect to server
UUID = str(uuid.uuid4())
# Create the header data and save it to a file
header_data = "{ \n" + socket.gethostbyname(hostname) + "\n SCOPE:upload \n" + dt_string + "\n" + UUID + "\n}"
with open("header.txt", "w") as datasave:
    datasave.write(header_data)

# Send the header to the server and receive a response
client_socket.send(header_data.encode())
data_from_server = client_socket.recv(1024).decode()

# Save the response to a file and print it
with open("header_response.txt", "w") as datasave:
    datasave.write(data_from_server)
print(data_from_server)

# Get the USR and PASSWD values from the header response
with open("header_response.txt", "r") as header_file:
    header = header_file.read()
    usr = header.split("USR: ")[1].split("\n")[0]
    passwd = header.split("PASSWD: ")[1].split("\n")[0]
    usr = usr.strip()
    passwd = passwd.strip()
os.system("sudo rm header_response.txt")
premium = input("premium user?(1/0) \n")
# Connect to the server using SSH and SFTP
with open("data.nimb", 'w') as d:
    d.write(UUID + '\n' + dt_string + "\n" + premium)
with open('data.nimb', 'rb') as miau:
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect("192.168.1.24", username=usr, password=passwd)
        sftp = ssh.open_sftp()
        sftp.putfo(miau, '/incoming/' + "data.nimb") 
os.remove('data.nimb')
