python3 cred.py
usr=$(head -n 1 creds.txt)
passwd=$(sed -n '2{p;q;}' creds.txt)
echo $usr
echo $passwd