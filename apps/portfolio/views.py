from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PortfolioAlbum, PortfolioPhoto
from .forms import PortfolioAlbumForm
from apps.accounts.models import User


# ── PHOTOGRAPHE (privé) ──────────────────────────────

@login_required
def album_list(request):
    """Liste des albums du photographe connecté"""
    if not request.user.is_photographer():
        return redirect('client_dashboard')
    albums = request.user.albums.all()
    return render(request, 'portfolio/album_list.html', {'albums': albums})


@login_required
def album_create(request):
    if not request.user.is_photographer():
        return redirect('client_dashboard')

    form = PortfolioAlbumForm()
    if request.method == 'POST':
        form = PortfolioAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.photographer = request.user
            album.save()

            # Upload des photos de l'album
            files = request.FILES.getlist('photos')
            for f in files:
                PortfolioPhoto.objects.create(album=album, image=f)

            messages.success(request, f'Album "{album.title}" créé avec succès !')
            return redirect('album_detail', pk=album.pk)

    return render(request, 'portfolio/album_form.html', {'form': form, 'action': 'Créer'})


@login_required
def album_detail(request, pk):
    album = get_object_or_404(PortfolioAlbum, pk=pk, photographer=request.user)
    photos = album.photos.all()

    if request.method == 'POST':
        files = request.FILES.getlist('photos')
        for f in files:
            PortfolioPhoto.objects.create(album=album, image=f)
        messages.success(request, f'{len(files)} photo(s) ajoutée(s) !')
        return redirect('album_detail', pk=pk)

    return render(request, 'portfolio/album_detail.html', {
        'album': album,
        'photos': photos,
    })


@login_required
def album_delete(request, pk):
    album = get_object_or_404(PortfolioAlbum, pk=pk, photographer=request.user)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Album supprimé.')
        return redirect('album_list')
    return render(request, 'portfolio/album_confirm_delete.html', {'album': album})


@login_required
def portfolio_photo_delete(request, pk):
    photo = get_object_or_404(PortfolioPhoto, pk=pk, album__photographer=request.user)
    album_pk = photo.album.pk
    photo.delete()
    messages.success(request, 'Photo supprimée.')
    return redirect('album_detail', pk=album_pk)


# ── PUBLIC ───────────────────────────────────────────

def photographer_public_profile(request, username):
    """Page publique d'un photographe"""
    photographer = get_object_or_404(User, username=username, role='photographer')
    albums = photographer.albums.filter(is_public=True)
    return render(request, 'portfolio/photographer_profile.html', {
        'photographer': photographer,
        'albums': albums,
    })


def album_public_view(request, pk):
    """Vue publique d'un album"""
    album = get_object_or_404(PortfolioAlbum, pk=pk, is_public=True)
    photos = album.photos.all()
    return render(request, 'portfolio/album_public_view.html', {
        'album': album,
        'photos': photos,
    })