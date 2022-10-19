from utils.api import APIView, validate_serializer

from video.models import VideoInfo
from video.serializers import (VideoSerializer)
from account.decorators import login_required



class VideoInfoListAPI(APIView):
    @login_required
    def get(self, request):
        # videos = VideoInfo.objects.filter(visible=True)
        videos = VideoInfo.objects.select_related("created_by").filter(visible=True)
        return self.success(self.paginate_data(request, videos, VideoSerializer))



class VideoInfoAPI(APIView):
    @login_required
    def get(self, request):
        """
        get video list / get one video
        """
        video_id = request.GET.get("id")
        if video_id:
            try:
                video = VideoInfo.objects.get(id=video_id)
                return self.success(VideoSerializer(video).data)
            except VideoInfo.DoesNotExist:
                return self.error("VideoInfo does not exist")
        videos = VideoInfo.objects.all().order_by("-create_time")

        return self.success(self.paginate_data(request, videos, VideoSerializer))

