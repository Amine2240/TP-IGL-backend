from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        # 1. Try cookie first
        token = request.COOKIES.get("auth_token")

        # 2. Fall back to Authorization header ("Token <jwt>" or "Bearer <jwt>")
        if not token:
            header = request.META.get("HTTP_AUTHORIZATION", "")
            if header:
                parts = header.split()
                if len(parts) == 2 and parts[0].lower() in ("token", "bearer"):
                    token = parts[1]

        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except AuthenticationFailed:
            return None
