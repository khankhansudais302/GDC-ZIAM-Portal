from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import User, StudentProfile, TeacherProfile, Notice, Complaint, ReAdmissionApplication

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "first_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (("GDC ZIAM access", {"fields": ("role",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (("GDC ZIAM access", {"fields": ("role", "first_name", "email")} ,),)

admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "is_active", "created_by", "created_at")
    list_filter = ("audience", "is_active")
    search_fields = ("title", "body")

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "visibility", "status", "created_at")
    list_filter = ("visibility", "status")
    search_fields = ("title", "message", "student__username")
    readonly_fields = ("student", "title", "message", "visibility", "created_at", "updated_at")

@admin.register(ReAdmissionApplication)
class ReAdmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "current_year", "fee_amount", "status", "created_at")
    list_filter = ("status", "current_year")
    search_fields = ("student__username", "reason")
    readonly_fields = ("student", "current_year", "reason", "fee_amount", "created_at")

    def save_model(self, request, obj, form, change):
        if change and "status" in form.changed_data:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
