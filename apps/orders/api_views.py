from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from apps.accounts.models import User


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    if request.method == 'GET':
        if request.user.is_photographer():
            orders = Order.objects.filter(photographer=request.user)
        else:
            orders = Order.objects.filter(client=request.user)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        photographer_username = request.data.get('photographer_username')
        try:
            photographer = User.objects.get(username=photographer_username,
                                            role='photographer')
        except User.DoesNotExist:
            return Response({'error': 'Photographe introuvable'}, status=404)

        data = request.data.copy()
        data['photographer_id'] = photographer.id

        serializer = OrderSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(client=request.user, photographer=photographer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def order_detail_update(request, pk):
    try:
        if request.user.is_photographer():
            order = Order.objects.get(pk=pk, photographer=request.user)
        else:
            order = Order.objects.get(pk=pk, client=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Commande introuvable'}, status=404)

    if request.method == 'GET':
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PATCH':
        if not request.user.is_photographer():
            return Response({'error': 'Non autorisé'}, status=403)
        serializer = OrderSerializer(order, data=request.data,
                                     partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)