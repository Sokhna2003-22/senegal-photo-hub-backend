from django.urls import path
from . import api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', api_views.login_api, name='api_login'),
    path('me/', api_views.me_api, name='api_me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('photographers/', api_views.photographers_list, name='api_photographers'),
    path('photographers/<str:username>/', api_views.photographer_detail, name='api_photographer_detail'),
    path('admin/stats/', api_views.admin_stats, name='api_admin_stats'),
]