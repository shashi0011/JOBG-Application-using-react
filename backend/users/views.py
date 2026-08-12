from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError

from .serializers import UserSerializer
from .jwt_utils import generate_token, set_token_cookie

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        role = data.get("role")

        if not all([name, email, phone, password, role]):
            raise ValidationError("Please fill full form!")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered!")

        user = User.objects.create_user(
            email=email, name=name, phone=phone, role=role, password=password
        )

        token = generate_token(user)
        response = Response(
            {
                "success": True,
                "user": UserSerializer(user).data,
                "message": "user registered",
                "token": token,
            },
            status=200,
        )
        return set_token_cookie(response, token)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not all([email, password, role]):
            raise ValidationError("Please provide email ,password and role.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Invalid Email Or Password.")

        if not check_password(password, user.password):
            raise ValidationError("Invalid Email Or Password.")

        if user.role != role:
            raise ValidationError(f"User with provided email and {role} not found!")

        token = generate_token(user)
        response = Response(
            {
                "success": True,
                "user": UserSerializer(user).data,
                "message": "user login",
                "token": token,
            },
            status=200,
        )
        return set_token_cookie(response, token)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = Response(
            {"success": True, "message": "Logged Out Successfully."}, status=200
        )
        response.set_cookie(
            key="token", value="", max_age=0, httponly=True
        )
        return response


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"success": True, "user": UserSerializer(request.user).data}, status=200
        )
