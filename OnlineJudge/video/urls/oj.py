from django.conf.urls import url

from ..views.oj import VideoInfoAPI, VideoInfoListAPI

urlpatterns = [
    url(r"^video/?$", VideoInfoAPI.as_view(), name="video_info_api"),
    url(r"^videos/?$", VideoInfoListAPI.as_view(), name="video_info_list_api"),
]
