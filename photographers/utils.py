# photographers/utils.py
import os
import face_recognition
from PIL import Image
from .models import CroppedFace
from snox_pro import settings
import numpy as np


def detect_and_crop_faces(album_image, padding=10):
    # Path to the uploaded album image
    image_path = album_image.album_cover.path

    # Load the image using face_recognition library
    image = face_recognition.load_image_file(image_path)

    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)

    # Create a directory to store cropped faces
    cropped_faces_dir = os.path.join(settings.MEDIA_ROOT, 'cropped_faces')
    os.makedirs(cropped_faces_dir, exist_ok=True)

    # Loop through each face and crop it
    for i, (top, right, bottom, left) in enumerate(face_locations):
        # Add padding to the face location
        top = max(0, top + padding)
        right = min(image.shape[1], right + padding)
        bottom = min(image.shape[0], bottom + padding)
        left = max(0, left + padding)

        # Crop the face with padding
        face_image = Image.fromarray(image[top:bottom, left:right])
        face_image_path = os.path.join(cropped_faces_dir, f'album_{album_image.pk}_face_{i + 1}.jpg')
        face_image.save(face_image_path)

        # Calculate face embedding using face_recognition
        face_encoding = face_recognition.face_encodings(image, known_face_locations=[(top, right, bottom, left)])[0]
        face_embedding = ",".join(map(str, face_encoding))

        # Save cropped face and its embedding in the database
        CroppedFace.objects.create(album_id=album_image.pk, image=face_image_path, face_embedding=face_embedding)

    return True


def calculate_similarity(uploaded_embedding, stored_embeddings):
    print(uploaded_embedding)
    # Calculate Euclidean distance for each stored embedding
    distances = np.linalg.norm(stored_embeddings - uploaded_embedding, axis=1)

    # Find the index of the closest match
    closest_match_index = np.argmin(distances)

    # Calculate similarity score (inverse of distance)
    similarity_score = 1 / (1 + distances[closest_match_index])

    return similarity_score


def match_faces(face_embedding):
    if face_embedding is None:
        print("No face detected")
    else:
        face_embedding = ",".join(map(str, face_embedding))

        # Fetch stored face data from the database
        stored_faces = CroppedFace.objects.all()
        print(face_embedding)

    # Initialize lists to store matches and their similarity scores
    matches = []
    similarity_threshold = 0.8  # Set your desired threshold

    # Compare the uploaded face embedding with each stored face location
    for stored_face in stored_faces:
        similarity_score = calculate_similarity(face_embedding, face_embedding)

        # Check if the similarity score exceeds the threshold
        if similarity_score > similarity_threshold:
            matches.append({
                'stored_face': stored_face,
                'similarity_score': similarity_score,
                'album_id': stored_face.album_id
            })

