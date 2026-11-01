from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import PortalUserManager

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"
        PRINCIPAL = "principal", "Principal / Admin"

    role = models.CharField(max_length=12, choices=Role.choices, default=Role.STUDENT)
    objects = PortalUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

class StudentProfile(models.Model):
    class Year(models.TextChoices):
        FIRST = "first_year", "First Year (Class 11)"
        SECOND = "second_year", "Second Year (Class 12)"
    class Group(models.TextChoices):
        MEDICAL = "medical", "Medical"
        ENGINEERING = "engineering", "Engineering"
        COMPUTER_SCIENCE = "computer_science", "Computer Science"
        ARTS = "arts", "Arts"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    roll_number = models.CharField(max_length=40, unique=True)
    year = models.CharField(max_length=12, choices=Year.choices, default=Year.FIRST)
    group = models.CharField(max_length=24, choices=Group.choices, default=Group.COMPUTER_SCIENCE)

    def __str__(self):
        return f"{self.roll_number} — {self.get_year_display()} / {self.get_group_display()}"

class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    subjects = models.CharField(max_length=250, blank=True, help_text="Subjects this teacher teaches")
    assigned_groups = models.CharField(max_length=250, blank=True, help_text="Groups this teacher is assigned to")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Notice(models.Model):
    class Audience(models.TextChoices):
        ALL = "all", "All users"
        STUDENTS = "students", "Students"
        STAFF = "staff", "Teachers and principal"
    title = models.CharField(max_length=180)
    body = models.TextField()
    audience = models.CharField(max_length=12, choices=Audience.choices, default=Audience.ALL)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notices_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Complaint(models.Model):
    class Visibility(models.TextChoices):
        GENERAL = "general", "General complaint (teachers and principal)"
        PRINCIPAL_ONLY = "principal_only", "Only principal and student"
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_REVIEW = "in_review", "In review"
        RESOLVED = "resolved", "Resolved"
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="complaints")
    title = models.CharField(max_length=180)
    message = models.TextField()
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.GENERAL)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.student.username}"

class ReAdmissionApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="readmission_applications")
    current_year = models.CharField(max_length=12, choices=StudentProfile.Year.choices)
    reason = models.TextField()
    fee_amount = models.PositiveIntegerField(default=700)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    review_note = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="readmissions_reviewed")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Re-admission — {self.student.username} ({self.get_status_display()})"
