from django.urls import path
from .views import match_selfies, register_selfie
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('match_selfies/<int:user_selfie_id>/', match_selfies, name='match_selfies'),
    path('', register_selfie, name='capture_selfies'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
