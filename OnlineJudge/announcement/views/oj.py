from utils.api import APIView

from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer


class AnnouncementAPI(APIView):
    def get(self, request):
        notice = request.GET.get("notice")
        is_visible = request.GET.get("visible")
        keyword = request.GET.get("keyword")
        announcements = Announcement.objects.all().order_by("-create_time")        
        if keyword:
            announcements = announcements.filter(title__contains=keyword)        
        if notice == "true":
            announcements = announcements.filter(notice=True)
        if is_visible == "true":
            announcements = announcements.filter(visible=True)

        return self.success(self.paginate_data(request, announcements, AnnouncementSerializer))
