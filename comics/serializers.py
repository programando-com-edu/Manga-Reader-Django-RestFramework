from rest_framework import serializers,

from comics.models import Comic


class ComicSerializer(serializers.Serializer):
    class Meta:
        model = Comic
        fields = '__all__'
