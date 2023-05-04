from flask import Flask, render_template
import socket
import ftplib
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
    #print ('I got clicked!')
    #print('you are uploading')
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("192.168.0.9",9090))
    data = "sugi"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    return data
    print(dataFromServer.decode())

if __name__ == '__main__':
  app.run(debug=True)
