from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer
from apps.accounts.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inbox(request):
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')

    contacts = {}
    for msg in conversations:
        other = msg.receiver if msg.sender == request.user else msg.sender
        if other.id not in contacts:
            contacts[other.id] = {
                'user_id': other.id,
                'username': other.username,
                'full_name': other.get_full_name() or other.username,
                'avatar': request.build_absolute_uri(other.avatar.url)
                          if other.avatar else None,
                'last_message': msg.content,
                'last_message_time': msg.created_at.strftime('%d/%m %H:%M'),
                'unread': Message.objects.filter(
                    sender=other,
                    receiver=request.user,
                    is_read=False
                ).count()
            }

    return Response(list(contacts.values()))


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def conversation(request, username):
    other_user = User.objects.get(username=username)

    if request.method == 'GET':
        Message.objects.filter(
            sender=other_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

        msgs = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).order_by('created_at')

        serializer = MessageSerializer(msgs, many=True,
                                       context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        content = request.data.get('content', '').strip()
        if content:
            msg = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            serializer = MessageSerializer(msg, context={'request': request})
            return Response(serializer.data, status=201)
        return Response({'error': 'Message vide'}, status=400)