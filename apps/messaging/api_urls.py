from django.urls import path
from . import api_views

urlpatterns = [
    path('inbox/', api_views.inbox, name='api_inbox'),
    path('conversation/<str:username>/', api_views.conversation,
         name='api_conversation'),
]