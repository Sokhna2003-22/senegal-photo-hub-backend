from django.shortcuts import render
from apps.accounts.models import User
from apps.portfolio.models import PortfolioAlbum


def home_view(request):
    # Les photographes avec un profil vérifié ou actif
    photographers = User.objects.filter(
        role='photographer'
    ).select_related('photographer_profile')[:6]

    # Les derniers albums publics
    recent_albums = PortfolioAlbum.objects.filter(
        is_public=True
    ).select_related('photographer')[:8]

    return render(request, 'public/home.html', {
        'photographers': photographers,
        'recent_albums': recent_albums,
    })