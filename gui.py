import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import threading
import time
from file_operations import perform_check, save_scrolledtext_to_file, get_timestamp
from db import get_db_connection, get_all_legit_apk_info, get_all_hash_checks
import sqlite3
from socket_client import connect_to_server, process_apk
db_queue_manager = None
log_text = None
apk_info = None

def get_apk_info(apk_info_retrieved):
    global apk_info
    apk_info = apk_info_retrieved



def start_monitoring_thread(sio, monitor_dir, dest_dir, output_text_callback, monitoring_flag):
    if not monitoring_flag["active"]:
        monitoring_flag["active"] = True
        output_text_callback("Monitoring started...\n")
        
        try:
            connect_to_server('http://localhost:8000', sio, output_text_callback, monitoring_flag)
            output_text_callback("Socket open...\n")
        except Exception as e:
            print(e)
            output_text_callback(f"Error occured when connecting web socket: {e}")

        monitor_thread = threading.Thread(target=monitor_directory, args=(monitor_dir, dest_dir, output_text_callback, monitoring_flag))
        monitor_thread.daemon = True
        monitor_thread.start()

def monitor_directory(monitor_dir, dest_dir, output_text_callback, monitoring_flag):
    output_text_callback("Listener triggered...\n")
    while monitoring_flag["active"]:
        perform_check(monitor_dir, dest_dir, output_text_callback)
        time.sleep(60)  # Check every minute

def open_database_view(db_file='verified_apk_data.db'):
    db_window = tk.Toplevel()
    db_window.title("Verified Apk Viewer")
    db_window.geometry("800x800")
    

    # Create a frame for the Treeview and the scrollbars
    tree_frame = tk.Frame(db_window)
    tree_frame.pack(fill='both', expand=True)

    columns = ("ID", "Package Name", "APK Hash", "Version Code", "Version Number", "Cert Hash", "Permissions", "Created At", "Updated At")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    v_scroll.pack(side='right', fill='y')

    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    h_scroll.pack(side='bottom', fill='x')

    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    tree.pack(fill='both', expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='w')

    def populate_treeview():
        for i in tree.get_children():
            tree.delete(i)
            
        try:
            conn = get_db_connection(db_file)
            rows = get_all_legit_apk_info(conn)
            for row in rows:
                tree.insert('', 'end', values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            print(f"An error occurred: {e}")  # Print the error to the console as well

    # Add a refresh button to re-populate the Treeview with data
    refresh_button = tk.Button(db_window, text="Refresh", command=populate_treeview)
    refresh_button.pack(side='bottom', pady=10)

    populate_treeview()

def create_gui(sio, db_queue, monitor_dir, dest_dir, monitoring_flag):
    global log_text
    root = tk.Tk()
    root.title("Sentinel-Sight")
    root.geometry("800x800")

    db_queue_manager = db_queue

    output_text = scrolledtext.ScrolledText(root, height=40, width=60)
    output_text.pack(padx=10, pady=10)
    log_text = output_text
        
    def output_text_callback(message):
        output_text.insert(tk.END, message)
        output_text.see(tk.END)
        

    
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    start_button = tk.Button(button_frame, text="Start Monitoring", command=lambda: start_monitoring_thread(sio, monitor_dir, dest_dir, output_text_callback, monitoring_flag))
    start_button.pack(side=tk.LEFT, padx=10)

    check_button = tk.Button(button_frame, text="Check Now", command=lambda: perform_check(monitor_dir, dest_dir, output_text_callback))
    check_button.pack(side=tk.LEFT, padx=10)

    evaluate_button = tk.Button(button_frame, text="Evaluate Now", command=lambda: process_apk(apk_info))
    evaluate_button.pack(side=tk.LEFT, padx=10)

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

            if db_queue_manager is not None:
                db_queue_manager.stop_db_worker()             
        finally:
            db_queue_manager.stop_db_worker()  # Stop the DB worker
            if sio.connected:
                sio.disconnect()
            save_scrolledtext_to_file(log_text, f"{get_timestamp()} - logs", tk)

            root.destroy()

    exit_button = tk.Button(button_frame, text="Exit", command=exit_app)
    exit_button.pack(side=tk.RIGHT, padx=10)

    view_db_button = tk.Button(button_frame, text="View Legit Apk Info", command=open_database_view)
    view_db_button.pack(side=tk.LEFT, padx=10)

    def view_hash_checks():
        hash_checks_window = tk.Toplevel()
        hash_checks_window.title("Hash Checks Table")
        hash_checks_window.geometry("800x800")

        # Create a frame for the Treeview and the scrollbars
        tree_frame = tk.Frame(hash_checks_window)
        tree_frame.pack(fill='both', expand=True)

        columns = ("ID", "package_name", "version_code", "version_name", "incoming_hash", "downloaded_hash", "incoming_app_cert_hash", "downloaded_app_cert_hash", "incoming_permissions", "downloaded_permissions", "result", "received_time", "checked_time")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        v_scroll.pack(side='right', fill='y')

        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        h_scroll.pack(side='bottom', fill='x')

        tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        tree.pack(fill='both', expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='w')

        def populate_treeview():
            for i in tree.get_children():
                tree.delete(i)
                
            try:
                conn = get_db_connection()
                rows = get_all_hash_checks(conn)
                for row in rows:
                    tree.insert('', 'end', values=row)
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
                print(f"An error occurred: {e}")
        populate_treeview()
        refresh_button = tk.Button(hash_checks_window, text="Refresh", command=populate_treeview)
        refresh_button.pack(side='bottom', pady=10)

    view_hash_checks_button = tk.Button(root, text="View Hash Checks", command=view_hash_checks)
    # place the button beside the view database button
    view_hash_checks_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

    return root  # Return the root in case it needs to be accessed
