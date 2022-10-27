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
from video.serializers import (VideoSerializer, VideoUploadForm, VideoForm,
                                      ImageForm)


class VideoInfoListAdminAPI(APIView):
    @admin_role_required
    def get(self, request):
        videos = VideoInfo.objects.filter(visible=True).order_by("-create_time")
        keyword = request.GET.get("keyword")
        if keyword:
            videos = videos.filter(title__contains=keyword)        
        return self.success(self.paginate_data(request, videos, VideoSerializer))

class FileUploadAPIView(CSRFExemptAPIView):
    request_parsers = ()
    @admin_role_required

    def post(self, request):

        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_video = form.cleaned_data["file_path"]
            video_thumbnail = form.cleaned_data["video_thumbnail"]
        else:
            
            return self.response({
                "success": False,
                "msg": "Upload failed. Add video thumbnail and video correctly"
            })
        title = request.POST.get("title") 
        if not title:
            return self.error("Invalid parameter, title is required")
        # video upload 
        suffix = os.path.splitext(uploaded_video.name)[-1].lower()
        if suffix not in [".mp4", ".flv", ".mov"]:
            return self.error("Unsupported file format, expect mp4,flv and mov")

        if uploaded_video.size > 100 * 1024 * 1024:
            return self.error("video is too large, expect < 100MB")

        random_name = rand_str(10)

        file_name = random_name + suffix

        suffix_image = os.path.splitext(video_thumbnail.name)[-1].lower()
        if suffix_image not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.response({
                "success": False,
                "msg": "Unsupported file format for video thumbnail ",
                "file_path": ""})

        img_name = random_name + suffix_image       

        Path(settings.VIDEO_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(settings.VIDEO_UPLOAD_DIR+"/thumbnail").mkdir(parents=True, exist_ok=True)
        try:
            with open(os.path.join(settings.VIDEO_UPLOAD_DIR, file_name), "wb") as f:
                for chunk in uploaded_video:
                    f.write(chunk)
            with open(os.path.join(settings.VIDEO_UPLOAD_DIR+"/thumbnail", img_name), "wb") as imgFile:
                for chunk in video_thumbnail:
                    imgFile.write(chunk)                    
        except IOError as e:
            logger.error(e)
            return self.response({
                "success": False,
                "msg": "Upload Error"})


        file_path = f"{settings.VIDEO_URI_PREFIX}/{file_name}"
        video_thumbnail_path = f"{settings.VIDEO_URI_PREFIX}/thumbnail/{img_name}"               
        video_data = VideoInfo.objects.create(file_path=file_path, video_thumbnail=video_thumbnail_path, title=title, created_by=request.user)
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

        data = {}
        video_form = VideoForm(request.POST, request.FILES)
        thumbnail_form = ImageForm(request.POST, request.FILES)
        title = request.POST.get("title")
        if title:
            data["title"] = title

        if video_form.is_valid():
            uploaded_video = video_form.cleaned_data["file_path"]
            suffix = os.path.splitext(uploaded_video.name)[-1].lower()
            if suffix not in [".mp4", ".flv", ".mov"]:
                return self.error("Unsupported video format, expect mp4,flv and mov")

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

        if thumbnail_form.is_valid():
            video_thumbnail = thumbnail_form.cleaned_data["video_thumbnail"]
            suffix_image = os.path.splitext(video_thumbnail.name)[-1].lower()
            if suffix_image not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
                return self.response({
                    "success": False,
                    "msg": "Unsupported file format for video thumbnail ",
                    "file_path": ""})

            thumbnail_name = rand_str(10) + suffix_image
            Path(settings.VIDEO_UPLOAD_DIR+"/thumbnail").mkdir(parents=True, exist_ok=True)
            try:
                with open(os.path.join(settings.VIDEO_UPLOAD_DIR+"/thumbnail", thumbnail_name), "wb") as f:
                    for chunk in video_thumbnail:
                        f.write(chunk)
            except IOError as e:
                logger.error(e)
                return self.response({
                    "success": False,
                    "msg": "Upload Error"})
            thumbnail_path = f"{settings.VIDEO_URI_PREFIX}/thumbnail/{thumbnail_name}"
            
            data["video_thumbnail"] = thumbnail_path  
        

        for k, v in data.items():
            setattr(video_info, k, v)
        video_info.save()
        return self.success(VideoSerializer(video_info).data)
