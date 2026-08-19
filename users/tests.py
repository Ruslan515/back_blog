from django.test import TestCase
from users.models import User
import json


class UserAPITest(TestCase):
    def setUp(self):
        self.register_url = "/api/users/register"
        self.login_url = "/api/users/login"

    def test_register_success(self):
        response = self.client.post(
            self.register_url,
            data=json.dumps({"username": "testuser", "password": "testpass123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("token", data)
        self.assertEqual(data["username"], "testuser")
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_duplicate(self):
        User.objects.create_user(username="testuser", password="testpass123")
        response = self.client.post(
            self.register_url,
            data=json.dumps({"username": "testuser", "password": "another"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Username already taken")

    def test_login_success(self):
        User.objects.create_user(username="testuser", password="testpass123")
        response = self.client.post(
            self.login_url,
            data=json.dumps({"username": "testuser", "password": "testpass123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_fail(self):
        response = self.client.post(
            self.login_url,
            data=json.dumps({"username": "wrong", "password": "wrong"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
