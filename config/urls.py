from django.contrib import admin
from django.urls import path, include
from portal import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("timetables/", views.timetables, name="timetables"),
    path("past-papers/", views.past_papers, name="past_papers"),
    path("student/", include("portal.student_urls")),
    path("teacher/", include("portal.teacher_urls")),
    path("principal/", include("portal.principal_urls")),
]
