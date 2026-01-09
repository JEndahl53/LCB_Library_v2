# organizations/views/_auth.py

def is_staff_user(user):
    return user.is_authenticated and user.is_staff