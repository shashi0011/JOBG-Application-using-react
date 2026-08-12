from django.urls import path
from .views import (
    GetAllJobsView, PostJobView, GetMyJobsView,
    UpdateJobView, DeleteJobView, GetSingleJobView,
)

urlpatterns = [
    path("getall", GetAllJobsView.as_view()),
    path("post", PostJobView.as_view()),
    path("getmyjobs", GetMyJobsView.as_view()),
    path("update/<int:id>", UpdateJobView.as_view()),
    path("delete/<int:id>", DeleteJobView.as_view()),
    path("<int:id>", GetSingleJobView.as_view()),
]
