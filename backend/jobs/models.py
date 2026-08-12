from django.db import models
from django.conf import settings


class Job(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location = models.TextField()
    fixed_salary = models.IntegerField(null=True, blank=True)
    salary_from = models.IntegerField(null=True, blank=True)
    salary_to = models.IntegerField(null=True, blank=True)
    expired = models.BooleanField(default=False)
    job_posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs_posted"
    )

    def __str__(self):
        return self.title
