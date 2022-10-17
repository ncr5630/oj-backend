from utils.api import serializers
from utils.api._serializers import UsernameSerializer

from .models import Board


class CreateBoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    visible = serializers.BooleanField()


class BoardSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = Board
        fields = "__all__"


class EditBoardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=64)
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    visible = serializers.BooleanField()
