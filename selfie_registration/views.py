import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse

from photographers.models import CroppedFace, Album
from photographers.utils import calculate_similarity
from .models import UserSelfie
from .forms import UserSelfieForm
from .utils.selfie_matching import match_photos, get_face_embedding, match_face_encodings


def parse_face_encodings(string_value):
    try:
        known_face_encoding_str = string_value
        known_face_encoding_list = [float(x) for x in known_face_encoding_str.split(',')]
        return np.array(known_face_encoding_list).reshape(1, -1)
    except Exception as e:
        print("f'An error occurred: {str(e)}'")
        return None


def match_selfies(request, user_selfie_id):
    # try:

    user_selfie = UserSelfie.objects.get(pk=user_selfie_id)
    known_face_encoding_np = parse_face_encodings(user_selfie.selfie_embedding)

    # For testing, comparing with itself
    matching_result = match_face_encodings(known_face_encoding_np, known_face_encoding_np)
    print(matching_result)

    result = []
    coped_faces = CroppedFace.objects.all()
    for face in coped_faces:
        face_embeddings = parse_face_encodings(face.face_embedding)
        match_result = match_face_encodings(known_face_encoding_np, face_embeddings)
        result.append({
            'match_result': match_result,
            'album_id': face.album.id,
            'cropped_face': face.image,
        })
    return render(request, 'selfie_registration/match_result.html', {'results': result, 'image': user_selfie.selfie_image.url, 'sample': 'sample_data-'})


#
# except UserSelfie.DoesNotExist:
#     return JsonResponse({'error': 'User selfie not found'}, status=404)
# except Exception as e:
#     return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def register_selfie(request):
    if request.method == 'POST':
        form = UserSelfieForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)

            # Get face embedding from the image
            face_embedding = get_face_embedding(request.FILES['selfie_image'].read())

            if face_embedding:
                # Convert the face embedding to a string for storage in the database
                user_profile.selfie_embedding = ",".join(map(str, face_embedding))
                user_profile.save()
                return JsonResponse({'message': 'Selfie registered successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Face not found or error in processing'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = UserSelfieForm()
        return render(request, 'selfie_registration/register_selfie.html', {'form': form})
