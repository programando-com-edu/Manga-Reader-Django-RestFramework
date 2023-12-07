from rest_framework import serializers

from comics.models import Chapter, Comic


class ComicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comic
        fields = '__all__'

class ComicWithCapsSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()
    
    def get_chapters(self, obj):
        chapters = obj.chapter_set.all()
        return ChapterSerializer(chapters, many=True).data
    class Meta:
        model = Comic
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'