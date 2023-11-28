import socketio

import os
from file_operations import perform_check, get_timestamp
from extract_info_from_apk import extract_info
from db import insert_into_hash_checks_table, check_if_record_exists
from hash_results import HashResult
from db import get_db_connection
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
        perform_check(monitor_dir, dest_dir, gui_output_text_callback)


        # check if package name version code version name exists
        # if not, insert into db
        # else, do nothing

        conn = get_db_connection()
        cursor = conn.cursor()
        # If record does not exist in hash_checks_table
        gui_output_text_callback(f"CHECK IF RECORD EXISTS: ${check_if_record_exists(conn, apk_info['package_name'], apk_info['version_code'])}")


        if not check_if_record_exists(conn, apk_info['package_name'], apk_info['version_code']):
            db_queue_manager.enqueue_db_task(insert_into_hash_checks_table,
                                            apk_info['package_name'],
                                            apk_info['version_code'],
                                            apk_info['version_name'],
                                            apk_info['apk_hash'],
                                            "",
                                            apk_info['app_cert_hash'],
                                            "",
                                            apk_info['permissions'],
                                            "",
                                            HashResult.PENDING.value)
            gui_output_text_callback(f"{get_timestamp()} - Inserted {apk_info['package_name']} into hash_checks_table.\n")

            cursor.execute("SELECT package_name FROM legit_apk_info_table WHERE package_name = ? AND version_code = ?", ( apk_info['package_name'], apk_info['version_code']))
            result = cursor.fetchone()
            print(result)
            # Check if record exists in legit_apk_info_table
            if result: 
                # update hash_checks_table downloaded fields
                cursor.execute("UPDATE hash_checks_table SET downloaded_hash = ?, downloaded_app_cert_hash = ?, downloaded_permissions = ? WHERE package_name = ? AND version_code = ?",
                                (apk_info['apk_hash'], apk_info['app_cert_hash'], apk_info['permissions'], apk_info['package_name'], apk_info['version_code']))
                
                conn.commit()
                # Using hash_results enum, determine level of apk legitimacy
                # and update hash_checks_table result field
                # is_same_app_hash = apk_info['app_hash'] == expected_info['app_hash']
                # is_same_app_cert_hash = apk_info['app_cert_hash'] == expected_info['app_cert_hash']
                # is_same_permissions = apk_info['permissions'] == expected_info['permissions']

                # gui_output_text_callback(f"{get_timestamp()} - Updated {apk_info['package_name']} in hash_checks_table.\n")

        else:
            gui_output_text_callback(f"Package {apk_info['package_name']} already exists in hash_checks_table.")
                                   

        
    
    
if __name__ == '__main__':
    sio.connect('http://localhost:8000')  # Match the Flask server's address
    sio.wait()
