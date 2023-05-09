#06.05.2023
import pysftp

with pysftp.Connection('192.168.1.24', username='test', password='toor') as sftp:
    with sftp.cd('/allcode'):
        sftp.put('/pycode/filename')
        sftp.get('remote_file')
