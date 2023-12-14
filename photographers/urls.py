from django.urls import path
from .views import upload_album, upload_album_multiple,upload_album_multiple_ajax
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', upload_album, name='upload_album'),
    path('upload_multi/', upload_album_multiple, name='upload_album'),
    path('upload_multi_ajax/', upload_album_multiple_ajax, name='upload_album'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
