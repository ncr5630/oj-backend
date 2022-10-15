from django.conf.urls import url

from ..views.admin import UserAdminAPI, GenerateUserAPI, UserDetailsAdminAPI

urlpatterns = [
    url(r"^user/?$", UserAdminAPI.as_view(), name="user_admin_api"),
    url(r"^generate_user/?$", GenerateUserAPI.as_view(), name="generate_user_api"),
    url(r"^user_details/?$", UserDetailsAdminAPI.as_view(), name="user_details_api"),
]
