echo "Starting program"
echo "Initialisation!"
sleep 1
echo "1"
sleep 1 
echo "2"
sleep 1
echo "3"
sleep 1
sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo ufw status
sudo systemctl enable vsftpd.service
sudo systemctl start vsftpd.service
sudo systemctl restart vsftpd.service
sudo systemctl status vsftpd.service
echo "Starting main"
sudo bash main.sh
