from functools import wraps
from flask import abort
from flask_login import current_user

# Forbidden error for Non admin users


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function
