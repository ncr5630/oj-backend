from utils.api.tests import APITestCase

from .models import VideoInfo


class VideoInfoAdminTest(APITestCase):
    def setUp(self):
        self.user = self.create_super_admin()
        self.url = self.reverse("video_info_admin_api")

    def test_video_info_list(self):
        response = self.client.get(self.url)
        self.assertSuccess(response)

    def create_video_info(self):
        return self.client.post(self.url, data={"title": "test", "content": "test", "visible": True})

    def test_create_VideoInfo(self):
        resp = self.create_video_info()
        self.assertSuccess(resp)
        return resp

    def test_edit_video_info(self):
        data = {"id": self.create_video_info().data["data"]["id"], "title": "ahaha", "content": "test content",
                "visible": False}
        resp = self.client.put(self.url, data=data)
        self.assertSuccess(resp)
        resp_data = resp.data["data"]
        self.assertEqual(resp_data["title"], "ahaha")
        self.assertEqual(resp_data["content"], "test content")
        self.assertEqual(resp_data["visible"], False)

    def test_delete_video_info(self):
        id = self.test_create_video_info().data["data"]["id"]
        resp = self.client.delete(self.url + "?id=" + str(id))
        self.assertSuccess(resp)
        self.assertFalse(VideoInfo.objects.filter(id=id).exists())


class VideoInfoAPITest(APITestCase):
    def setUp(self):
        self.user = self.create_super_admin()
        VideoInfo.objects.create(title="title", content="content", visible=True, created_by=self.user)
        self.url = self.reverse("video_info_api")

    def test_get_video_info_list(self):
        resp = self.client.get(self.url)
        self.assertSuccess(resp)
