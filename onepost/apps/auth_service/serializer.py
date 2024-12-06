# serializers.py
import datetime
import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.auth_service.models import VerificationCode
from config.utils.phone_validate import PhoneValidate


class PasswordVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        self.validate_std_password(attrs)
        return attrs

    def validate_std_password(self, attrs):
        """Validate password."""
        password = attrs.get('password', None)
        if password is None:
            raise ValidationError("Password is required")
            # if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$', password):
            #     raise ValidationError("Invalid password format (min 8 characters, max 20 characters, at least one number)")
            # return attrs
        return attrs


class EmailPasswordVerifySerializer(serializers.Serializer):
    email= serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        self.validate_std_password(attrs)
        return attrs

    def validate_std_password(self, attrs):
        """Validate password."""
        password = attrs.get('password', None)
        if password is None:
            raise ValidationError("Password is required")
            # if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$', password):
            #     raise ValidationError("Invalid password format (min 8 characters, max 20 characters, at least one number)")
            # return attrs
        return attrs
