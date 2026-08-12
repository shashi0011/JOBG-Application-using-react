from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # password (via password_hash) is deliberately excluded, mirroring
        # `select: false` on the password field in the original Mongoose schema.
        fields = ["id", "name", "email", "phone", "role", "created_at"]
