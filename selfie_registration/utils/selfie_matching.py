import face_recognition_models
import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO


def match_photos(selfie_path, threshold=0.4):
    try:
        # Load the known selfie (replace 'path/to/known/selfie.jpg' with the actual path)
        known_image = face_recognition.load_image_file(selfie_path)
        known_encoding = face_recognition.face_encodings(known_image)[0]

        # Load the user selfie
        user_image = face_recognition.load_image_file(selfie_path)
        user_encoding = face_recognition.face_encodings(user_image)[0]

        # Compare faces
        result = face_recognition.compare_faces([known_encoding], user_encoding, tolerance=threshold)

        return result[0]

    except Exception as e:
        return f'Error in photo matching: {str(e)}'


def match_face_encodings(known_encoding, comparing_encoding, threshold=0.4):
    result = face_recognition.compare_faces(known_encoding, comparing_encoding, tolerance=threshold)

    return result[0]


def get_face_embedding(image_bytes):
    try:
        # Use BytesIO to create a file-like object from the binary data
        image_file = BytesIO(image_bytes)

        # Open the image using Pillow
        pil_image = Image.open(image_file)

        # Convert the image to RGB if it's not in that mode
        pil_image = pil_image.convert("RGB")

        # Get face encodings using face_recognition
        face_encodings = face_recognition.face_encodings(np.array(pil_image))

        if face_encodings:
            # Convert the face encoding to a list for storage in the database
            return face_encodings[0].tolist()

    except Exception as e:
        # Log or return a more descriptive error message
        print(f"An error occurred: {e}")

    return None
