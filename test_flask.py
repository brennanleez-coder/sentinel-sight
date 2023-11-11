from flask import Flask, jsonify, request
from hash_util import compute_sha256
import subprocess
import os
from db import get_db_connection
from hash_results import HashResult

conn = get_db_connection()
cursor = conn.cursor()

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"


@app.route('/submit_apk', methods=['POST'])
def submit_apk():
    data = request.json
    apk_hash = data['apkHash']
    package_name = data['packageName']
    # Store the hash and package name in the queue/database and notify the admin
    update_stmt = """
        UPDATE hash_checks_table
        SET result = ?, checkedTime = CURRENT_TIMESTAMP
        WHERE packageName = ?
        """
    # Execute the update statement with the new result and the package name
    cursor.execute(update_stmt, (HashResult['UNCHECKED'], package_name))
        
    return jsonify({"status": "success", "message": "Hash and package name received."})

@app.route('/get-apk-info', methods=['POST'])
def get_apk_info():
    # Save the uploaded file
    apk_file = request.files['file']
    apk_file_path = 'temp.apk'
    apk_file.save(apk_file_path)

    # Run aapt to get the version info
    result = subprocess.run(["aapt", "dump", "badging", apk_file_path], stdout=subprocess.PIPE)

    # Delete the APK file after analysis
    os.remove(apk_file_path)

    # Parse the result
    output = result.stdout.decode()
    version_code = extract_version_code(output)
    version_name = extract_version_name(output)

    # Return the info as JSON
    return jsonify({
        'version_code': version_code,
        'version_name': version_name
    })


if __name__ == "__main__":
  app.run()
