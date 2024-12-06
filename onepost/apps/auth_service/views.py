import uuid
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from apps.auth_service.serializer import *
from apps.auth_service.token.jwt_utils import JWTUtils
from django.contrib.auth import authenticate
from apps.auth_service.utils.sms_service import SMSAPI
from apps.user_service.models import UserBase, Admin
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from apps.user_service.serializers.common.user_common_serializer import AdminRetrieveSerializer
from config.settings.base import APP_VERSION



current_user = get_user_model()



class AppVersionViewSet(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {
                "version": APP_VERSION,
                "is_force": False,
                "is_update": True,
            },
            status=status.HTTP_200_OK
        )


class VerifyPhonePasswordViewSet(generics.GenericAPIView):
    serializer_class = PasswordVerifySerializer
    authentication_classes = []
    permission_classes = []

    @classmethod
    def get_tokens(cls, user):
        user_id = user.id
        phone = user.phone
        jti = uuid.uuid4().hex

        access_token = JWTUtils.generate_token(user_id=user_id, phone=phone, jti=jti, is_refresh=False)
        refresh_token = JWTUtils.generate_token(user_id=user_id, phone=phone, jti=jti, is_refresh=True)
        return access_token, refresh_token

    @classmethod
    def check_admin_instance(cls, user):
        try:
            admin = Admin.objects.get(user=user)
            if admin.user.is_deleted:
                raise ValidationError("Admin account is deactivated.")
            if not admin.user.is_active:
                raise ValidationError("Admin account is not activated.")
            return admin
        except Admin.DoesNotExist:
            raise ValidationError("Admin account does not exist.")

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone', None)
        password = serializer.validated_data.get('password', None)
        user = authenticate(request, username=phone, password=password)
        admin = self.check_admin_instance(user=user)
        if admin is None:
            raise AuthenticationFailed("Invalid phone number or password.")
        admin_data = AdminRetrieveSerializer(admin.user).data
        access_token, refresh_token = self.get_tokens(admin.user)
        return Response(
            {
                "data": admin_data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK
        )


class VerifyEmailPasswordViewSet(generics.GenericAPIView):
    serializer_class = EmailPasswordVerifySerializer
    authentication_classes = []
    permission_classes = []

    @classmethod
    def get_tokens(cls, user):
        user_id = user.id
        phone = user.phone
        jti = uuid.uuid4().hex

        access_token = JWTUtils.generate_token(user_id=user_id, phone=phone, jti=jti, is_refresh=False)
        refresh_token = JWTUtils.generate_token(user_id=user_id, phone=phone, jti=jti, is_refresh=True)
        return access_token, refresh_token

    @classmethod
    def check_admin_instance(cls, user):
        try:
            admin = Admin.objects.get(user=user)
            if admin.user.is_deleted:
                raise ValidationError("Admin account is deactivated.")
            if not admin.user.is_active:
                raise ValidationError("Admin account is not activated.")
            return admin
        except Admin.DoesNotExist:
            raise ValidationError("Admin account does not exist.")

    @classmethod
    def get_phone_by_email(cls, email):
        try:
            phone = UserBase.objects.get(email=email)
            return phone
        except UserBase.DoesNotExist:
            raise ValidationError("User does not exist.")
        except UserBase.MultipleObjectsReturned:
            raise ValidationError("Multiple users found with this email.")
        except Exception as e:
            raise ValidationError("Error occurred while fetching user data.")



    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', None)
        password = serializer.validated_data.get('password', None)
        phone = self.get_phone_by_email(email)
        user = authenticate(request, username=phone, password=password)
        admin = self.check_admin_instance(user=user)
        if admin is None:
            raise AuthenticationFailed("Invalid phone number or password.")
        admin_data = AdminRetrieveSerializer(admin.user).data
        access_token, refresh_token = self.get_tokens(admin.user)
        return Response(
            {
                "data": admin_data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK
        )


class RefreshTokenViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = []

    def post(self, request):
        user = request.user
        user_id = user.id
        phone = user.phone
        jti = uuid.uuid4().hex  # 新生成 jti

        access_token = JWTUtils.generate_token(user_id=user_id, phone=phone, jti=jti, is_refresh=False)
        refresh_token = JWTUtils.generate_token(user_id=user_id, phone=phone, jti=jti, is_refresh=True)

        return Response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK
        )
