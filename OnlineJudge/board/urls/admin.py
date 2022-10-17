from django.conf.urls import url

from ..views.admin import BoardAdminAPI, BoardListAdminAPI

urlpatterns = [
    url(r"^board/?$", BoardAdminAPI.as_view(), name="board_admin_api"),
    url(r"^boards/?$", BoardListAdminAPI.as_view(), name="boards_admin_api"),
]
