from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, TeacherProfile

@receiver(post_save, sender=User)
def ensure_role_profile(sender, instance, created, **kwargs):
    # Keep role-specific profiles available. Defaults are deliberately minimal and can be edited by the principal.
    if instance.role == User.Role.STUDENT:
        StudentProfile.objects.get_or_create(
            user=instance,
            defaults={"roll_number": instance.username},
        )
        TeacherProfile.objects.filter(user=instance).delete()
    elif instance.role == User.Role.TEACHER:
        TeacherProfile.objects.get_or_create(user=instance)
        StudentProfile.objects.filter(user=instance).delete()
    else:
        StudentProfile.objects.filter(user=instance).delete()
        TeacherProfile.objects.filter(user=instance).delete()
