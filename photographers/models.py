from django.db import models
from PIL import Image


class Album(models.Model):
    title = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    album_cover = models.ImageField(upload_to='upload/album_covers/')


class CroppedFace(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload/cropped_faces/')
    face_locations = models.JSONField(null=True)
    face_embedding = models.JSONField(null=True)
