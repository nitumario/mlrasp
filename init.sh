sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo ufw status
sudo systemctl enable vsftpd.service
sudo systemctl start vsftpd.service
sudo systemctl restart vsftpd.service
sudo systemctl status vsftpd.service