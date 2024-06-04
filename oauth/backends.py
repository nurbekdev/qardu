from django.contrib.auth.backends import BaseBackend

from .models import User


class AuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, oauth=False):
        try:
            user = User.objects.get(email=email)

            if oauth or user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
