import os
import shutil
from datetime import datetime
from directory import directory_of_local_apks, directory_of_tools
from extract_info_from_apk import extract_info
from db import get_all_legit_apk_info, get_db_connection, insert_into_legit_apk_info_table

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
            
    output_text(f"{get_timestamp()} - Processing downloaded apks...\n")

    conn = get_db_connection()
    cursor = conn.cursor()

    list_of_legit_apk_info = get_all_legit_apk_info(conn)
    if (len(list_of_legit_apk_info) == len(os.listdir(dest_dir))):
        output_text(f"{get_timestamp()} - legit_apk_info table is up to date.\n")
        return
    else:
        for filename in os.listdir(dest_dir):
            if filename.endswith(".apk"):
                apk_path = os.path.join(dest_dir, filename)
                info = extract_info(directory_of_tools, apk_path)
                app_hash, version_code, version_name, package_name, app_cert_hash, permissions = \
                info['app_hash'], info['version_code'], info['version_name'], info['package_name'], info['app_cert_hash'], info['permissions']
                is_package_present = cursor.execute("SELECT package_name FROM legit_apk_info_table WHERE package_name = ? AND version_code = ?", (package_name, version_code))
                if is_package_present.fetchone() is None:
                    insert_into_legit_apk_info_table(conn, package_name, app_hash, version_code, version_name, app_cert_hash, permissions)
                    output_text(f"{get_timestamp()} - Inserted {package_name} into legit_apk_info_table.\n")
                else:
                    print(f"Package {package_name} already exists in legit_apk_info_table.")
    output_text(f"{get_timestamp()} - legit_apk_info table is up to date.\n")
    output_text(f"{get_timestamp()} ===================================== \n")


