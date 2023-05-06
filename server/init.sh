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
sudo ufw allow 22/tcp
sudo ufw status
echo "Starting main"
sudo python3 main.py
