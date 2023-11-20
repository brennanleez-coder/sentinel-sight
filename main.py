from gui import create_gui
from socket_client import start_socket
from db_queue_manager import DBQueueManager

if __name__ == "__main__":
    monitor_dir = "C:\\Users\\Cyber\\Downloads"
    dest_dir = "C:\\Users\\Cyber\\Desktop\\extractedApks"
    
    # macbook setup
    # monitor_dir = "/Users/brennanlee/Downloads/"
    # dest_dir = "/Users/brennanlee/Desktop/extractedApks/"
    monitoring_flag = {"active": False}  # Use a dict to allow for mutable flag

    db_queue_manager = DBQueueManager()
    sio = start_socket(db_queue_manager)

    
    create_gui(sio, db_queue_manager, monitor_dir, dest_dir, monitoring_flag)
