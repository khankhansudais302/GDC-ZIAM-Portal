from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .decorators import role_required
from .forms import LoginForm, ComplaintForm, ReAdmissionForm, NoticeForm, AccountCreateForm, ReAdmissionReviewForm
from .models import User, StudentProfile, Notice, Complaint, ReAdmissionApplication


def role_home(user):
    if user.role == User.Role.STUDENT:
        return "student_dashboard"
    if user.role == User.Role.TEACHER:
        return "teacher_dashboard"
    return "principal_dashboard"


def home(request):
    notices = Notice.objects.filter(is_active=True, audience=Notice.Audience.ALL)[:3]
    return render(request, "portal/home.html", {"notices": notices})


def login_view(request):
    if request.user.is_authenticated:
        return redirect(role_home(request.user))
    form = LoginForm(request.POST or None)
    error = None
    if request.method == "POST" and form.is_valid():
        user = authenticate(request, username=form.cleaned_data["login_id"].strip(), password=form.cleaned_data["password"])
        if user is not None and user.is_active:
            login(request, user)
            return redirect(role_home(user))
        error = "Login ID ya password ghalat hai. Apne college admin se account confirm karein."
    return render(request, "portal/login.html", {"form": form, "error": error})


@login_required
def dashboard(request):
    return redirect(role_home(request.user))


def logout_view(request):
    if request.method != "POST":
        raise PermissionDenied("Logout must be submitted as a POST request.")
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


def timetables(request):
    return render(request, "portal/timetables.html")


def past_papers(request):
    return render(request, "portal/past_papers.html")


@role_required(User.Role.STUDENT)
def student_dashboard(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user, defaults={"roll_number": request.user.username})
    notices = Notice.objects.filter(is_active=True).filter(audience__in=[Notice.Audience.ALL, Notice.Audience.STUDENTS])[:8]
    complaints = request.user.complaints.all()[:10]
    applications = request.user.readmission_applications.all()[:10]
    return render(request, "portal/student_dashboard.html", {"profile": profile, "notices": notices, "complaints": complaints, "applications": applications})


@role_required(User.Role.STUDENT)
def complaint_create(request):
    form = ComplaintForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        complaint = form.save(commit=False)
        complaint.student = request.user
        complaint.save()
        messages.success(request, "Complaint submit ho gayi. Aap dashboard par status dekh sakte hain.")
        return redirect("student_dashboard")
    return render(request, "portal/form_page.html", {"form": form, "page_title": "Submit a complaint", "button_text": "Submit complaint"})


@role_required(User.Role.STUDENT)
def readmission_create(request):
    form = ReAdmissionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.student = request.user
        application.fee_amount = 700
        application.save()
        messages.success(request, "Re-admission request submit ho gayi. Rs. 700 ka fee amount record hua hai; payment method college se confirm karein.")
        return redirect("student_dashboard")
    return render(request, "portal/form_page.html", {"form": form, "page_title": "Re-admission request", "button_text": "Submit request", "notice_text": "Fee shown: Rs. 700. Payment instructions must be confirmed with college administration."})


@role_required(User.Role.TEACHER)
def teacher_dashboard(request):
    # Deliberately exclude principal-only complaints at query time, not only in the template.
    complaints = Complaint.objects.filter(visibility=Complaint.Visibility.GENERAL).select_related("student")[:30]
    notices = Notice.objects.filter(is_active=True).filter(audience__in=[Notice.Audience.ALL, Notice.Audience.STAFF, Notice.Audience.STUDENTS])[:8]
    return render(request, "portal/teacher_dashboard.html", {"complaints": complaints, "notices": notices})


@role_required(User.Role.TEACHER, User.Role.PRINCIPAL)
def notice_create(request):
    form = NoticeForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        notice = form.save(commit=False)
        notice.created_by = request.user
        # Teachers cannot publish staff-only content even if a crafted request submits it.
        if request.user.role == User.Role.TEACHER and notice.audience == Notice.Audience.STAFF:
            raise PermissionDenied("Teachers cannot publish staff-only notices.")
        notice.save()
        messages.success(request, "Notice publish ho gaya.")
        return redirect(role_home(request.user))
    return render(request, "portal/form_page.html", {"form": form, "page_title": "Create college notice", "button_text": "Publish notice"})


@role_required(User.Role.PRINCIPAL)
def principal_dashboard(request):
    complaints = Complaint.objects.select_related("student").all()[:50]
    applications = ReAdmissionApplication.objects.select_related("student", "reviewed_by").all()[:50]
    notices = Notice.objects.filter(is_active=True)[:8]
    return render(request, "portal/principal_dashboard.html", {"complaints": complaints, "applications": applications, "notices": notices})


@role_required(User.Role.PRINCIPAL)
def account_create(request):
    form = AccountCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(created_by=request.user)
        messages.success(request, f"Account created for {user.username}. Give the login ID and temporary password directly to the intended person; ask them to keep it private.")
        return redirect("account_create")
    return render(request, "portal/form_page.html", {"form": form, "page_title": "Create student or teacher account", "button_text": "Create account", "notice_text": "Only principal accounts can create student or teacher logins. This form cannot create another principal account."})


@role_required(User.Role.PRINCIPAL)
def readmission_review(request, application_id):
    application = get_object_or_404(ReAdmissionApplication, pk=application_id)
    form = ReAdmissionReviewForm(request.POST or None, instance=application)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()
        messages.success(request, "Re-admission status update ho gaya.")
        return redirect("principal_dashboard")
    return render(request, "portal/form_page.html", {"form": form, "page_title": f"Review re-admission for {application.student.username}", "button_text": "Save review"})
