
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('conversation/<str:username>/', views.conversation, name='conversation'),
    path('new/<str:username>/', views.new_message, name='new_message'),
    path('api/<str:username>/', views.get_new_messages, name='get_new_messages'),
]