from flask import Flask, jsonify, request, abort
from db import get_db_connection
from hash_results import HashResult
from flask_socketio import SocketIO
from flask_cors import CORS 

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

@app.route("/", methods=['POST'])
def hello_post():
    data = request.json
    if not data:
        abort(400, description="No JSON data provided")
    return jsonify({"status": "success", "message": f"data received: {data}"}), 200

@app.route('/submit_apk', methods=['POST'])
def submit_apk():
    data = request.json
    if not data:
        abort(400, description="No JSON data provided")
    
    print(data)
    package_name = data['package_name']
    incoming_apk_hash = data['incoming_apk_hash']
    incoming_app_cert_hash = data['incoming_app_cert_hash']
    incoming_permissions = data['incoming_permissions']
    result = HashResult.UNCHECKED

    if None in [package_name, incoming_apk_hash, incoming_app_cert_hash, incoming_permissions]:
        return jsonify({"error": "Missing required fields"}), 400  # Bad Request
    
    socketio.emit('process_apk', {
        'incoming_apk_info': {
        'package_name': package_name,
        'apk_hash': incoming_apk_hash,
        'app_cert_hash': incoming_app_cert_hash,
        'permissions': incoming_permissions
    }
    })

    return jsonify({"status": "success", "message": "information received successfully."}),200

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    print(request.environ)
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return jsonify({"status": "success", "message": "Server shutting down..."}), 200

def run_flask():
    socketio.run(app, host='0.0.0.0', port=8000)
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)