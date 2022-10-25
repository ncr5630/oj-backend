from django.conf.urls import url
from django.conf import settings
from ..views.oj import VideoInfoAPI, VideoInfoListAPI
from django.conf.urls.static import static



urlpatterns = [
    url(r"^video/?$", VideoInfoAPI.as_view(), name="video_info_api"),
    url(r"^videos/?$", VideoInfoListAPI.as_view(), name="video_info_list_api"),
]

if settings.DEBUG:
  urlpatterns += static(settings.VIDEO_UPLOAD_DIR, document_root=settings.STATICFILES_DIRS)