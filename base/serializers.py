from django.contrib.auth import get_user_model
from rest_framework import serializers

from base.models import ComicsRead
from comics.models import Chapter
from comics.serializers import ComicSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'is_active']


class ComicsReadSerializer(serializers.ModelSerializer):
    chapter = serializers.SerializerMethodField()

    def get_chapter(self, obj):
        return ComicReadChapterSerializer(obj.last_chapter).data

    class Meta:
        model = ComicsRead
        fields = '__all__'


class ComicReadChapterSerializer(serializers.ModelSerializer):
    comic_data = serializers.SerializerMethodField()
    next_chapter = serializers.SerializerMethodField()
    def get_comic_data(self, obj):
        return ComicSerializer(obj.comic).data

    def get_next_chapter(self, obj):
        chapter_num = str(int(obj.number) + 1)
        next_chapter = Chapter.objects.filter(comic=obj.comic, number=chapter_num).first()
        return next_chapter.pk if next_chapter else None
    class Meta:
        model = Chapter
        fields = '__all__'