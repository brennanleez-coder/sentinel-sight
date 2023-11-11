from gui import create_gui

if __name__ == "__main__":
    monitor_dir = "C:\\Users\\Cyber\\Downloads"
    dest_dir = "../extractedApks/"
    monitoring_flag = {"active": False}  # Use a dict to allow for mutable flag

    create_gui(monitor_dir, dest_dir, monitoring_flag)
