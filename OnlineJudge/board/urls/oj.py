from django.conf.urls import url

from ..views.oj import BoardAPI, BoardListAPI, BoardViewCountAPI

urlpatterns = [
    url(r"^board/?$", BoardAPI.as_view(), name="bulletin_board_api"),
    url(r"^boards/?$", BoardListAPI.as_view(), name="bulletin_boards_api"),
    url(r"^board_views/?$", BoardViewCountAPI.as_view(), name="bulletin_board_views_api"),
]
