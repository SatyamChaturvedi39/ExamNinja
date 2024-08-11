from flask import Blueprint, request, jsonify
import numpy as np
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import cv2
import base64

recognition = Blueprint('recognition', __name__)

# Load custom embeddings from .pkl file
with open('website/embeddings.pkl', 'rb') as f:
    embeddings, names = pickle.load(f)
    print(f"Loaded embeddings shape: {embeddings.shape}")

# Initialize face analysis model
detector = FaceAnalysis(name='buffalo_s')  # Use the appropriate model pack
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

@recognition.route('/recognize', methods=['POST'])
def recognize():
    image_data = request.json.get('image_data')
    if image_data:
        result = recognize_face(image_data)
        return jsonify(result)
    return jsonify({'error': 'No image data provided'}), 400
