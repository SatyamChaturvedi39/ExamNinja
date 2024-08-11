import warnings
import cv2
import base64
import numpy as np
import pickle
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
socketio = SocketIO(app)

# Suppress specific FutureWarnings related to `rcond`
warnings.simplefilter(action='ignore', category=FutureWarning)

# Load custom embeddings from .pkl file
with open('embeddings.pkl', 'rb') as f:
    embeddings, names = pickle.load(f)
    print(f"Loaded embeddings shape: {embeddings.shape}")

# Initialize face analysis model
detector = FaceAnalysis(name='buffalo_l')  # Use the appropriate model pack
detector.prepare(ctx_id=-1)

def recognize_face(image_data):
    """Function to recognize face and return name and confidence."""
    np_array = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    faces = detector.get(img)
    
    if faces is not None and len(faces) > 0:
        for face in faces:
            face_embedding = face.normed_embedding
            
            if face_embedding.ndim == 1:  # Reshape if necessary
                face_embedding = face_embedding.reshape(1, -1)
                
            # Compare with custom embeddings
            similarities = cosine_similarity(face_embedding, embeddings)
            max_similarity_index = np.argmax(similarities)
            confidence = similarities[0][max_similarity_index]
            name = names[max_similarity_index]

            return {'name': name, 'confidence': f'{confidence:.2f}'}
    
    return {'name': None, 'confidence': None}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(data):
    if data:  # Ensure data is received
        result = recognize_face(data)
        emit('response', result)
    else:
        emit('response', {'error': 'No image data received'})

@app.route('/recognize', methods=['POST'])
def recognize():
    image_data = request.json.get('image_data')
    if image_data:
        result = recognize_face(image_data)
        return jsonify(result)
    return jsonify({'error': 'No image data provided'}), 400

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
