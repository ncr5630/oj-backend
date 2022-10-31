from utils.api import APIView

from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer


class AnnouncementAPI(APIView):
    def get(self, request):
        notice = request.GET.get("notice")
        is_visible = request.GET.get("visible")

        announcements = Announcement.objects.all().order_by("-create_time")
        if notice == "true":
            announcements = announcements.filter(notice=True)
        if is_visible == "true":
            announcements = announcements.filter(visible=True)

        return self.success(self.paginate_data(request, announcements, AnnouncementSerializer))
