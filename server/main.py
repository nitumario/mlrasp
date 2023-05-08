import os
import socket
import subprocess
import time
import random
import string
import datetime
def init():
    print("Starting the initialisation phase. \n")
    # Allow ports 20, 21, and 22
    subprocess.run(['sudo', 'ufw', 'allow', '20/tcp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'ufw', 'allow', '21/tcp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'ufw', 'allow', '22/tcp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)    
    # Show UFW status
    subprocess.run(['sudo', 'ufw', 'status'])

def creds():
    def get_random_string():
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(24))
        return result_str
    global PASSWD
    global USR
    PASSWD = get_random_string()
    USR = get_random_string()
    with open('datafromclient.txt', 'r') as f:
        lines = f.readlines()
        ip = lines[1].strip()
        uuid = lines[-2].strip()

    print(f'IP: {ip}')
    print(f'UUID: {uuid}')

    # Remove input files
    os.remove("datafromclient.txt")
    # Append credentials to data.txt and tempdata.txt
    with open("data.txt", "a") as f:
        f.write("{ \n UUID: %s \n IP: %s \n USR: %s \n PASSWD: %s \n DATE: %s \n }, \n"
            % (uuid, ip, USR, PASSWD, datetime.datetime.now()))
    with open("tempdata.txt", "w") as f:
        f.write("{ \n UUID: %s \n IP: %s \n USR: %s \n PASSWD: %s \n DATE: %s \n }, \n"
            % (uuid, ip, USR, PASSWD, datetime.datetime.now()))
    # Set permissions on tempdata.txt
    os.system("sudo chmod -R a+rwx tempdata.txt")


def handle_client(client_connected):
    # Receives the header
    data_from_client = client_connected.recv(1024)
    print(data_from_client.decode())    
    
    # Saves it to datafromclient.txt
    with open("datafromclient.txt", "w") as datasave:
        datasave.write(data_from_client.decode())
    creds()
    global PASSWD
    global USR
    USR = USR.strip()
    PASSWD = PASSWD.strip()    
        # create user and set home directory to /upload and login shell to /sbin/nologin
    subprocess.run(["useradd", "-g", "sftp", "-d", "/incoming", "-s", "/sbin/nologin", USR])

        # set the password for the user
    proc = subprocess.Popen(["passwd", USR], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.write(f"{PASSWD}\n{PASSWD}\n".encode())
    proc.communicate()

        # create incoming directory and set permissions
    subprocess.run(["mkdir", "-p", f"/data/{USR}/incoming"])
    subprocess.run(["chown", "-R", "root:sftp", f"/data/{USR}"])
    subprocess.run(["chown", "-R", f"{USR}:sftp", f"/data/{USR}/incoming"])

    with open("tempdata.txt", "r") as tempfile:
        tempdata = " ".join(tempfile.readlines())
        print("\n", tempdata)
        client_connected.send(tempdata.encode())
            
    os.system("sudo rm tempdata.txt")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        (client_connected, client_address) = server_socket.accept()
        print("Accepted a connection request from %s:%s" % (client_address[0], client_address[1]))
        
        handle_client(client_connected)
        
    server_socket.close()

# example usage:
init()
start_server("192.168.1.24", 9090)
