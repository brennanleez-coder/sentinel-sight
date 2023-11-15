from hash_util import compute_sha256
from datetime import datetime
from extract_info_from_apk import extract_info
import os
from db import get_db_connection, insert_into_legit_apk_info_table
import sqlite3

# macbook setup
# directory_of_local_apks = '/Users/brennanlee/Desktop/extractedApks/'
# directory_of_tools = '/Users/brennanlee/library/Android/sdk/build-tools/33.0.1/'

# windows setup
directory_of_tools = "C:\\Users\\Cyber\\AppData\\Local\\Android\\Sdk\\build-tools\\33.0.1"
directory_of_local_apks = "C:\\Users\\Cyber\\Desktop\\extractedApks"

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

def insert_data_from_local_apk_directory(conn, directory_of_local_apks):
    cursor = conn.cursor()
    try:
        for filename in os.listdir(directory_of_local_apks):
            if filename.endswith(".apk"):
                apk_path = os.path.join(directory_of_local_apks, filename)
                info = extract_info(directory_of_tools, apk_path)

                # Extracting values
                version_code, version_name, package_name, app_cert_hash, permissions = \
                info['version_code'], info['version_name'], info['package_name'], info['app_cert_hash'], info['permissions']

                apk_hash = compute_sha256(apk_path)

                data = (package_name, apk_hash, version_code, version_name, app_cert_hash, permissions, datetime.now(), datetime.now())

                # cursor.execute("""
                #     INSERT INTO legit_apk_info_table (package_name, apk_hash, version_code, version_name, app_cert_hash, permissions, createdAt, updatedAt)
                #     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                # """, data)
                
                insert_into_legit_apk_info_table(conn, package_name, apk_hash, version_code, version_name, app_cert_hash, permissions)
                print("Live apk data inserted successfully into legit_apk_info_table.")

                
    except sqlite3.Error as e:
            print(f"An error occurred while inserting live apk data: {e}")

    


def insert_mock_data_hash_checks(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM hash_checks_table")
        
        if cursor.fetchone()[0] == 0:  # Check if the table is empty
            mock_data = [
            ('com.example.app1', 'incoming_hash1', 'downloaded_hash1', 'cert_hash1', 'cert_hash1', 'permission1,permission2', 'permission1,permission2', 'Result1'),
            ('com.example.app2', 'incoming_hash2', 'downloaded_hash2', 'cert_hash2', 'cert_hash2', 'permission3,permission4', 'permission3,permission4', 'Result2'),
            ('com.example.app3', 'incoming_hash3', 'downloaded_hash3', 'cert_hash3', 'cert_hash3', 'permission5,permission6', 'permission5,permission6', 'Result3'),
            ('com.example.app4', 'incoming_hash4', 'downloaded_hash4', 'cert_hash4', 'cert_hash4', 'permission7,permission8', 'permission7,permission8', 'Result4'),
            ('com.example.app5', 'incoming_hash5', 'downloaded_hash5', 'cert_hash5', 'cert_hash5', 'permission9,permission10', 'permission9,permission10', 'Result5')
        ]


            for data in mock_data:
                cursor.execute("""
                    INSERT INTO hash_checks_table 
                        (package_name, incoming_hash, downloaded_hash, incoming_app_cert_hash, downloaded_app_cert_hash, incoming_permissions, downloaded_permissions, result, received_time, checked_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data + (datetime.now(), datetime.now()))

            conn.commit()  # Commit the transaction
            print("Mock data inserted successfully into hash_checks_table.")

    except sqlite3.Error as e:
        print(f"An error occurred while inserting mock data: {e}")


def retrieve_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM legit_apk_info_table")
    rows = cursor.fetchall()
    return rows

def main():
    db_file = 'verified_apk_data.db'
    conn = get_db_connection(db_file)
    
    # Insert mock data
    # insert_mock_data_apk_info(conn)
    # print("Mock data inserted into apk_info_table successfully.")
    
    # Insert live apk data from local directory
    insert_data_from_local_apk_directory(conn, directory_of_local_apks)
    insert_mock_data_hash_checks(conn)
    
    # Retrieve and print all rows
    # rows = retrieve_data(conn)
    # if rows:
    #     print("Retrieved rows:")
    #     for row in rows:
    #         print(row)
    # else:
    #     print("No rows found in the database.")
    
    conn.close()

if __name__ == '__main__':
    main()