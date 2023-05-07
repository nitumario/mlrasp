#!/bin/bash

echo "Starting program"
echo "Initialisation!"

for i in {1..5}; do
    echo $i
    sleep 1
done

sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo ufw allow 22/tcp
sudo ufw status

echo "Starting main"
sudo python3 main.py
