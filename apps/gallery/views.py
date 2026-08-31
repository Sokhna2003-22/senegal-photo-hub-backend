from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
import os
from .models import ClientGallery, Photo
from .forms import ClientGalleryForm, GalleryAccessForm

# ── PHOTOGRAPHE ──────────────────────────────────────

@login_required
def gallery_list(request):
    """Liste des galeries du photographe"""
    if not request.user.is_photographer():
        return redirect('client_dashboard')
    galleries = request.user.galleries.all()
    return render(request, 'gallery/gallery_list.html', {'galleries': galleries})


@login_required
def gallery_create(request):
    """Créer une nouvelle galerie"""
    if not request.user.is_photographer():
        return redirect('client_dashboard')

    form = ClientGalleryForm()
    if request.method == 'POST':
        form = ClientGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.photographer = request.user
            gallery.save()
            messages.success(request, f'Galerie "{gallery.title}" créée ! Code d\'accès : {gallery.access_code}')
            return redirect('gallery_detail', pk=gallery.pk)

    return render(request, 'gallery/gallery_form.html', {'form': form, 'action': 'Créer'})


@login_required
def gallery_detail(request, pk):
    """Voir une galerie + uploader des photos"""
    gallery = get_object_or_404(ClientGallery, pk=pk, photographer=request.user)
    photos = gallery.photos.all()

    if request.method == 'POST':
        files = request.FILES.getlist('image')
        for f in files:
            Photo.objects.create(
                gallery=gallery,
                image=f,
                title=request.POST.get('title', ''),
                is_downloadable=request.POST.get('is_downloadable') == 'on'
            )
        messages.success(request, f'{len(files)} photo(s) ajoutée(s) avec succès !')
        return redirect('gallery_detail', pk=pk)

    return render(request, 'gallery/gallery_detail.html', {
        'gallery': gallery,
        'photos': photos,
    })


@login_required
def gallery_delete(request, pk):
    gallery = get_object_or_404(ClientGallery, pk=pk, photographer=request.user)
    if request.method == 'POST':
        gallery.delete()
        messages.success(request, 'Galerie supprimée.')
        return redirect('gallery_list')
    return render(request, 'gallery/gallery_confirm_delete.html', {'gallery': gallery})


@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk, gallery__photographer=request.user)
    gallery_pk = photo.gallery.pk
    photo.delete()
    messages.success(request, 'Photo supprimée.')
    return redirect('gallery_detail', pk=gallery_pk)


# ── CLIENT ───────────────────────────────────────────

def gallery_access(request):
    """Page d'accès avec code pour les clients"""
    form = GalleryAccessForm()
    if request.method == 'POST':
        form = GalleryAccessForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['access_code'].upper()
            try:
                gallery = ClientGallery.objects.get(access_code=code, is_active=True)
                # Stocker le code en session
                request.session[f'gallery_access_{gallery.pk}'] = True
                return redirect('gallery_client_view', pk=gallery.pk)
            except ClientGallery.DoesNotExist:
                messages.error(request, 'Code incorrect ou galerie introuvable.')

    return render(request, 'gallery/gallery_access.html', {'form': form})


def gallery_client_view(request, pk):
    """Vue client de la galerie"""
    gallery = get_object_or_404(ClientGallery, pk=pk, is_active=True)

    # Vérifier l'accès
    if not request.session.get(f'gallery_access_{gallery.pk}'):
        messages.warning(request, 'Veuillez entrer votre code d\'accès.')
        return redirect('gallery_access')

    photos = gallery.photos.all()
    return render(request, 'gallery/gallery_client_view.html', {
        'gallery': gallery,
        'photos': photos,
    })


def photo_download(request, pk):
    """Télécharger une photo"""
    photo = get_object_or_404(Photo, pk=pk, is_downloadable=True)
    gallery = photo.gallery

    if not request.session.get(f'gallery_access_{gallery.pk}'):
        raise Http404

    file_path = photo.image.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    raise Http404