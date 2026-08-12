import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .jwt_utils import decode_token


class CookieJWTAuthentication(BaseAuthentication):
    """
    Equivalent of middlewares/auth.js -> isAuthenticated.
    Reads the httpOnly 'token' cookie set at login/register, verifies it,
    and attaches the resolved user to request.user.
    """

    def authenticate(self, request):
        token = request.COOKIES.get("token")
        if not token:
            # Returning None (not raising) lets DRF permission classes
            # decide what happens next -- same as isAuthenticated calling
            # next(new ErrorHandler("User Not Authorized", 401)) only when
            # the route actually requires auth.
            return None

        try:
            decoded = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Json Web Token is expired, Try again!")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Json Web Token is invalid, Try again!")

        try:
            user = User.objects.get(id=decoded["id"])
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Authorized")

        return (user, None)

    def authenticate_header(self, request):
        # Presence of this makes DRF respond 401 (not 403) when
        # IsAuthenticated rejects an unauthenticated request --
        # matching the Node app's "User Not Authorized", 401.
        return "Bearer"
