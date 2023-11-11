# Database Initialization for APK Verification System

This guide will walk you through the steps to create and initialize the database for the APK verification system.

## Step 1: Create the Tables

Before you can start using the database, you need to create the necessary tables where the data will be stored.

To create the tables, run the following script from the command line:


Run the `db.py` file. This script will set up the following tables in the `verified_apk_data.db` SQLite database:

- `hash_checks`: Stores the hash information for the APK files.
- `legit_apk_info_table`: Contains information about legitimate APK files, referencing the `hash_checks` table.

## Step 2: Initialize the Database

Once the tables are created, you need to populate them with initial data.

Run the `insert_mock_data.py` script only once to insert mock data into the database:


**Note:** Do not run this script multiple times as it will insert duplicate entries. It is only required to run once to initialize the database with mock data.

## Additional Information

- Ensure that Python and SQLite are properly installed on your system before running these scripts.
- The `db.py` script must be run before `insert_mock_data.py` to ensure the tables exist.
- If you encounter any errors, please check the console output for diagnostic information.
