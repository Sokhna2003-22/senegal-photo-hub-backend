from django.urls import path
from . import views

urlpatterns = [
    # Photographe
    path('', views.gallery_list, name='gallery_list'),
    path('create/', views.gallery_create, name='gallery_create'),
    path('<int:pk>/', views.gallery_detail, name='gallery_detail'),
    path('<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
    path('photo/<int:pk>/delete/', views.photo_delete, name='photo_delete'),

    # Client
    path('access/', views.gallery_access, name='gallery_access'),
    path('view/<int:pk>/', views.gallery_client_view, name='gallery_client_view'),
    path('photo/<int:pk>/download/', views.photo_download, name='photo_download'),
]