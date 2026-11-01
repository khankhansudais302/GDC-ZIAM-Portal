from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, StudentProfile, Complaint, ReAdmissionApplication, Notice

class LoginForm(forms.Form):
    login_id = forms.CharField(label="Roll number / Staff ID", max_length=150, widget=forms.TextInput(attrs={"autocomplete": "username", "placeholder": "Your roll number or staff ID"}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Password"}))

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["title", "message", "visibility"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5, "placeholder": "Explain the issue clearly. Please do not include passwords."})}

class ReAdmissionForm(forms.ModelForm):
    class Meta:
        model = ReAdmissionApplication
        fields = ["current_year", "reason"]
        widgets = {"reason": forms.Textarea(attrs={"rows": 5, "placeholder": "Explain the reason for requesting re-admission."})}

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ["title", "body", "audience"]
        widgets = {"body": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.role == User.Role.TEACHER:
            self.fields["audience"].choices = [
                (Notice.Audience.ALL, "All users"),
                (Notice.Audience.STUDENTS, "Students"),
            ]

class AccountCreateForm(forms.Form):
    ROLE_CHOICES = [(User.Role.STUDENT, "Student"), (User.Role.TEACHER, "Teacher")]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Account type")
    username = forms.CharField(max_length=150, label="Roll number / Staff ID")
    full_name = forms.CharField(max_length=150, label="Full name")
    password = forms.CharField(widget=forms.PasswordInput, label="Temporary password", help_text="Use at least 10 characters; tell the user to change it when possible.")
    year = forms.ChoiceField(choices=StudentProfile.Year.choices, required=False, label="Student year")
    group = forms.ChoiceField(choices=StudentProfile.Group.choices, required=False, label="Student group")
    subjects = forms.CharField(max_length=250, required=False, label="Teacher subjects", help_text="Only for a teacher, e.g. Mathematics, Physics")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("That login ID already exists.")
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("role") == User.Role.STUDENT:
            if not cleaned.get("year") or not cleaned.get("group"):
                raise ValidationError("For a student account, choose year and group.")
        if cleaned.get("role") == User.Role.TEACHER and not cleaned.get("subjects"):
            cleaned["subjects"] = "To be confirmed"
        return cleaned

    def save(self, created_by):
        role = self.cleaned_data["role"]
        full_name = self.cleaned_data["full_name"].strip()
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            role=role,
            first_name=full_name,
            is_staff=False,
        )
        if role == User.Role.STUDENT:
            profile = user.student_profile
            profile.roll_number = user.username
            profile.year = self.cleaned_data["year"]
            profile.group = self.cleaned_data["group"]
            profile.save()
        elif role == User.Role.TEACHER:
            profile = user.teacher_profile
            profile.subjects = self.cleaned_data.get("subjects", "")
            profile.save()
        return user

class ReAdmissionReviewForm(forms.ModelForm):
    class Meta:
        model = ReAdmissionApplication
        fields = ["status", "review_note"]
        widgets = {"review_note": forms.Textarea(attrs={"rows": 3})}
