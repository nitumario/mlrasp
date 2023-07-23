import time
import os
import shutil
from datetime import datetime, timedelta

directory = "/data"
while True:
    current_time = datetime.now()

    for subdirectory in os.scandir(directory):
        if subdirectory.is_dir() and os.path.isdir(os.path.join(subdirectory.path, "incoming")):
            print(f"Checking directory {subdirectory.path}")
            data_nimb_path = os.path.join(subdirectory.path, "incoming", "data.nimb")
            if os.path.exists(data_nimb_path):
                print(f"Found data.nimb file in {subdirectory.path}")
                with open(data_nimb_path, "r") as f:
                    content = f.read().split("\n")
                    premium = content[2]
                    date_str = content[1]
                date = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                delta = datetime.now() - date
                print(f"Difference: {delta.total_seconds() / 3600:.2f} hours")
                diff = delta.total_seconds() / 3600
                premium = premium.strip()
                if diff > 6:
                    shutil.rmtree(subdirectory.path)
                    os.system('sudo userdel ' + subdirectory.name)
                    print(f"Deleted outdated directory {subdirectory.name}")

            else:
                print(f"No data.nimb file found in {subdirectory.path}")
                shutil.rmtree(subdirectory.path)
                os.system('sudo userdel ' + subdirectory.name)
                print(f"Deleted empty directory {subdirectory.name}")
    time.sleep(10)
