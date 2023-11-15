import sqlite3
import datetime

def get_db_connection(db_file='verified_apk_data.db'):
    conn = sqlite3.connect(db_file)
    conn.isolation_level = None  # Sets connection to auto-commit mode
    return conn

def create_legit_apk_info_table(conn):
    try:
        cursor = conn.cursor()
        
        cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS legit_apk_info_table
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    apk_hash TEXT,
                    version_code TEXT,
                    version_name TEXT,
                    app_cert_hash TEXT,
                    permissions TEXT,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (package_name) REFERENCES hash_checks_table(package_name)
                )
        """
        )
        print("Table legit_apk_info_table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")

def insert_into_legit_apk_info_table(conn, package_name, apk_hash="", version_code="", 
                                    version_name="", app_cert_hash="", permissions=""):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO legit_apk_info_table (package_name, apk_hash, version_code, 
                                             version_name, app_cert_hash, permissions, 
                                             createdAt, updatedAt)
            VALUES (?, ? ,?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (
                package_name,
                apk_hash,
                version_code,
                version_name,
                app_cert_hash,
                permissions
            )
        )
        print("Data inserted successfully into legit_apk_info_table.")
    except sqlite3.Error as e:
        print(f"An error occurred while inserting data: {e}")

def create_hash_checks_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS hash_checks_table
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT UNIQUE NOT NULL,
                    incoming_hash TEXT,
                    downloaded_hash TEXT,
                    incoming_app_cert_hash TEXT,
                    downloaded_app_cert_hash TEXT,
                    incoming_permissions TEXT,
                    downloaded_permissions TEXT,
                    result TEXT,
                    received_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checked_time TIMESTAMP
                )
        """
        )
        print("Table hash_checks_table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")
        
def insert_into_hash_checks_table(conn, package_name, incoming_hash="", downloaded_hash="", 
                            incoming_app_cert_hash="", downloaded_app_cert_hash="", 
                            incoming_permissions="", downloaded_permissions="", result=""):
    try:
        
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO hash_checks_table (package_name, incoming_hash, downloaded_hash, 
                                           incoming_app_cert_hash, downloaded_app_cert_hash, 
                                           incoming_permissions, downloaded_permissions, result, 
                                           received_time, checked_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, NULL)
            """,
            (
                package_name,
                incoming_hash,
                downloaded_hash,
                incoming_app_cert_hash,
                downloaded_app_cert_hash,
                incoming_permissions,
                downloaded_permissions,
                result
            )
        )
        print("Data inserted successfully into hash_checks_table.")
    except sqlite3.Error as e:
        print(f"An error occurred while inserting data: {e}")

def test_db_connection(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        result = cursor.fetchall()
        if result:
            for table in result:
                print(f"Connection verified, found table: {table}")
        else:
            print("Connection verified, no tables found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Usage
conn = get_db_connection()
create_legit_apk_info_table(conn)
create_hash_checks_table(conn)
test_db_connection(conn)
conn.close()
