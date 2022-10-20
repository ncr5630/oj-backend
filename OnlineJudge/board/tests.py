from utils.api.tests import APITestCase

from .models import Board


class BoardAdminTest(APITestCase):
    def setUp(self):
        self.user = self.create_super_admin()
        self.url = self.reverse("Board_admin_api")

    def test_Board_list(self):
        response = self.client.get(self.url)
        self.assertSuccess(response)

    def create_Board(self):
        return self.client.post(self.url, data={"title": "test", "content": "test", "visible": True})

    def test_create_Board(self):
        resp = self.create_Board()
        self.assertSuccess(resp)
        return resp

    def test_edit_Board(self):
        data = {"id": self.create_Board().data["data"]["id"], "title": "ahaha", "content": "test content",
                "visible": False}
        resp = self.client.put(self.url, data=data)
        self.assertSuccess(resp)
        resp_data = resp.data["data"]
        self.assertEqual(resp_data["title"], "ahaha")
        self.assertEqual(resp_data["content"], "test content")
        self.assertEqual(resp_data["visible"], False)

    def test_delete_Board(self):
        id = self.test_create_Board().data["data"]["id"]
        resp = self.client.delete(self.url + "?id=" + str(id))
        self.assertSuccess(resp)
        self.assertFalse(Board.objects.filter(id=id).exists())


class BoardAPITest(APITestCase):
    def setUp(self):
        self.user = self.create_super_admin()
        Board.objects.create(title="title", content="content", visible=True, created_by=self.user)
        self.url = self.reverse("Board_api")

    def test_get_Board_list(self):
        resp = self.client.get(self.url)
        self.assertSuccess(resp)
