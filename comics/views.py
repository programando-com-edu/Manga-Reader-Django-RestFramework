from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from .models import Chapter, Comic
from .serializers import ComicSerializer, ComicWithCapsSerializer
from .utils import AsuraCatalog, AsuraChapter

# Create your views here.


# class GetCatalogAsura(APIView):
#     def get(self, request, *args, **kwargs):
#         AsuraCatalog()
#         return Response('', status=status.HTTP_201_CREATED)


class RetriveComicView(generics.RetrieveAPIView):
    queryset = Comic.objects.all()
    renderer_classes = [JSONRenderer]
    serializer_class = ComicWithCapsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ComicListView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ComicSerializer
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        title = self.request.query_params.get('title', '')
        return Comic.objects.filter(title__icontains=title)

class ChapterImages(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    renderer_classes = [JSONRenderer]
    # serializer_class = ComicWithCapsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def get(self, request, *args, **kwargs):
        chapter = self.get_object()
        if chapter:
            images_links =  AsuraChapter(chapter.link).get_chapters_images()
        
        return Response(images_links, status=status.HTTP_200_OK)