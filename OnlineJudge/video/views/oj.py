import logging
import traceback
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from utils.api import APIView
from video.models import VideoInfo
from video.serializers import (VideoSerializer)
from account.decorators import login_required
from utils.shortcuts import check_is_id
from django.db.models import Q


class VideoInfoListAPI(APIView):
    @login_required
    def get(self, request):
        videos = VideoInfo.objects.select_related("created_by").filter(visible=True)
        keyword = request.GET.get("keyword")
        if keyword:
            videos = videos.filter(title__contains=keyword)

        return self.success(self.paginate_data(request, videos, VideoSerializer))


class VideoInfoAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @login_required
    def get(self, request):
        """
        get video list / get one video
        """

        video_id = request.GET.get("id")
        if not video_id or not check_is_id(video_id):
            return self.error("Invalid parameter, id is required")

        try:
            video = VideoInfo.objects.get(id=video_id)
            return self.success(VideoSerializer(video).data)
        except VideoInfo.DoesNotExist:
            return self.error("VideoInfo does not exist")

