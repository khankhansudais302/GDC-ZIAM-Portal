from django.urls import path
from . import views
urlpatterns = [
    path("dashboard/", views.principal_dashboard, name="principal_dashboard"),
    path("accounts/new/", views.account_create, name="account_create"),
    path("notices/new/", views.notice_create, name="principal_notice_create"),
    path("readmission/<int:application_id>/review/", views.readmission_review, name="readmission_review"),
]
