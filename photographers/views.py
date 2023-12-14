from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from .forms import AlbumForm, FileFieldForm
from .utils import detect_and_crop_faces
from PIL import Image
from io import BytesIO
import os
import uuid


def upload_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save()
            detect_and_crop_faces(album)
            return render(request, 'photographers/success_message.html', {'success_message': 'Uploaded'})
    else:
        form = AlbumForm()

    return render(request, 'photographers/upload_album.html', {'form': form})


def upload_album_multiple(request):
    return render(request, 'photographers/upload_multiple_album.html')


@csrf_exempt
def upload_album_multiple_ajax(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')

        if not files:
            return JsonResponse({'error': 'No files provided'})

        # Set the maximum resolution you want for the image
        max_width = 2000
        max_height = 2000

        uploaded_files = []

        for file_data in files:
            # Open the image using Pillow
            img = Image.open(file_data)

            # Check if resizing is needed
            if img.width > max_width or img.height > max_height:
                # Resize the image
                img.thumbnail((max_width, max_height), Image.ANTIALIAS)

                # Create an in-memory buffer to store the resized image
                resized_buffer = BytesIO()
                img.save(resized_buffer, format='JPEG')  # Save as JPEG, you can choose another format

                # Generate a unique filename
                unique_filename = str(uuid.uuid4()) + '_' + file_data.name
                resized_filepath = os.path.join('upload', 'albums', unique_filename)

                with open(resized_filepath, 'wb') as resized_file:
                    resized_file.write(resized_buffer.getvalue())

                uploaded_files.append(resized_filepath)
            else:
                # Generate a unique filename
                unique_filename = str(uuid.uuid4()) + '_' + file_data.name
                original_filepath = os.path.join('upload', 'albums', unique_filename)

                with open(original_filepath, 'wb') as original_file:
                    for chunk in file_data.chunks():
                        original_file.write(chunk)

                uploaded_files.append(original_filepath)

        return JsonResponse({'message': 'Files uploaded successfully!', 'filenames': uploaded_files})
    else:
        return JsonResponse({'error': 'Invalid request method'})