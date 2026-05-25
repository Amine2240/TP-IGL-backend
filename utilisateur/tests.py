from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "test_user"
        self.email = "test.user@example.com"
        self.password = "Password123!"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            nom="Test",
            prenom="User",
            role="patient",
            date_naissance="1990-01-01",
            telephone="0550000000"
        )

    def test_login_with_username_success(self):
        response = self.client.post("/api/users/login/", {
            "username": self.username,
            "password": self.password
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("auth_token", response.cookies)

    def test_login_with_email_success(self):
        response = self.client.post("/api/users/login/", {
            "username": self.email,
            "password": self.password
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("auth_token", response.cookies)

    def test_login_invalid_credentials(self):
        response = self.client.post("/api/users/login/", {
            "username": self.username,
            "password": "WrongPassword!"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_with_cookie_success(self):
        # First log in to get token
        login_response = self.client.post("/api/users/login/", {
            "username": self.username,
            "password": self.password
        }, format="json")
        token = login_response.data["token"]
        
        # Clear cookies to ensure client doesn't hold it implicitly, then set it explicitly
        self.client.cookies.clear()
        self.client.cookies["auth_token"] = token
        
        response = self.client.get("/api/users/user-info/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.email)

    def test_user_info_with_token_header_success(self):
        login_response = self.client.post("/api/users/login/", {
            "username": self.username,
            "password": self.password
        }, format="json")
        token = login_response.data["token"]
        
        # Clear cookies so it has to fall back to header
        self.client.cookies.clear()
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get("/api/users/user-info/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.email)

    def test_user_info_with_bearer_header_success(self):
        login_response = self.client.post("/api/users/login/", {
            "username": self.username,
            "password": self.password
        }, format="json")
        token = login_response.data["token"]
        
        # Clear cookies so it has to fall back to header
        self.client.cookies.clear()
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/users/user-info/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.email)

    def test_user_info_unauthorized(self):
        self.client.cookies.clear()
        self.client.credentials() # Clear all credentials
        response = self.client.get("/api/users/user-info/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
