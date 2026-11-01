from django.urls import path
from . import views
urlpatterns = [
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("complaints/new/", views.complaint_create, name="complaint_create"),
    path("readmission/new/", views.readmission_create, name="readmission_create"),
]
