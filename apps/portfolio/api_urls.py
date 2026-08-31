from django.urls import path
from . import api_views

urlpatterns = [
    path('public/', api_views.public_albums, name='api_public_albums'),
    path('public/<int:pk>/', api_views.album_detail, name='api_album_detail'),
    path('my/', api_views.my_albums, name='api_my_albums'),
    path('my/<int:pk>/delete/', api_views.delete_album, name='api_delete_album'),
]