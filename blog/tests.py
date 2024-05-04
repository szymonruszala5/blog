from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )
        cls.post = Post.objects.create(
            title="Title",
            body="Body",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.body, "Body")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "Title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Body")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(
            reverse(
                "post_detail",
                kwargs={"pk": self.post.pk},
            )
        )
        no_response = self.client.get("/post/99/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Title")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_createview(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "test title",
                "body": "test body",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "test title")
        self.assertEqual(Post.objects.last().body, "test body")

    def test_post_updateview(self):
        response = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title": "test title (updated)",
                "body": "test body (updated)",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "test title (updated)")
        self.assertEqual(Post.objects.last().body, "test body (updated)")

    def test_post_deleteview(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)
