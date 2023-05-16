import os
import shutil
from datetime import datetime, timedelta

# Define the directory to search for incoming folders
directory = "/data"

# Get the current time
current_time = datetime.now()

# Loop through each subdirectory in the main directory
for subdirectory in os.scandir(directory):
    # Check if the subdirectory is a directory and has an "incoming" folder
    if subdirectory.is_dir() and os.path.isdir(os.path.join(subdirectory.path, "incoming")):
        print(f"Checking directory {subdirectory.path}")
        # Get the path of the "data.nimb" file
        data_nimb_path = os.path.join(subdirectory.path, "incoming", "data.nimb")
        # Check if the "data.nimb" file exists
        if os.path.exists(data_nimb_path):
            print(f"Found data.nimb file in {subdirectory.path}")
            # Get the modification time of the "data.nimb" file
            with open(data_nimb_path, "r") as f:
                date_str = f.read().split("\n")[1]  # assuming the date is the second line

            # parse the date string to a datetime object
            date = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")

            # calculate the difference between the date and the current time
            delta = datetime.now() - date

            # print the difference in hours
            print(f"Difference: {delta.total_seconds() / 3600:.2f} hours")
            diff = delta.total_seconds() / 3600
            if diff > 2:
                # Delete the subdirectory and print a message
                shutil.rmtree(subdirectory.path)
                os.system('sudo userdel ' + subdirectory.name)
                print(f"Deleted empty directory {subdirectory.name}")

        else:
            print(f"No data.nimb file found in {subdirectory.path}")
            # Delete the subdirectory and print a message
            shutil.rmtree(subdirectory.path)
            os.system('sudo userdel ' + subdirectory.name)
            print(f"Deleted empty directory {subdirectory.name}")
