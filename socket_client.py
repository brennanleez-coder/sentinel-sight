import socketio

sio = socketio.Client()

#global variable to store the callback function
gui_output_text_callback = None 

def start_socket():
    return sio

@sio.event
def message(data):
    print('I received a message!')

def connect_to_server(server, sio, output_callback_from_gui):
    global gui_output_text_callback
    gui_output_text_callback = output_callback_from_gui
    
    try:
        sio.connect(server)
    except Exception as e:
        print(f"Error connecting to server: {e}")

    
@sio.on('test')
def update_message(data):
    if gui_output_text_callback is not None:
        gui_output_text_callback(data['message'] + '\n')
    

    
def start_socketio_thread():
    sio.connect('http://localhost:8000')
    sio.wait()
    
if __name__ == '__main__':
    sio.connect('http://localhost:8000')  # Match the Flask server's address
    sio.wait()
