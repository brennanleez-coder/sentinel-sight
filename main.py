from gui import create_gui
from socket_client import start_socket
from db_queue_manager import DBQueueManager
from test_flask import run_flask
from threading import Thread
from directory import monitor_dir, dest_dir

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    monitoring_flag = {"active": False}  # Use a dict to allow for mutable flag

    db_queue_manager = DBQueueManager()
    sio = start_socket(db_queue_manager)

    
    create_gui(sio, db_queue_manager, monitor_dir, dest_dir, monitoring_flag)
