from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Complaint, ReAdmissionApplication, StudentProfile

class RoleAccessTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student-101", password="VeryStrongPass!48", role=User.Role.STUDENT)
        self.teacher = User.objects.create_user(username="teacher-11", password="VeryStrongPass!48", role=User.Role.TEACHER)
        self.principal = User.objects.create_superuser(username="principal-admin", password="VeryStrongPass!48")
        StudentProfile.objects.filter(user=self.student).update(roll_number="student-101")

    def test_student_cannot_open_teacher_dashboard(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_open_principal_dashboard(self):
        self.client.force_login(self.teacher)
        response = self.client.get(reverse("principal_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_teacher_does_not_see_principal_only_complaint(self):
        Complaint.objects.create(student=self.student, title="Private", message="private body", visibility=Complaint.Visibility.PRINCIPAL_ONLY)
        Complaint.objects.create(student=self.student, title="General", message="general body", visibility=Complaint.Visibility.GENERAL)
        self.client.force_login(self.teacher)
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertContains(response, "General")
        self.assertNotContains(response, "private body")

    def test_student_only_sees_own_complaints(self):
        other = User.objects.create_user(username="student-202", password="VeryStrongPass!48", role=User.Role.STUDENT)
        Complaint.objects.create(student=self.student, title="Mine", message="my complaint")
        Complaint.objects.create(student=other, title="Not mine", message="other complaint")
        self.client.force_login(self.student)
        response = self.client.get(reverse("student_dashboard"))
        self.assertContains(response, "Mine")
        self.assertNotContains(response, "other complaint")
