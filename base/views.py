from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView

from base.serializers import UserSerializer, ComicsReadSerializer
from base.models import ComicsRead
from comics.models import Chapter
from comics.serializers import ComicWithCapsSerializer

User = get_user_model()


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]
    
    def post(self, request, *arg, **kwargs):
        data = request.data
        password = data.get('password')
        username = data.get('username')
        email = data.get('email')
        data.pop('username', None)
        data.pop('password', None)
        data.pop('email', None)

        user = User.objects.create_user(username, email, password, **data)
        serialized_user = self.get_serializer(user)

        return Response(serialized_user.data, status=status.HTTP_201_CREATED)


class MeAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        instance = User.objects.get(pk=request.user.pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ComicsReadView(APIView):
    serializer_class = ComicsReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ComicsRead.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        chapter_id = request.data.get('chapter')
        chapter = Chapter.objects.filter(pk=chapter_id).first()
        comic_read = ComicsRead.objects.filter(user=user, last_chapter__comic=chapter.comic.pk).first()
        if comic_read:
            comic_read.last_chapter = chapter
            comic_read.save()
        else:
            comic_read = ComicsRead(user=user, last_chapter=chapter)
            comic_read.save()
        serializer = self.serializer_class(comic_read)
        return Response(serializer.data)