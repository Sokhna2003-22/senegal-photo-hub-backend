from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.order_list_create, name='api_order_list'),
    path('<int:pk>/', api_views.order_detail_update, name='api_order_detail'),
]