from django.test import TestCase
from users.models import User
from articles.models import Article
from comments.models import Comment
import json


class CommentAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="commenter", password="pass")
        self.user.token = "comment_token"
        self.user.save()
        self.article = Article.objects.create(
            title="Test Article", content="...", author=self.user
        )
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {self.user.token}"

    def test_create_comment_success(self):
        response = self.client.post(
            "/api/comments/",
            data=json.dumps({"article_id": self.article.id, "text": "Nice!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.user)

    def test_create_comment_invalid_article(self):
        response = self.client.post(
            "/api/comments/",
            data=json.dumps({"article_id": 999, "text": "Nice!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)  # get_object_or_404 вернёт 404

    def test_update_comment_authorized(self):
        comment = Comment.objects.create(
            author=self.user, article=self.article, text="Old"
        )
        response = self.client.put(
            f"/api/comments/{comment.id}",
            data=json.dumps({"text": "New text"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.text, "New text")

    def test_update_comment_unauthorized(self):
        comment = Comment.objects.create(
            author=self.user, article=self.article, text="Old"
        )
        other_user = User.objects.create_user(username="hacker", password="pass")
        other_user.token = "hack_token"
        other_user.save()
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer hack_token"
        response = self.client.put(
            f"/api/comments/{comment.id}",
            data=json.dumps({"text": "Hacked"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
