import sqlite3
from datetime import datetime

# Assuming db.py contains the get_db_connection function
from db import get_db_connection

def insert_mock_data_apk_info(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM legit_apk_info_table")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ('com.example.app1', 'hash1', 'code1', 'number1', 'certHash1'),
            ('com.example.app2', 'hash2', 'code2', 'number2', 'certHash2'),
            ('com.example.app3', 'hash3', 'code3', 'number3', 'certHash3'),
            ('com.example.app4', 'hash4', 'code4', 'number4', 'certHash4'),
            ('com.example.app5', 'hash5', 'code5', 'number5', 'certHash5')
        ]
        
        for data in mock_data:
            cursor.execute("""
                INSERT INTO legit_apk_info_table (packageName, apkHash, versionCode, versionNumber, appCertHash, createdAt, updatedAt)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data + (datetime.now(), datetime.now()))

    conn.commit()

def insert_mock_data_hash_checks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM hash_checks_table")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ('com.example.app1', 'incoming_hash1', 'downloaded_hash1', 'Result1'),
            ('com.example.app2', 'incoming_hash2', 'downloaded_hash2', 'Result2'),
            ('com.example.app3', 'incoming_hash3', 'downloaded_hash3', 'Result3'),
            ('com.example.app4', 'incoming_hash4', 'downloaded_hash4', 'Result4'),
            ('com.example.app5', 'incoming_hash5', 'downloaded_hash5', 'Result5')
        ]
        
        for data in mock_data:
            cursor.execute("""
                INSERT INTO hash_checks_table (packageName, incomingHash, downloadedHash, result, receivedTime, checkedTime)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data + (datetime.now(), datetime.now()))

    conn.commit()

def retrieve_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hash_checks_table")
    rows = cursor.fetchall()
    return rows

def main():
    db_file = 'verified_apk_data.db'
    conn = get_db_connection(db_file)
    
    # Insert mock data
    insert_mock_data_apk_info(conn)
    print("Mock data inserted into apk_info_table successfully.")
    
    insert_mock_data_hash_checks(conn)
    print("Mock data inserted into hash_checks_table successfully.")
    
    # Retrieve and print all rows
    rows = retrieve_data(conn)
    if rows:
        print("Retrieved rows:")
        for row in rows:
            print(row)
    else:
        print("No rows found in the database.")
    conn.close()

if __name__ == '__main__':
    main()