from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import ClientGallery, Photo
from .serializers import ClientGallerySerializer, PhotoSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def gallery_list_create(request):
    if request.method == 'GET':
        galleries = ClientGallery.objects.filter(photographer=request.user)
        serializer = ClientGallerySerializer(galleries, many=True,
                                             context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClientGallerySerializer(data=request.data,
                                             context={'request': request})
        if serializer.is_valid():
            serializer.save(photographer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def gallery_detail_delete(request, pk):
    try:
        gallery = ClientGallery.objects.get(pk=pk, photographer=request.user)
    except ClientGallery.DoesNotExist:
        return Response({'error': 'Galerie introuvable'}, status=404)

    if request.method == 'GET':
        serializer = ClientGallerySerializer(gallery, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'DELETE':
        gallery.delete()
        return Response({'message': 'Galerie supprimée'}, status=204)


@api_view(['POST'])
@permission_classes([AllowAny])
def gallery_access(request):
    code = request.data.get('access_code', '').upper()
    try:
        gallery = ClientGallery.objects.get(access_code=code, is_active=True)
        serializer = ClientGallerySerializer(gallery, context={'request': request})
        return Response(serializer.data)
    except ClientGallery.DoesNotExist:
        return Response({'error': 'Code incorrect ou galerie introuvable'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_photos(request, pk):
    try:
        gallery = ClientGallery.objects.get(pk=pk, photographer=request.user)
    except ClientGallery.DoesNotExist:
        return Response({'error': 'Galerie introuvable'}, status=404)

    files = request.FILES.getlist('images')
    photos = []
    for f in files:
        photo = Photo.objects.create(
            gallery=gallery,
            image=f,
            is_downloadable=request.data.get('is_downloadable', True)
        )
        photos.append(PhotoSerializer(photo, context={'request': request}).data)

    return Response({'uploaded': len(photos), 'photos': photos})