import socketio
from file_operations import perform_check, get_timestamp
from db import insert_into_hash_checks_table, check_if_record_exists
from hash_results import HashResult, determine_apk_legitimacy
from db import get_db_connection
from directory import monitor_dir, dest_dir

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
def process_apk(data=None):
    from gui import get_apk_info # import here to avoid circular import

    perform_check(monitor_dir, dest_dir, gui_output_text_callback)
    
    if gui_output_text_callback is not None and data is not None:

        # Pass apk info to gui
        get_apk_info(data)

        gui_output_text_callback("Processing retrieved apk...\n")
        
        gui_output_text_callback(f"{get_timestamp()} ============APK Received============= \n")
        apk_info = data['incoming_apk_info']
        
        # Print Apk Information received from server
        apk_info_str = "\n".join([f"{key}: {value}" for key, value in apk_info.items()])
        gui_output_text_callback(apk_info_str + '\n')

        gui_output_text_callback(f"{get_timestamp()} ===================================== \n")

        # check if package name version code version name exists
        # if not, insert into db
        # else, do nothing

        conn = get_db_connection()
        cursor = conn.cursor()
        

        # If record does not exist in hash_checks_table, insert into table
        if not check_if_record_exists(conn, apk_info['package_name'], apk_info['version_code']):
            db_queue_manager.enqueue_db_task(insert_into_hash_checks_table,
                                            apk_info['package_name'],
                                            apk_info['version_name'],
                                            apk_info['version_code'],
                                            apk_info['apk_hash'],
                                            "",
                                            apk_info['app_cert_hash'],
                                            "",
                                            apk_info['permissions'],
                                            "",
                                            HashResult.PENDING.value)
        gui_output_text_callback(f"{get_timestamp()} - {apk_info['package_name']}: {apk_info['version_code']} pending APK check....\n")        

        evaluate_apk(apk_info, get_apk_info, conn, cursor)

def evaluate_apk(apk_info, get_apk_info, conn, cursor):
    cursor.execute("SELECT package_name, apk_hash, app_cert_hash, permissions FROM legit_apk_info_table WHERE package_name = ? AND version_code = ?", ( apk_info['package_name'], apk_info['version_code']))
    result = cursor.fetchone()
        # Check if record exists in legit_apk_info_table
    if result:
        downloaded_hash = result[1]
        downloaded_app_cert_hash = result[2]
        downloaded_permissions = result[3]

        print(f"incominga_app_cert_hash: {apk_info['app_cert_hash']}")
        print(f"downloaded_app_cert_hash: {downloaded_app_cert_hash}")
        print(apk_info['app_cert_hash'] == downloaded_app_cert_hash)
            
        apk_legitimacy = determine_apk_legitimacy(
                incoming_apk_hash=apk_info['apk_hash'],
                downloaded_apk_hash=downloaded_hash,
                incoming_app_cert_hash=apk_info['app_cert_hash'],
                downloaded_app_cert_hash=downloaded_app_cert_hash,
                incoming_permissions=apk_info['permissions'],
                downloaded_permissions=downloaded_permissions
            )
        
        # print(apk_info['permissions'])
        # print(downloaded_permissions)
            
            # update hash_checks_table downloaded fields
        query = """
            UPDATE hash_checks_table
            SET
                downloaded_hash = ?,
                downloaded_app_cert_hash = ?,
                downloaded_permissions= ?,
                checked_time = ?,
                result= ?
            WHERE
                package_name = ?
                AND
                version_code = ?;
            """
        cursor.execute(query, (apk_info['apk_hash'],
                                    apk_info['app_cert_hash'],
                                    apk_info['permissions'],
                                    get_timestamp(),
                                    apk_legitimacy,
                                    apk_info['package_name'],
                                    apk_info['version_code'])
                            )
        conn.commit()         
        gui_output_text_callback(f"{get_timestamp()} =============APK Result============== \n")       
        gui_output_text_callback(f"{get_timestamp()} - {apk_info['package_name']} - version: {apk_info['version_code']} legitimacy: {apk_legitimacy}.\n")
        gui_output_text_callback(f"{get_timestamp()} ===================================== \n")
        get_apk_info(None)   

    else:
        gui_output_text_callback(f"{get_timestamp()} - {apk_info['package_name']} - version: {apk_info['version_code']} awaiting downloaded APK.\n")
        gui_output_text_callback(f"{get_timestamp()} ===================================== \n")

                                   

        
    
    
if __name__ == '__main__':
    sio.connect('http://localhost:8000')  # Match the Flask server's address
    sio.wait()
