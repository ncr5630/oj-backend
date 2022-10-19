from django.conf.urls import url

from ..views.admin import VideoInfoAdminAPI, VideoListAdminAPI

urlpatterns = [
    url(r"^video/?$", VideoInfoAdminAPI.as_view(), name="video_info_admin_api"),
    url(r"^videos/?$", VideoListAdminAPI.as_view(), name="video_list_admin_api"),
]
