from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied("Your account does not have permission to open this page.")
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
