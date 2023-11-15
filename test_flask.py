from flask import Flask, jsonify, request, abort
from hash_util import compute_sha256
import subprocess
import os
from db import get_db_connection
from hash_results import HashResult
from flask_socketio import SocketIO
from flask_cors import CORS 
from threading import Thread

conn = get_db_connection()
cursor = conn.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = '4FB3D994-8B97-4EA3-A492-FCAA51E88A4B'  # Replace with your secret key
CORS(app)
socketio = SocketIO(app)

@app.route("/")
def hello():
    socketio.emit('process_apk', {'message': 'Hello World from socket emit!'})
    return jsonify({"status": "success", "message": "Hello World!"})


@app.route('/submit_apk', methods=['POST'])
def submit_apk():
    data = request.json
    if not data:
        abort(400, description="No JSON data provided")
    
    package_name = data['package_name']
    incoming_apk_hash = data['incoming_apk_hash']
    incoming_app_cert_hash = data['incoming_app_cert_hash']
    incoming_permissions = data['incoming_permissions']
    result = HashResult.UNCHECKED

    if None in [package_name, incoming_apk_hash, incoming_app_cert_hash, incoming_permissions]:
        return jsonify({"error": "Missing required fields"}), 400  # Bad Request
    
    socketio.emit('process_apk', {
        'message': 'Hello World from socket emit!',
        'incoming_apk_info': {
        'package_name': package_name,
        'apk_hash': incoming_apk_hash,
        'app_cert_hash': incoming_app_cert_hash,
        'permissions': incoming_permissions
    }
    })

    return jsonify({"status": "success", "message": "information received successfully."}),200



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)