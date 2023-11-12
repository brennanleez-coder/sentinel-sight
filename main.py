from gui import create_gui
from socket_client import start_socket
if __name__ == "__main__":
    # monitor_dir = "C:\\Users\\Cyber\\Downloads"
    # dest_dir = "../extractedApks/"
    
    # macbook setup
    monitor_dir = "/Users/brennanlee/Downloads/"
    dest_dir = "/Users/brennanlee/Desktop/extractedApks/"
    monitoring_flag = {"active": False}  # Use a dict to allow for mutable flag
    sio = start_socket()

    
    create_gui(sio, monitor_dir, dest_dir, monitoring_flag)
