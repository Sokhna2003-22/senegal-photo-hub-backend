from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import PortfolioAlbum, PortfolioPhoto
from .serializers import PortfolioAlbumSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def public_albums(request):
    albums = PortfolioAlbum.objects.filter(is_public=True).order_by('-created_at')
    serializer = PortfolioAlbumSerializer(albums, many=True,
                                          context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def album_detail(request, pk):
    try:
        album = PortfolioAlbum.objects.get(pk=pk, is_public=True)
        serializer = PortfolioAlbumSerializer(album, context={'request': request})
        return Response(serializer.data)
    except PortfolioAlbum.DoesNotExist:
        return Response({'error': 'Album introuvable'}, status=404)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_albums(request):
    if request.method == 'GET':
        albums = PortfolioAlbum.objects.filter(photographer=request.user)
        serializer = PortfolioAlbumSerializer(albums, many=True,
                                              context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PortfolioAlbumSerializer(data=request.data,
                                              context={'request': request})
        if serializer.is_valid():
            album = serializer.save(photographer=request.user)
            files = request.FILES.getlist('photos')
            for f in files:
                PortfolioPhoto.objects.create(album=album, image=f)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_album(request, pk):
    try:
        album = PortfolioAlbum.objects.get(pk=pk, photographer=request.user)
        album.delete()
        return Response({'message': 'Album supprimé'}, status=204)
    except PortfolioAlbum.DoesNotExist:
        return Response({'error': 'Album introuvable'}, status=404)