# Initial database migration for GDC ZIAM Secure Portal.
# Generated for the project models in portal/models.py.
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import portal.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", verbose_name="superuser status")),
                ("username", models.CharField(error_messages={"unique": "A user with that username already exists."}, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name="username")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                ("is_staff", models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.", verbose_name="staff status")),
                ("is_active", models.BooleanField(default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.", verbose_name="active")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("role", models.CharField(choices=[("student", "Student"), ("teacher", "Teacher"), ("principal", "Principal / Admin")], default="student", max_length=12)),
                ("groups", models.ManyToManyField(blank=True, help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.", related_name="user_set", related_query_name="user", to="auth.group", verbose_name="groups")),
                ("user_permissions", models.ManyToManyField(blank=True, help_text="Specific permissions for this user.", related_name="user_set", related_query_name="user", to="auth.permission", verbose_name="user permissions")),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users"},
            managers=[("objects", portal.managers.PortalUserManager())],
        ),
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("roll_number", models.CharField(max_length=40, unique=True)),
                ("year", models.CharField(choices=[("first_year", "First Year (Class 11)"), ("second_year", "Second Year (Class 12)")], default="first_year", max_length=12)),
                ("group", models.CharField(choices=[("medical", "Medical"), ("engineering", "Engineering"), ("computer_science", "Computer Science"), ("arts", "Arts")], default="computer_science", max_length=24)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="student_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TeacherProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subjects", models.CharField(blank=True, help_text="Subjects this teacher teaches", max_length=250)),
                ("assigned_groups", models.CharField(blank=True, max_length=250)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="teacher_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Notice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("body", models.TextField()),
                ("audience", models.CharField(choices=[("all", "All users"), ("students", "Students"), ("staff", "Teachers and principal")], default="all", max_length=12)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="notices_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Complaint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("message", models.TextField()),
                ("visibility", models.CharField(choices=[("general", "General complaint (teachers and principal)"), ("principal_only", "Only principal and student")], default="general", max_length=20)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("in_review", "In review"), ("resolved", "Resolved")], default="pending", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="complaints", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ReAdmissionApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("current_year", models.CharField(choices=[("first_year", "First Year (Class 11)"), ("second_year", "Second Year (Class 12)")], max_length=12)),
                ("reason", models.TextField()),
                ("fee_amount", models.PositiveIntegerField(default=700)),
                ("status", models.CharField(choices=[("pending", "Pending review"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=12)),
                ("review_note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("reviewed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="readmissions_reviewed", to=settings.AUTH_USER_MODEL)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="readmission_applications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
