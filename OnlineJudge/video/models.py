from django.db import models

from account.models import User
from utils.models import RichTextField
from django.conf import settings

class VideoInfo(models.Model):
    title = models.TextField()
    # HTML
    file_path = models.FileField(blank=False, null=False)
    video_thumbnail = models.FileField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")    
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update_time = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = "video_info"
        ordering = ("-create_time",)

