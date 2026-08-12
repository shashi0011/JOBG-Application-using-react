from django.urls import path
from .views import (
    PostApplicationView, EmployerGetAllApplicationsView,
    JobseekerGetAllApplicationsView, JobseekerDeleteApplicationView,
)

urlpatterns = [
    path("post", PostApplicationView.as_view()),
    path("employer/getall", EmployerGetAllApplicationsView.as_view()),
    path("jobseeker/getall", JobseekerGetAllApplicationsView.as_view()),
    path("delete/<int:id>", JobseekerDeleteApplicationView.as_view()),
]
