from flask import Flask, render_template
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return "File has been uploaded."
    return render_template('index(1).html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

'''
import socket
import time

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
recived_f = 'imgt_thread'+str(time.time()).split('.')[0]+'.jpeg'
with open(recived_f, 'wb') as f:
    print('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            print('file close()')
            break
        # write data to a file
        f.write(data)

print('Successfully get the file')
s.close()
print('connection closed')
'''