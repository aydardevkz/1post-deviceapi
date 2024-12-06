from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class PhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        phone = kwargs.get("phone") or username
        # print("backend-------------------phone", phone)
        if not phone or not password:
            return None
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

        if check_password(password, user.password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
