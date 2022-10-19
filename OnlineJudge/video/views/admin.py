import logging
import sys
import traceback
from account.decorators import admin_role_required
from utils.api import APIView, validate_serializer

from video.models import VideoInfo
from video.serializers import (VideoSerializer, CreateVideoInfoSerializer,
                                      EditVideoInfoSerializer)


class VideoInfoListAdminAPI(APIView):
    @admin_role_required
    def get(self, request):
        videos = VideoInfo.objects.filter(visible=True)
        return self.success(self.paginate_data(request, videos, VideoSerializer))


class VideoInfoAdminAPI(APIView):
    @validate_serializer(CreateVideoInfoSerializer)
    @admin_role_required
    def post(self, request):
        """
        publish VideoInfo
        """
        data = request.data
        videos = VideoInfo.objects.create(title=data["title"],
                                                   content=data["content"],
                                                   created_by=request.user,
                                                   visible=data["visible"])
        return self.success(VideoSerializer(videos).data)

    @validate_serializer(EditVideoInfoSerializer)
    @admin_role_required
    def put(self, request):
        """
        edit VideoInfo
        """
        data = request.data
        try:
            video_info=VideoInfo.objects.get(id=data.pop("id"))
        except VideoInfo.DoesNotExist:
            return self.error("Videos  does not exist")

        for k, v in data.items():
            setattr(video_info, k, v)
        video_info.save()
        return self.success(VideoSerializer(video_info).data)

    @admin_role_required
    def get(self, request):
        """
        get VideoInfo list / get one VideoInfo
        """
        video_id = request.GET.get("id")
        if video_id:
            try:
                video = VideoInfo.objects.get(id=video_id)
                return self.success(VideoSerializer(video).data)
            except VideoInfo.DoesNotExist:
                return self.error("VideoInfo does not exist")
        videos = VideoInfo.objects.all().order_by("-create_time")
        # if request.GET.get("visible") == "true":
        #     VideoInfo = VideoInfo.filter(visible=True)
        return self.success(self.paginate_data(request, videos, VideoSerializer))

    @admin_role_required
    def delete(self, request):
        if request.GET.get("id"):
            VideoInfo.objects.filter(id=request.GET["id"]).delete()
        return self.success()
