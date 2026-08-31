from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, PhotographerProfileForm
from .models import PhotographerProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Si photographe → créer son profil automatiquement
            if user.role == 'photographer':
                PhotographerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Votre compte a été créé.")
            return redirect('dashboard')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Identifiants incorrects.")

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_view(request):
    if request.user.is_photographer():
        return redirect('photographer_dashboard')
    else:
        return redirect('client_dashboard')


@login_required
def photographer_dashboard(request):
    if not request.user.is_photographer():
        return redirect('client_dashboard')

    galleries = request.user.galleries.all()
    albums = request.user.albums.all()
    orders = request.user.received_orders.filter(status='pending')

    context = {
        'galleries': galleries,
        'albums': albums,
        'orders': orders,
        'total_galleries': galleries.count(),
        'total_albums': albums.count(),
        'pending_orders': orders.count(),
    }
    return render(request, 'accounts/photographer_dashboard.html', context)


@login_required
def client_dashboard(request):
    if not request.user.is_client():
        return redirect('photographer_dashboard')

    orders = request.user.orders.all()
    context = {'orders': orders}
    return render(request, 'accounts/client_dashboard.html', context)