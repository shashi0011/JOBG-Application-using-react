from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source="id", read_only=True)
    coverLetter = serializers.CharField(source="cover_letter")
    resume = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ["_id", "name", "email", "coverLetter", "phone", "address", "resume"]

    def get_resume(self, obj):
        return {"public_id": obj.resume_public_id, "url": obj.resume_url}
