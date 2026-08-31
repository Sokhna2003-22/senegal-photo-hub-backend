from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    return Response({'error': 'Identifiants incorrects'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_api(request):
    return Response(UserSerializer(request.user, context={'request': request}).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def photographers_list(request):
    photographers = User.objects.filter(role='photographer')
    return Response(UserSerializer(photographers, many=True,
                                   context={'request': request}).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def photographer_detail(request, username):
    try:
        user = User.objects.get(username=username, role='photographer')
        return Response(UserSerializer(user, context={'request': request}).data)
    except User.DoesNotExist:
        return Response({'error': 'Photographe introuvable'}, status=404)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("DATA REÇUE:", request.data)  # ← Ajoute cette ligne
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("ERREURS:", serializer.errors)  # ← Et celle-ci
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)