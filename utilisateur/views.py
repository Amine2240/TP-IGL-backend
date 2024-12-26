from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from utilisateur.models import Utilisateur

# Create your views here.


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_email = request.data.get("username")
        password = request.data.get("password")

        if not username_email or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = (
            Utilisateur.objects.filter(username=username_email).first()
            or Utilisateur.objects.filter(email=username_email).first()
        )
        if not user or not user.check_password(password):
            raise AuthenticationFailed("Incorrect username or password")

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response = Response(
            {
                "message": "Login successful",
            }
        )

        response.set_cookie(
            key="auth_token",
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        return response
