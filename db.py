import sqlite3

def get_db_connection(db_file='verified_apk_data.db'):
    conn = sqlite3.connect(db_file)
    conn.isolation_level = None  # This sets the connection to auto-commit mode
    return conn

def create_legit_apk_info_table(conn):
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS legit_apk_info_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packageName TEXT NOT NULL,
                apkHash TEXT,
                versionCode TEXT,
                versionNumber TEXT,
                appCertHash TEXT,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (packageName) REFERENCES hash_checks(packageName)
            )
        """)
        print("Table legit_apk_info_table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")

def create_hash_checks_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS hash_checks_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packageName TEXT UNIQUE NOT NULL,
                incomingHash TEXT,
                downloadedHash TEXT, 
                result TEXT,
                receivedTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                checkedTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        )
        print("Table hash_checks_table created successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")
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

def insert_into_hash_checks_table(conn, package_name, incoming_hash, downloaded_hash, result):
    try:
        cursor = conn.cursor()
        # Prepare the insert statement
        insert_stmt = """
        INSERT INTO hash_checks_table (packageName, incomingHash, downloadedHash, result, receivedTime, checkedTime)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        # Execute the insert statement with the provided values
        cursor.execute(insert_stmt, (package_name, incoming_hash, downloaded_hash, result))
        # Commit the changes to the database
        conn.commit()
        print("Data inserted into hash_checks_table successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while inserting data into the table: {e}")

# Usage
conn = get_db_connection()
create_legit_apk_info_table(conn)
create_hash_checks_table(conn)

test_db_connection(conn)
conn.close()
