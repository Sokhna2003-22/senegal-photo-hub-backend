from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm, OrderStatusForm
from apps.accounts.models import User


def order_create(request, username):
    """Réserver un photographe"""
    photographer = get_object_or_404(User, username=username, role='photographer')

    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.photographer = photographer
            # Si l'utilisateur est connecté, on le met comme client
            if request.user.is_authenticated:
                order.client = request.user
            else:
                messages.warning(request, 'Connectez-vous pour passer une commande.')
                return redirect('login')
            order.save()
            messages.success(request, 'Votre réservation a été envoyée au photographe !')
            return redirect('client_dashboard')

    return render(request, 'orders/order_create.html', {
        'form': form,
        'photographer': photographer,
    })


@login_required
def order_list_photographer(request):
    """Liste des commandes reçues par le photographe"""
    if not request.user.is_photographer():
        return redirect('client_dashboard')

    orders = request.user.received_orders.all()
    pending = orders.filter(status='pending')
    confirmed = orders.filter(status='confirmed')
    completed = orders.filter(status='completed')

    return render(request, 'orders/order_list_photographer.html', {
        'orders': orders,
        'pending': pending,
        'confirmed': confirmed,
        'completed': completed,
    })


@login_required
def order_list_client(request):
    """Liste des commandes du client"""
    if not request.user.is_photographer():
        orders = request.user.orders.all()
        return render(request, 'orders/order_list_client.html', {'orders': orders})
    return redirect('photographer_dashboard')


@login_required
def order_detail(request, pk):
    """Détail d'une commande"""
    # Photographe ou client peut voir
    try:
        order = Order.objects.get(pk=pk, photographer=request.user)
    except Order.DoesNotExist:
        order = get_object_or_404(Order, pk=pk, client=request.user)

    form = None
    if request.user.is_photographer():
        form = OrderStatusForm(instance=order)
        if request.method == 'POST':
            form = OrderStatusForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, 'Commande mise à jour !')
                return redirect('order_detail', pk=pk)

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'form': form,
    })