from website import create_app
from flask_socketio import SocketIO, emit
from website.recognition import recognize_face
import logging

logging.basicConfig(level=logging.DEBUG)


app = create_app()
socketio = SocketIO(app)

@socketio.on('video_frame')
def handle_video_frame(data):
    if data:  # Ensure data is received
        result = recognize_face(data)
        emit('response', result)
    else:
        emit('response', {'error': 'No image data received'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5100, debug=True)
