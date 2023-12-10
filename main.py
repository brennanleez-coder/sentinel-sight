from gui import create_gui
from socket_client import start_socket
from db_queue_manager import DBQueueManager
from directory import monitor_dir, dest_dir


# Main entry point into the GUI application
if __name__ == "__main__":
    monitoring_flag = {"active": False}  # Use a dict to allow for mutable flag

    db_queue_manager = DBQueueManager()
    sio = start_socket(db_queue_manager)

    
    create_gui(sio, db_queue_manager, monitor_dir, dest_dir, monitoring_flag)
