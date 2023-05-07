import os
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.1.24", 9090))
server_socket.listen()

while True:
    (client_connected, client_address) = server_socket.accept()
    print("Accepted a connection request from %s:%s" % (client_address[0], client_address[1]))
    
    # Receives the header
    data_from_client = client_connected.recv(1024)
    print(data_from_client.decode())
    
    # Saves it to datafromclient.txt
    with open("datafromclient.txt", "w") as datasave:
        datasave.write(data_from_client.decode())
    
    os.system("sudo bash main.sh")

    with open('tempdata.txt', 'r') as f:
        data = f.read()
        usr_start = data.find("USR: ") + 5
        usr_end = data.find("\n", usr_start)
        usr = data[usr_start:usr_end]
        passwd_start = data.find("PASSWD: ") + 8
        passwd_end = data.find("\n", passwd_start)
        passwd = data[passwd_start:passwd_end]

        print("USR: ", usr)
        print("PASSWD: ", passwd)
    os.system("sudo useradd -g sftp -d /upload -s /sbin/nologin " + usr)
    os.system("passwd" + usr)
    os.system(passwd)
    os.system(passwd)
    with open("tempdata.txt", "r") as tempfile:
        tempdata = " ".join(tempfile.readlines())
        print("\n", tempdata)
        client_connected.send(tempdata.encode())
    os.system("sudo rm tempdata.txt")
