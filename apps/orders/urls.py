from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:username>/', views.order_create, name='order_create'),
    path('photographer/', views.order_list_photographer, name='order_list_photographer'),
    path('client/', views.order_list_client, name='order_list_client'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
]