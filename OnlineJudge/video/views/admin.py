from asyncio.log import logger
import logging
import os
import sys
import traceback
from django.utils.timezone import now
from pathlib import Path
from django.conf import settings
from account.decorators import admin_role_required
from utils.api import APIView, validate_serializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from utils.api import CSRFExemptAPIView, validate_serializer
from django.utils.decorators import method_decorator
from utils.shortcuts import rand_str, check_is_id, datetime2str
from video.models import VideoInfo
from video.serializers import (VideoSerializer, VideoUploadForm, CreateVideoInfoSerializer,
                                      EditVideoInfoSerializer)


class VideoInfoListAdminAPI(APIView):
    @admin_role_required
    def get(self, request):
        videos = VideoInfo.objects.filter(visible=True).order_by("-create_time")
        return self.success(self.paginate_data(request, videos, VideoSerializer))

class FileUploadAPIView(CSRFExemptAPIView):
    request_parsers = ()
    @admin_role_required
    def post(self, request):

        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_video = form.cleaned_data["file_path"]
        else:
            return self.response({
                "success": False,
                "msg": "Upload failed"
            })

        suffix = os.path.splitext(uploaded_video.name)[-1].lower()
        if suffix not in [".mp4", ".flv", ".mov"]:
            return self.error("Unsupported file format, expect mp4,flv and mov")

        if uploaded_video.size > 100 * 1024 * 1024:
            return self.error("video is too large, expect < 100MB")

        file_name = rand_str(10) + suffix

        Path(settings.VIDEO_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        try:
            with open(os.path.join(settings.VIDEO_UPLOAD_DIR, file_name), "wb") as f:
                for chunk in uploaded_video:
                    f.write(chunk)
        except IOError as e:
            logger.error(e)
            return self.response({
                "success": False,
                "msg": "Upload Error"})
        file_path = f"{settings.VIDEO_URI_PREFIX}/{file_name}"
        title = request.POST.get("title")        
        video_data = VideoInfo.objects.create(file_path=file_path, title=title, created_by=request.user)
        return self.success(VideoSerializer(video_data).data)


    @admin_role_required
    def get(self, request):
        id = request.GET.get("id")
        if not id or not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            video = VideoInfo.objects.get(id=id, visible=True)
        except VideoInfo.DoesNotExist:
            return self.error("VideoInfo does not exist")
        data = VideoSerializer(video).data
        data["now"] = datetime2str(now())
        return self.success(data)

    @admin_role_required
    def delete(self, request):
        if request.GET.get("id"):
            VideoInfo.objects.filter(id=request.GET["id"]).delete()
        return self.success()


class VideoInfoUpdateAdminAPI(APIView):

    request_parsers = ()
    @admin_role_required
    def post(self, request):
        """
        edit VideoInfo
        """
        id = request.GET.get("id")
        if not id or not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            video_info=VideoInfo.objects.get(id=id)
        except VideoInfo.DoesNotExist:
            return self.error("Videos  does not exist")
        # video_info_data = VideoSerializer(video_info).data
        data = {}
        form = VideoUploadForm(request.POST, request.FILES)
        title = request.POST.get("title")
        if form.is_valid():
            uploaded_video = form.cleaned_data["file_path"]
            suffix = os.path.splitext(uploaded_video.name)[-1].lower()
            if suffix not in [".mp4", ".flv", ".mov"]:
                return self.error("Unsupported file format, expect mp4,flv and mov")

            if uploaded_video.size > 100 * 1024 * 1024:
                return self.error("video is too large, expect < 100MB")

            file_name = rand_str(10) + suffix

            Path(settings.VIDEO_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
            try:
                with open(os.path.join(settings.VIDEO_UPLOAD_DIR, file_name), "wb") as f:
                    for chunk in uploaded_video:
                        f.write(chunk)
            except IOError as e:
                logger.error(e)
                return self.response({
                    "success": False,
                    "msg": "Upload Error"})
            file_path = f"{settings.VIDEO_URI_PREFIX}/{file_name}"
            
            data["file_path"] = file_path            

        data["title"] = title

        for k, v in data.items():
            setattr(video_info, k, v)
        video_info.save()
        return self.success(VideoSerializer(video_info).data)
