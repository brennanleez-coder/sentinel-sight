import socketio

import os
from file_operations import perform_check
from extract_info_from_apk import extract_info
from db import insert_into_hash_checks_table, check_if_record_exists
from hash_results import HashResult
from directory import directory_of_tools, apk_file_path, monitor_dir, dest_dir
sio = socketio.Client()
db_queue_manager = None




#global variable to store the callback function
gui_output_text_callback = None
global_monitoring_flag = None

directory_of_local_apks = dest_dir
db_queue_manager = None

def start_socket(queue_manager):
    global db_queue_manager
    db_queue_manager = queue_manager

    return sio

def connect_to_server(server, sio, output_text_callback, monitoring_flag):
    global gui_output_text_callback
    global global_monitoring_flag
    gui_output_text_callback = output_text_callback
    global_monitoring_flag = monitoring_flag
    
    try:
        sio.connect(server)
    except Exception as e:
        print(f"Error connecting to server: {e}")

    
@sio.on('process_apk')
def process_apk(data):
    if gui_output_text_callback is not None:
        gui_output_text_callback("Processing apk...\n\n")
        
        apk_info = data['incoming_apk_info']
        
        # Print Apk Information received from server
        apk_info_str = "\n".join([f"{key}: {value}" for key, value in apk_info.items()])
        gui_output_text_callback(apk_info_str + '\n\n')
        
        # Manual checking to ensure that there are no apks in downloads
        # Apks moved to dest_dir
        perform_check(monitor_dir, dest_dir, gui_output_text_callback)

        for filename in os.listdir(dest_dir):
            if filename.endswith(".apk"):
                apk_path = os.path.join(dest_dir, filename)
                apk_info = extract_info(directory_of_tools, apk_path)
                # print(f"Package Name: {type(apk_info['package_name'])}, Incoming Hash: {type(apk_info['app_hash'])}, App Cert Hash: {type(apk_info['app_cert_hash'])}, Permissions: {type(apk_info['permissions'])}, Result: {type(HashResult.UNCHECKED.value)}")

                # check if package name version code version name exists
                # if not, insert into db
                # else, do nothing
                if (db_queue_manager.enqueue_db_task(check_if_record_exists, apk_info['package_name'], apk_info['version_code'])):
                    db_queue_manager.enqueue_db_task(insert_into_hash_checks_table,
                                                    apk_info['package_name'],
                                                    apk_info['version_code'],
                                                    apk_info['version_name'],
                                                    apk_info['app_hash'],
                                                    "",
                                                    apk_info['app_cert_hash'],
                                                    "",
                                                    apk_info['permissions'],
                                                    "",
                                                    HashResult.PENDING.value)

                                   

        
    
    
if __name__ == '__main__':
    sio.connect('http://localhost:8000')  # Match the Flask server's address
    sio.wait()
