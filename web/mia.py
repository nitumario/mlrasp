from flask import Flask, request, render_template, send_file
import paramiko
import ftplib
import os
import uuid
import random
from datetime import datetime
import socket
from io import BytesIO
from tempfile import SpooledTemporaryFile
import sqlite3

ip = "192.168.1.24"
db_file = "users.db"  # SQLite database file name

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
    os.system("sudo rm header.txt")

    # Generate a random 6-digit code
    code = str(random.randint(100000, 999999))

    # Create a new SQLite connection and cursor
    con = sqlite3.connect(db_file)
    cursor = con.cursor()

    # Create the users table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, code TEXT)")

    # Insert user information into the database
    cursor.execute("INSERT INTO users (username, password, code) VALUES (?, ?, ?)", (usr, passwd, code))
    con.commit()

    # Create a Paramiko SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=usr, password=passwd)

    # Create an SFTP client from the SSH client
    sftp = ssh.open_sftp()

    # Loop through each uploaded file and upload it to the SFTP server
    for uploaded_file in request.files.getlist('file'):
        filename = uploaded_file.filename
        sftp.putfo(uploaded_file, '/incoming/' + filename)

    sftp.close()
    ssh.close()

    con.close()  # Close the SQLite connection

    return render_template('success.html', code=code)

import logging

@app.route('/view', methods=['GET', 'POST'])
def view_files():
    try:
        con = sqlite3.connect("users.db")
        cursor = con.cursor()

        if request.method == 'POST':
            code = request.form.get('code')
            cursor.execute("SELECT username, password FROM users WHERE code = ?", (code,))
            user = cursor.fetchone()

            if user:
                username, password = user
                app.logger.info('Valid code: {}'.format(code))
                print('Code is valid')
                return render_template('view.html', username=username, password=password)
            else:
                app.logger.info('Invalid code: {}'.format(code))
                print('Code is invalid')
                return render_template('view.html', error="Invalid code")

        return render_template('view.html')

    except Exception as e:
        app.logger.error('An error occurred: {}'.format(str(e)))
        return render_template('view.html', error="An error occurred")

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


@app.route('/incoming/<path:file_path>')
def download_file(file_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=usr, password=passwd)
    transport = ssh.open_sftp()

    with SpooledTemporaryFile(1024000) as f:
        transport.get(file_path, os.path.basename(file_path))
        f.seek(0)
        return send_file(os.path.basename(file_path), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
