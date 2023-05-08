import os
import socket
import subprocess

def handle_client(client_connected):
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
        USR  = data[usr_start:usr_end]
        passwd_start = data.find("PASSWD: ") + 8
        passwd_end = data.find("\n", passwd_start)
        PASSWD = data[passwd_start:passwd_end]

        print("USR: ", USR)
        print("PASSWD: ", PASSWD)
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
start_server("192.168.1.24", 9090)
