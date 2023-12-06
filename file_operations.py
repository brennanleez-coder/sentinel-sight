import os
import shutil
from datetime import datetime
from directory import directory_of_local_apks, directory_of_tools
from extract_info_from_apk import extract_info
from db import get_all_legit_apk_info, get_db_connection, insert_into_legit_apk_info_table
import platform

def get_timestamp():
    return datetime.now().strftime("%Y_%m_%d %H_%M_%S")

# Perform check on downloaded apks
# @params: monitor_dir: directory to monitor for downloaded apks
# @params: dest_dir: directory to move downloaded apks to
# @params: output_text: function to output text to GUI

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
            
    output_text(f"{get_timestamp()} - Processing downloaded apks...\n")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    for filename in os.listdir(dest_dir):
        if filename.endswith(".apk"):
            apk_path = os.path.join(dest_dir, filename)
            info = extract_info(directory_of_tools, apk_path)
            app_hash, version_code, version_name, package_name, app_cert_hash, permissions = \
            info['app_hash'], info['version_code'], info['version_name'], info['package_name'], info['app_cert_hash'], info['permissions']
            is_package_present = cursor.execute("SELECT package_name FROM legit_apk_info_table WHERE package_name = ? AND version_code = ?", (package_name, version_code))
            if is_package_present.fetchone() is None:
                insert_into_legit_apk_info_table(conn, package_name, app_hash, version_code, version_name, app_cert_hash, permissions)
                output_text(f"{get_timestamp()} - Inserted {package_name}: version code: {info['version_code']} into legit_apk_info_table.\n")
            else:
                print(f"Package {package_name}: version code: {info['version_code']} already exists in legit_apk_info_table.")
    output_text(f"{get_timestamp()} - legit_apk_info table is up to date.\n")
    output_text(f"{get_timestamp()} ===================================== \n")


# Extract logs from GUI
# @params: output_text: function to output text to GUI
# @params: filename, name of file to save to desktop
# @params: tk, tkinter object
def save_scrolledtext_to_file(output_text_widget, filename, tk):
    # Retrieve the entire text from the ScrolledText widget
    full_text = output_text_widget.get("1.0", tk.END)


    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        
    file_path = os.path.join(desktop_path, filename)

    print(desktop_path)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(full_text)
        

    

    print(f"File saved to {file_path}")