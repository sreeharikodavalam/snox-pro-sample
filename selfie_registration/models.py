from django.db import models


class UserSelfie(models.Model):
    user_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    selfie_image = models.ImageField(upload_to='user_selfies')
    selfie_embedding = models.TextField(default=None, blank=True, null=True)
