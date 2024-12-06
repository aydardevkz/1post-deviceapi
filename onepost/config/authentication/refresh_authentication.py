import time
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.auth_service.token.token_handler import TokenHandler
from firebase.config import FIREBASE_AUTH
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRefreshAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("--custom_refresh_authentication--")
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        user_id = request.META.get('user_id', None)
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return None
        token = auth_header[1]
        if user_id is None:
            raise AuthenticationFailed('user_id is None.')
        try:
            decoded_token = TokenHandler(
                user_id=user_id
            ).verify_refresh_token(token)
            user = FIREBASE_AUTH.get_user(decoded_token['uid'])
            print("user:", user)
            return user, None
        except Exception as e:
            print("e:", e)
            raise AuthenticationFailed('Invalid token.')

    def authenticate_header(self, request):
        return 'Bearer'
