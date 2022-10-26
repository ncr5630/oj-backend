from django import forms
from utils.api import serializers
from utils.api._serializers import UsernameSerializer

from .models import VideoInfo


class VideoSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = VideoInfo
        fields = "__all__"


class CreateVideoInfoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)


class EditVideoInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=64)
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    visible = serializers.BooleanField()

class VideoUploadForm(forms.Form):
    file_path = forms.FileField()
    video_thumbnail = forms.FileField()

class VideoForm(forms.Form):
    file_path = forms.FileField()

class ImageForm(forms.Form):
    video_thumbnail = forms.FileField()