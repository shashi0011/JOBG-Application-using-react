from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    # Field names are mapped to camelCase / _id to match exactly what the
    # existing React frontend already expects from the Mongoose API.
    _id = serializers.IntegerField(source="id", read_only=True)
    fixedSalary = serializers.IntegerField(source="fixed_salary", required=False, allow_null=True)
    salaryFrom = serializers.IntegerField(source="salary_from", required=False, allow_null=True)
    salaryTo = serializers.IntegerField(source="salary_to", required=False, allow_null=True)
    jobPostedOn = serializers.DateTimeField(source="job_posted_on", read_only=True)
    postedBy = serializers.PrimaryKeyRelatedField(source="posted_by", read_only=True)

    class Meta:
        model = Job
        fields = [
            "_id", "title", "description", "category", "country", "city",
            "location", "fixedSalary", "salaryFrom", "salaryTo", "expired",
            "jobPostedOn", "postedBy",
        ]
