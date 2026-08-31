from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.gallery_list_create, name='api_gallery_list'),
    path('<int:pk>/', api_views.gallery_detail_delete, name='api_gallery_detail'),
    path('access/', api_views.gallery_access, name='api_gallery_access'),
    path('<int:pk>/upload/', api_views.upload_photos, name='api_upload_photos'),
]