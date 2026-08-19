from django.test import TestCase
from users.models import User
from articles.models import Article, Category
import json


class ArticleAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="pass")
        self.token = self.user.token = "test_token_123"
        self.user.save()
        self.category = Category.objects.create(name="Tech")
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {self.token}"

    def test_create_article_success(self):
        response = self.client.post(
            "/api/articles/",
            data=json.dumps(
                {
                    "title": "My Article",
                    "content": "Content",
                    "category_id": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().author, self.user)

    def test_create_article_missing_fields(self):
        response = self.client.post(
            "/api/articles/",
            data=json.dumps({"title": "No content"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

    def test_update_article_unauthorized(self):
        article = Article.objects.create(title="Old", content="Old", author=self.user)
        other_user = User.objects.create_user(username="other", password="pass")
        other_user.token = "other_token"
        other_user.save()
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer other_token"
        response = self.client.put(
            f"/api/articles/{article.id}",
            data=json.dumps({"title": "Hacked"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_article_authorized(self):
        article = Article.objects.create(
            title="To delete", content="x", author=self.user
        )
        response = self.client.delete(f"/api/articles/{article.id}")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.filter(id=article.id).exists())
