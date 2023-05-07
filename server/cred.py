import random
import string

def get_random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(24))
    return result_str

passw = get_random_string()
usr = get_random_string()

with open("creds.txt", 'w') as file:
    pass

creds = open("creds.txt", "w")
creds.write(passw)
creds.write('\n')
creds.write(usr)
creds.close()
