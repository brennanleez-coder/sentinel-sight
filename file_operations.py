import os
import shutil
from datetime import datetime

# Function to get the current timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def perform_check(monitor_dir, dest_dir, output_text):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    apk_files = [f for f in os.listdir(monitor_dir) if f.endswith('.apk')]
    if not apk_files:
        output_text(f"{get_timestamp()} - No files to move.\n")
    else:
        for file in apk_files:
            source_file = os.path.join(monitor_dir, file)
            destination_file = os.path.join(dest_dir, file)
            shutil.move(source_file, destination_file)
            output_text(f"{get_timestamp()} - Moved file: {file}\n")
