import socketio

import os
from file_operations import perform_check
from extract_info_from_apk import extract_info
from db import insert_incoming_data_into_hash_checks_table,insert_into_hash_checks_table
from hash_results import HashResult

sio = socketio.Client()
db_queue_manager = None




#global variable to store the callback function
gui_output_text_callback = None
global_monitoring_flag = None


directory_of_local_apks = "C:\\Users\\Cyber\\Desktop\\extractedApks\\"
monitor_dir = "C:\\Users\\Cyber\\Downloads"
dest_dir = "C:\\Users\\Cyber\\Desktop\\extractedApks"
directory_of_tools = "C:\\Users\\Cyber\\AppData\\Local\\Android\\Sdk\\build-tools\\33.0.1\\"
db_queue_manager = None

def start_socket(queue_manager):
    global db_queue_manager
    db_queue_manager = queue_manager

    return sio

@sio.event
def message(data):
    print('I received a message!')

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
        gui_output_text_callback(data['message'] + '\n')
        apk_info = data['incoming_apk_info']
        apk_info_str = "\n".join([f"{key}: {value}" for key, value in apk_info.items()])
        gui_output_text_callback(apk_info_str + '\n')
        
        # manual checking to ensure that there are no apks in downloads
        # apks moved to dest_dir
        perform_check(monitor_dir, dest_dir, gui_output_text_callback)

        for filename in os.listdir(dest_dir):
            if filename.endswith(".apk"):
                apk_path = os.path.join(dest_dir, filename)
                # print(filename)
                # print(extract_info(directory_of_tools, apk_path))
                apk_info = extract_info(directory_of_tools, apk_path)
                # print(f"Package Name: {type(apk_info['package_name'])}, Incoming Hash: {type(apk_info['app_hash'])}, App Cert Hash: {type(apk_info['app_cert_hash'])}, Permissions: {type(apk_info['permissions'])}, Result: {type(HashResult.UNCHECKED.value)}")

                db_queue_manager.enqueue_db_task(insert_into_hash_checks_table,
                                                apk_info['package_name'],
                                                apk_info['app_hash'],
                                                "",
                                                apk_info['app_cert_hash'],
                                                "",
                                                apk_info['permissions'],
                                                "",
                                                HashResult.UNCHECKED.value)

                                   

        
    
    
if __name__ == '__main__':
    sio.connect('http://localhost:8000')  # Match the Flask server's address
    sio.wait()
