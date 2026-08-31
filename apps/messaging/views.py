from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Message
from apps.accounts.models import User


@login_required
def inbox(request):
    """Boîte de réception"""
    # Toutes les conversations de l'utilisateur
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')

    # Récupérer les interlocuteurs uniques
    contacts = {}
    for msg in conversations:
        other = msg.receiver if msg.sender == request.user else msg.sender
        if other.id not in contacts:
            contacts[other.id] = {
                'user': other,
                'last_message': msg,
                'unread': Message.objects.filter(
                    sender=other,
                    receiver=request.user,
                    is_read=False
                ).count()
            }

    return render(request, 'messaging/inbox.html', {
        'contacts': contacts.values(),
    })


@login_required
def conversation(request, username):
    """Conversation avec un utilisateur"""
    other_user = get_object_or_404(User, username=username)

    # Marquer les messages comme lus
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    # Récupérer tous les messages entre les deux
    msgs = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('conversation', username=username)

    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': msgs,
    })


@login_required
def new_message(request, username):
    """Démarrer une conversation"""
    other_user = get_object_or_404(User, username=username)
    return redirect('conversation', username=username)

from django.http import JsonResponse

@login_required
def get_new_messages(request, username):
    """Retourne les messages en JSON pour AJAX"""
    other_user = get_object_or_404(User, username=username)

    msgs = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    # Marquer comme lus
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    data = {
        'count': msgs.count(),
        'messages': [
            {
                'content': msg.content,
                'is_mine': msg.sender == request.user,
                'created_at': msg.created_at.strftime('%d/%m %H:%M'),
            }
            for msg in msgs
        ]
    }
    return JsonResponse(data)