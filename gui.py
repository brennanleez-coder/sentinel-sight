import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import threading
import time
from file_operations import perform_check
from db import get_db_connection
import sqlite3
from socket_client import start_socket, connect_to_server, update_message



def start_monitoring_thread(sio, monitor_dir, dest_dir, output_text_callback, monitoring_flag):
    if not monitoring_flag["active"]:
        monitoring_flag["active"] = True
        output_text_callback("Monitoring started...\n")
        
        connect_to_server('http://localhost:8000', sio, output_text_callback)
        output_text_callback("Socket open...\n")

        monitor_thread = threading.Thread(target=monitor_directory, args=(monitor_dir, dest_dir, output_text_callback, monitoring_flag))
        monitor_thread.daemon = True
        monitor_thread.start()

def monitor_directory(monitor_dir, dest_dir, output_text_callback, monitoring_flag):
    output_text_callback("Listener triggered...\n")
    while monitoring_flag["active"]:
        perform_check(monitor_dir, dest_dir, output_text_callback)
        time.sleep(50)  # Check every 50 seconds

def open_database_view(db_file='verified_apk_data.db'):
    # Create a new top-level window
    db_window = tk.Toplevel()
    db_window.title("Verified Apk Viewer")
    db_window.geometry("800x800")
    

    # Create a frame for the Treeview and the scrollbars
    tree_frame = tk.Frame(db_window)
    tree_frame.pack(fill='both', expand=True)

    columns = ("ID", "Package Name", "APK Hash", "Version Code", "Version Number", "Cert Hash", "Created At", "Updated At")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    v_scroll.pack(side='right', fill='y')

    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    h_scroll.pack(side='bottom', fill='x')

    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    tree.pack(fill='both', expand=True)

    # Configure column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='w')  # adjust the alignment as needed

    # Function to populate the Treeview with data from the database
    def populate_treeview():
        # Clear the existing treeview entries
        for i in tree.get_children():
            tree.delete(i)
            
        try:
            conn = get_db_connection(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM legit_apk_info_table")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert('', 'end', values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            print(f"An error occurred: {e}")  # Print the error to the console as well

    # Add a refresh button to re-populate the Treeview with data
    refresh_button = tk.Button(db_window, text="Refresh", command=populate_treeview)
    refresh_button.pack(side='bottom', pady=10)

    # Initially populate the Treeview
    populate_treeview()

def create_gui(sio, monitor_dir, dest_dir, monitoring_flag):
    root = tk.Tk()
    root.title("Directory Monitoring")
    root.geometry("800x800")

    output_text = scrolledtext.ScrolledText(root, height=30, width=60)
    output_text.pack(padx=10, pady=10)

    # update_message(root, output_text_callback, "Hello World from socket emit!")
        
    def output_text_callback(message):
        output_text.insert(tk.END, message)
        output_text.see(tk.END)
        

    
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    start_button = tk.Button(button_frame, text="Start Monitoring", command=lambda: start_monitoring_thread(sio, monitor_dir, dest_dir, output_text_callback, monitoring_flag))
    start_button.pack(side=tk.LEFT, padx=10)

    check_button = tk.Button(button_frame, text="Check Now", command=lambda: perform_check(monitor_dir, dest_dir, output_text_callback))
    check_button.pack(side=tk.LEFT, padx=10)

    def stop_monitoring():
        monitoring_flag["active"] = False
        output_text_callback("Monitoring stopped...\n")

    stop_button = tk.Button(button_frame, text="Stop Monitoring", command=stop_monitoring)
    stop_button.pack(side=tk.LEFT, padx=10)

    def exit_app():
        try:
            if monitoring_flag["active"]:
                if messagebox.askyesno("Exit", "Monitoring is active. Are you sure you want to exit?"):
                    monitoring_flag["active"] = False
                    root.destroy()
                if sio.connected:
                    print("Disconnecting from socket...")
                    sio.disconnect()
        finally:
            root.destroy()

    exit_button = tk.Button(button_frame, text="Exit", command=exit_app)
    exit_button.pack(side=tk.RIGHT, padx=10)

    view_db_button = tk.Button(button_frame, text="View Database", command=open_database_view)
    view_db_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

    return root  # Return the root in case it needs to be accessed
