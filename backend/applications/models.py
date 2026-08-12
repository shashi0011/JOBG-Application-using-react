from django.db import models
from django.conf import settings


class Application(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    cover_letter = models.TextField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    resume_public_id = models.CharField(max_length=255)
    resume_url = models.URLField()

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications_sent"
    )
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications_received"
    )

    def __str__(self):
        return f"{self.name} -> {self.employer}"
