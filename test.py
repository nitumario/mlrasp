import os

# Change effective user ID to root temporarily
os.seteuid(0)

# Run the command as root
output = os.popen('whoami').read().strip()

# Restore effective user ID to the original user
os.seteuid(os.getuid())

print("Current user:", output)
