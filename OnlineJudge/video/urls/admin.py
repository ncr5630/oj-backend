from django.conf.urls import url

from ..views.admin import VideoInfoUpdateAdminAPI, VideoInfoListAdminAPI, FileUploadAPIView

urlpatterns = [
    url(r"^video/?$", FileUploadAPIView.as_view(), name="video_info_admin_api"),
    url(r"^video_list/?$", VideoInfoListAdminAPI.as_view(), name="video_list_admin_api"),
    url(r"^video_update/?$", VideoInfoUpdateAdminAPI.as_view(), name="video_list_admin_api"),
]
