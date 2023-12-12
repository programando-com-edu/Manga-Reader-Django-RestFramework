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
        qs = Comic.objects.all()
        if title and title != 'null':
            qs = qs.filter(title__icontains=title)
        return qs if title else qs[:30]


class ChapterView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def get_chapter(number, comic):
        return Chapter.objects.filter(comic=comic, number=number).first()

    def get_images(self):
        return AsuraChapter(self.object.link).get_chapters_images()
    
    def get_next_chapter(self):
        chapter_num = str(int(self.object.number) + 1)
        chapter = self.get_chapter(chapter_num, self.comic)
        return chapter.pk if chapter else None

    def get_previous_chapter(self):
        chapter_num = str(int(self.object.number) - 1)
        chapter = self.get_chapter(chapter_num, self.comic)
        return chapter.pk if chapter else None

    def build_data(self):
        return {"next_chap": self.get_next_chapter(),
                "prev_chap": self.get_previous_chapter(),
                "images": self.get_images(),
                "comic_id": self.comic.pk}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            self.comic = self.object.comic
            return Response(self.build_data(), status=status.HTTP_200_OK)
        return Response('', status=status.HTTP_404_NOT_FOUND)
