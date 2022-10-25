from django.conf.urls import url
from django.conf import settings
from ..views.oj import VideoInfoAPI, VideoInfoListAPI
from django.conf.urls.static import static



urlpatterns = [
    url(r"^video/?$", VideoInfoAPI.as_view(), name="video_info_api"),
    url(r"^video_list/?$", VideoInfoListAPI.as_view(), name="video_info_list_api"),
]
