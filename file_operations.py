import os
import shutil
from datetime import datetime
from directory import directory_of_local_apks, directory_of_tools
from extract_info_from_apk import extract_info
from db import get_all_legit_apk_info, get_db_connection, insert_into_legit_apk_info_table
import webbrowser
from fpdf import FPDF

def get_timestamp():
    return datetime.now().strftime("%Y_%m_%d %H_%M_%S")

# Perform check on downloaded apks
# @params: monitor_dir: directory to monitor for downloaded apks
# @params: dest_dir: directory to move downloaded apks to
# @params: output_text: function to output text to GUI

def perform_check(monitor_dir, dest_dir, output_text):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    apk_files = [f for f in os.listdir(monitor_dir) if f.endswith('.apk')]
    if not apk_files:
        output_text(f"{get_timestamp()} - No files to move.\n")
    else:
        for file in apk_files:
            source_file = os.path.join(monitor_dir, file)
            destination_file = os.path.join(dest_dir, file)
            shutil.move(source_file, destination_file)
            output_text(f"{get_timestamp()} - Moved file: {file}\n")
            
    output_text(f"{get_timestamp()} - Processing downloaded apks...\n")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    for filename in os.listdir(dest_dir):
        if filename.endswith(".apk"):
            apk_path = os.path.join(dest_dir, filename)
            info = extract_info(directory_of_tools, apk_path)
            app_hash, version_code, version_name, package_name, app_cert_hash, permissions = \
            info['app_hash'], info['version_code'], info['version_name'], info['package_name'], info['app_cert_hash'], info['permissions']
            is_package_present = cursor.execute("SELECT package_name FROM legit_apk_info_table WHERE package_name = ? AND version_code = ?", (package_name, version_code))
            if is_package_present.fetchone() is None:
                insert_into_legit_apk_info_table(conn, package_name, app_hash, version_code, version_name, app_cert_hash, permissions)
                output_text(f"{get_timestamp()} - Inserted {package_name}: version code: {info['version_code']} into legit_apk_info_table.\n")
            else:
                print(f"Package {package_name}: version code: {info['version_code']} already exists in legit_apk_info_table.")
    output_text(f"{get_timestamp()} - legit_apk_info table is up to date.\n")
    output_text(f"{get_timestamp()} ===================================== \n")



# PDF class for generating PDF reports
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        # Calculate width of title and position
        title_w = self.get_string_width('Sentinel-sight Report') + 6
        self.set_x((210 - title_w) / 2)  # 210 mm is approximately the width of an A4 page
        # Title
        self.cell(title_w, 10, 'Sentinel-sight Report', 0, 1, 'C')
        # Subtitle with timestamp
        self.set_font('Arial', 'I', 12)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subtitle_w = self.get_string_width(f'Generated as of {timestamp}') + 6
        self.set_x((210 - subtitle_w) / 2)  # Center subtitle
        self.cell(subtitle_w, 10, f'Generated as of {timestamp}', 0, 0, 'C')
        # Line break
        self.ln(20)
        # Logo
        self.image('./assets/Sentinel_Sight.png', 170, 10, 30)  # Position the logo at x = 170, y = 10 with a width of 30 mm

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

# Extract logs from GUI
# @params: output_text: function to output text to GUI
# @params: filename, name of file to save to desktop
# @params: tk, tkinter object
def save_scrolledtext_to_file(output_text_widget, filename, tk):
    # Retrieve the entire text from the ScrolledText widget
    full_text = output_text_widget.get("1.0", tk.END)
    if full_text == '\n':
        print("No logs to save.")
        return

    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    # Create a directory called Sentinel Sight Reports
    if not os.path.exists(os.path.join(desktop_path, 'Sentinel Sight Reports')):
        os.makedirs(os.path.join(desktop_path, 'Sentinel Sight Reports'))
    report_dir = os.path.join(desktop_path, 'Sentinel Sight Reports')
    file_path = os.path.join(report_dir, filename)

    # Create a PDF document
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    # Add subheader
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, 'Log Extracted', 0, 1)
    pdf.ln(10)  # Add a line break

    # Reset font for the content
    pdf.set_font("Times", size=12)

    # Add the text to the PDF
    for line in full_text.split('\n'):
        pdf.multi_cell(0, 10, txt=line)

    pdf.output(file_path)

    print(f"PDF file saved to {file_path}")

    webbrowser.open_new(file_path)