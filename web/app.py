import time
from flask import Flask, request, render_template, send_file, make_response
import paramiko
import os
import uuid
import random
from datetime import datetime
import socket
from tempfile import SpooledTemporaryFile
import sqlite3
import logging
import traceback
from stat import S_ISDIR

ip = "192.168.1.5"
db_file = "users.db"
app = Flask(__name__)
username = None
password = None
con = sqlite3.connect(db_file)
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, code TEXT, uuid TEXT)")
# Check if 'uuid' column already exists in 'users' table
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
if any(column[1] == 'uuid' for column in columns):
    pass
else:
    cursor.execute("ALTER TABLE users ADD COLUMN uuid TEXT")
con.commit()
con.close()
ip_address = "192.168.130.32" 

@app.route('/')
def index():
    return render_template('indexmain.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


def cleanup_uploaded_files(filenames):
    for filename in filenames:
        file_path = os.path.join(app.root_path, filename) 
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            app.logger.warning("File not found: {}".format(file_path))


@app.route('/success', methods=['POST'])
def success():
    try:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("You are uploading at", dt_string)

        hostname = socket.gethostname()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, 9090))  
        UUID = str(uuid.uuid4())
        header_data = "{ \n" + socket.gethostbyname(hostname) + "\n SCOPE:upload \n" + dt_string + "\n" + UUID + "\n}"
        with open("header.txt", "w") as datasave:
            datasave.write(header_data)

        client_socket.send(header_data.encode())
        data_from_server = client_socket.recv(1024).decode()

        with open("header_response.txt", "w") as datasave:
            datasave.write(data_from_server)
        print(data_from_server)

        with open("header_response.txt", "r") as header_file:
            header = header_file.read()
            usr = header.split("USR: ")[1].split("\n")[0].strip()
            passwd = header.split("PASSWD: ")[1].split("\n")[0].strip()
        os.system("sudo rm header_response.txt")
        os.system("sudo rm header.txt")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=usr, password=passwd)
        print('a trecut')
        sftp = ssh.open_sftp()
        with open("data.nimb", 'w') as d:
            d.write(UUID + '\n' + dt_string + "\n")
        with open('data.nimb', 'rb') as miau:
            sftp.putfo(miau, '/incoming/' + "data.nimb")
        os.remove('data.nimb')
        code = str(random.randint(1000000000, 9999999999))
        con = sqlite3.connect(db_file)
        cursor = con.cursor()
        cursor.execute("INSERT INTO users (username, password, code, uuid) VALUES (?, ?, ?, ?)",
                       (usr, passwd, code, UUID))
        con.commit()


        uploaded_filenames = [] 

        for uploaded_file in request.files.getlist('file'):
            filename = uploaded_file.filename
            uploaded_filenames.append(filename) 
            sftp.putfo(uploaded_file, '/incoming/' + filename)
        sftp.close()
        ssh.close()

        cleanup_uploaded_files(uploaded_filenames)

        return render_template('success.html', code=code, filenames=uploaded_filenames)

    except Exception as e:
        traceback.print_exc() 
        app.logger.error('An error occurred: {}'.format(str(e)))
        return render_template('error.html', message="An error occurred")

def send_filenames(filenames):
    try:
        hostname = socket.gethostname()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, 80))  
        time.sleep(1)

        # Format filenames with each name on a different line
        formatted_filenames = '\n'.join(filenames).encode()

        client_socket.send(formatted_filenames)
        time.sleep(1)
        #client_socket.close()

    except Exception as e:
        app.logger.error('An error occurred while sending filenames: {}'.format(str(e)))


@app.route('/view', methods=['GET', 'POST'])
def view():
    global username, password
    cursor = None
    con = None
    ssh = None
    file_info = []
    try:
        code = request.form.get('code')
        con = sqlite3.connect(db_file)
        cursor = con.cursor()
        cursor.execute("SELECT username, password FROM users WHERE code = ?", (code,))
        user = cursor.fetchone()

        if user:
            username, password = user
            app.logger.info('Valid code: {}'.format(code))
            print('Code is valid')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)
            sftp = ssh.open_sftp()
            sftp.chdir("/incoming/")

            files = sftp.listdir_attr()

            for file in files:
                if S_ISDIR(file.st_mode):
                    folder_path = sftp.normalize('/incoming/' + file.filename)
                    folder_files = sftp.listdir_attr(folder_path)
                    for folder_file in folder_files:
                        file_path = sftp.normalize(folder_path + '/' + folder_file.filename)
                        file_info.append({'file': folder_file.filename, 'file_path': file_path})
                else:
                    file_path = sftp.normalize('/incoming/' + file.filename)
                    file_info.append({'file': file.filename, 'file_path': file_path})

            sftp.close()
        else:
            app.logger.info('Invalid code: {}'.format(code))
            print('Code is invalid')

        sort_param = request.args.get('sort')
        if sort_param == '1':
            print('started')
            print(username)
            os.system("python3 /home/nimbus-pi/mlrasp/server/ml/classify_image.py -f /data/" + username + "/incoming")
            print('finished')

    except Exception as e:
        app.logger.error('An error occurred: {}'.format(str(e)))
        return render_template('error.html', message="An error occurred")

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
        if ssh:
            ssh.close()

        return render_template('view.html', file_info=file_info)


@app.route('/incoming/<path:file_path>')
def download_file(file_path):
    global username, password
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password)
    transport = ssh.open_sftp()

    try:
        with SpooledTemporaryFile(1024000) as f:
            transport.get(file_path, os.path.basename(file_path))
            f.seek(0)
            return send_file(os.path.basename(file_path), as_attachment=True)

    except Exception as e:
        app.logger.error('An error occurred: {}'.format(str(e)))
        return render_template('error.html', error="An error occurred during file download.")

    finally:
        transport.close()
        ssh.close()


if __name__ == '__main__':
    app.run(host='192.168.1.5', port=5555, debug=True)
