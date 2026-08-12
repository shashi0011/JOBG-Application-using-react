import cloudinary.uploader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job

ALLOWED_FORMATS = ["image/png", "image/jpeg", "image/webp"]


class PostApplicationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if request.user.role == "Employer":
            raise PermissionDenied("Employer not allowed to access this resource.")

        resume = request.FILES.get("resume")
        if not resume:
            raise ValidationError("Resume File Required!")

        if resume.content_type not in ALLOWED_FORMATS:
            raise ValidationError("Invalid file type. Please upload a PNG file.")

        data = request.data
        name = data.get("name")
        email = data.get("email")
        cover_letter = data.get("coverLetter")
        phone = data.get("phone")
        address = data.get("address")
        job_id = data.get("jobId")

        if not job_id:
            raise NotFound("Job not found!")

        try:
            job = Job.objects.get(id=job_id)
        except (Job.DoesNotExist, ValueError):
            raise NotFound("Job not found!")

        if not all([name, email, cover_letter, phone, address]):
            raise ValidationError("Please fill all fields.")

        try:
            cloudinary_response = cloudinary.uploader.upload(resume)
        except Exception:
            raise ValidationError("Failed to upload Resume to Cloudinary")

        application = Application.objects.create(
            name=name,
            email=email,
            cover_letter=cover_letter,
            phone=phone,
            address=address,
            applicant=request.user,
            employer=job.posted_by,
            resume_public_id=cloudinary_response["public_id"],
            resume_url=cloudinary_response["secure_url"],
        )
        return Response(
            {
                "success": True,
                "message": "Application Submitted!",
                "application": ApplicationSerializer(application).data,
            },
            status=200,
        )


class EmployerGetAllApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "Job Seeker":
            raise PermissionDenied("Job Seeker not allowed to access this resource.")
        applications = Application.objects.filter(employer=request.user)
        return Response(
            {"success": True, "applications": ApplicationSerializer(applications, many=True).data},
            status=200,
        )


class JobseekerGetAllApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "Employer":
            raise PermissionDenied("Employer not allowed to access this resource.")
        applications = Application.objects.filter(applicant=request.user)
        return Response(
            {"success": True, "applications": ApplicationSerializer(applications, many=True).data},
            status=200,
        )


class JobseekerDeleteApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        if request.user.role == "Employer":
            raise PermissionDenied("Employer not allowed to access this resource.")
        try:
            application = Application.objects.get(id=id)
        except Application.DoesNotExist:
            raise NotFound("Application not found!")
        application.delete()
        return Response({"success": True, "message": "Application Deleted!"}, status=200)
