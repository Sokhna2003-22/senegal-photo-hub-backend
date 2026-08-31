from django.urls import path
from . import views

urlpatterns = [
    # Photographe (privé)
    path('', views.album_list, name='album_list'),
    path('create/', views.album_create, name='album_create'),
    path('<int:pk>/', views.album_detail, name='album_detail'),
    path('<int:pk>/delete/', views.album_delete, name='album_delete'),
    path('photo/<int:pk>/delete/', views.portfolio_photo_delete, name='portfolio_photo_delete'),

    # Public
    path('photographe/<str:username>/', views.photographer_public_profile, name='photographer_profile'),
    path('album/<int:pk>/view/', views.album_public_view, name='album_public_view'),
]