from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound

from .models import Job
from .serializers import JobSerializer


class GetAllJobsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        jobs = Job.objects.filter(expired=False)
        return Response(
            {"success": True, "jobs": JobSerializer(jobs, many=True).data}, status=200
        )


class PostJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role == "Job Seeker":
            raise PermissionDenied("Job Seeker not allowed to access this resource.")

        data = request.data
        required = ["title", "description", "category", "country", "city", "location"]
        if not all(data.get(f) for f in required):
            raise ValidationError("Please provide full job details.")

        fixed_salary = data.get("fixedSalary") or None
        salary_from = data.get("salaryFrom") or None
        salary_to = data.get("salaryTo") or None

        if (not salary_from or not salary_to) and not fixed_salary:
            raise ValidationError("Please either provide fixed salary or ranged salary.")
        if salary_from and salary_to and fixed_salary:
            raise ValidationError("Cannot Enter Fixed and Ranged Salary together.")

        job = Job.objects.create(
            title=data["title"],
            description=data["description"],
            category=data["category"],
            country=data["country"],
            city=data["city"],
            location=data["location"],
            fixed_salary=fixed_salary,
            salary_from=salary_from,
            salary_to=salary_to,
            posted_by=request.user,
        )
        return Response(
            {
                "success": True,
                "message": "Job Posted Successfully!",
                "job": JobSerializer(job).data,
            },
            status=200,
        )


class GetMyJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "Job Seeker":
            raise PermissionDenied("Job Seeker not allowed to access this resource.")
        my_jobs = Job.objects.filter(posted_by=request.user)
        return Response(
            {"success": True, "myJobs": JobSerializer(my_jobs, many=True).data}, status=200
        )


class UpdateJobView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        if request.user.role == "Job Seeker":
            raise PermissionDenied("Job Seeker not allowed to access this resource.")
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            raise NotFound("OOPS! Job not found.")

        serializer = JobSerializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Job Updated!"}, status=200)


class DeleteJobView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        if request.user.role == "Job Seeker":
            raise PermissionDenied("Job Seeker not allowed to access this resource.")
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            raise NotFound("OOPS! Job not found.")
        job.delete()
        return Response({"success": True, "message": "Job Deleted!"}, status=200)


class GetSingleJobView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            job = Job.objects.get(id=id)
        except (Job.DoesNotExist, ValueError):
            raise NotFound("Job not found.")
        return Response({"success": True, "job": JobSerializer(job).data}, status=200)
