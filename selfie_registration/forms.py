from django import forms
from .models import UserSelfie


class UserSelfieForm(forms.ModelForm):
    class Meta:
        model = UserSelfie
        fields = ['user_name', 'mobile_number', 'selfie_image']
