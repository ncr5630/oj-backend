from utils.api import serializers
from utils.api._serializers import UsernameSerializer

from .models import VideoInfo


class VideoSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = VideoInfo
        fields = "__all__"


class CreateVideoInfoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    visible = serializers.BooleanField()


class EditVideoInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=64)
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    visible = serializers.BooleanField()