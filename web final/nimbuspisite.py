from flask import Flask, request, render_template, redirect, url_for, send_from_directory, send_file
import paramiko
import ftplib
import os
import uuid
from datetime import datetime
import socket
from io import BytesIO
from tempfile import SpooledTemporaryFile
ip = "192.168.33.116"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indexmain.html')

@app.route('/success', methods=['POST'])
def success():
    # Get the current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("You are uploading at", dt_string)

# Get the hostname and create a socket
    hostname = socket.gethostname()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, 9090))  # Connect to server

# Create the header data and save it to a file
    header_data = "{ \n" + socket.gethostbyname(hostname) + "\n SCOPE:upload \n" + dt_string + "\n" + str(uuid.uuid4()) + "\n}"
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
    # Create a Paramiko SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username="pz83rjlkdeh3em5ld3fw12d7", password="pula")

    # Create an SFTP client from the SSH client
    sftp = ssh.open_sftp()

    # Loop through each uploaded file and upload it to the SFTP server
    for uploaded_file in request.files.getlist('file'):
        filename = uploaded_file.filename
        sftp.putfo(uploaded_file, '/incoming/' + filename)

    fisier = "miau.txt"
    remote_path = "/incoming/" + fisier
    local_path = "C:/Users/vlada/Desktop/pula/" + fisier

    with open(local_path, "wb") as local_file:
        sftp.getfo(remote_path, local_file)

    return render_template('succes.html')

    sftp.close()
    ssh.close()

@app.route('/view')
def view_files():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username="pz83rjlkdeh3em5ld3fw12d7", password="pula")

        # Create an SFTP client from the SSH client
        sftp = ssh.open_sftp()
        # Change to the desired directory on the SFTP server
        sftp.chdir("/incoming/")

        # Get the list of files in the directory
        files = sftp.listdir()

        # Create a list of dictionaries containing file name and file path
        file_info = []
        for file in files:
            file_path = sftp.normalize('/incoming/' + file)
            file_info.append({'file': file, 'file_path': file_path})

        # Close the SFTP session
        sftp.close()

    finally:
        # Close the SSH connection
        ssh.close()

    # Render the template with the file information
    return render_template('view.html', file_info=file_info)

@app.route('/incoming/<path:file_path>')
def download_file(file_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username="pz83rjlkdeh3em5ld3fw12d7", password="pula")
    transport = client.open_sftp()

    with SpooledTemporaryFile(1024000) as f:
        transport.get(file_path, os.path.basename(file_path))
        f.seek(0)
        return send_file(os.path.basename(file_path), as_attachment=True)





if __name__ == '__main__':
    app.run(debug=True)

























































"""
from flask import Flask, request, render_template, redirect, url_for
import paramiko
import os
import socket
import subprocess
import time
import random
import string
import datetime
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods=['POST'])
def success():
    # Create a Paramiko SSH client
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

# Connect to the server using SSH and SFTP
   # Create a Paramiko SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.33.116', username=usr, password=passwd)

    # Create an SFTP client from the SSH client
    sftp = ssh.open_sftp()

    # Loop through each uploaded file and upload it to the SFTP server
    for uploaded_file in request.files.getlist('file'):
        filename = uploaded_file.filename
        sftp.putfo(uploaded_file, '/incoming/' + filename)

    # Close the SFTP client and SSH client
    sftp.close()
    ssh.close()
    return render_template('succes.html')

if __name__ == '__main__':
    app.run(debug=True)
"""
