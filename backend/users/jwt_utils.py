import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_token(user):
    """Equivalent of userSchema.methods.getJWTToken in the Node app."""
    payload = {
        "id": str(user.id),
        "exp": datetime.utcnow() + timedelta(days=settings.JWT_EXPIRES_DAYS),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])


def set_token_cookie(response, token):
    """Equivalent of utils/jwtToken.js -> sendToken (httpOnly cookie)."""
    max_age = settings.COOKIE_EXPIRE_DAYS * 24 * 60 * 60
    response.set_cookie(
        key="token",
        value=token,
        max_age=max_age,
        httponly=True,
        samesite=settings.COOKIE_SAMESITE,
        secure=settings.COOKIE_SECURE,
    )
    return response
