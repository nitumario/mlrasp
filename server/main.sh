python3 cred.py
usr=$(head -n 1 creds.txt)
passwd=$(sed -n '2{p;q;}' creds.txt)
echo $usr
echo $passwd
set -o noclobber
printf "{ \n UUID: $uuid \n USR: $usr \n PASSWD: $passwd \n DATE: $(date +"%m %d %Y %H:%M:%S") \n }, \n" >> data.txt
