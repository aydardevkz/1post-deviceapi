import uuid
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from config.settings.base import VERIFICATION_CODE_LIFE_SPAN



class VerificationCode(models.Model):
    VERIFICATION_CODE_TYPE = (
        ('login', 'login'),
        ('password_reset', 'password_reset'),
        ('phone_change', 'phone_change'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(db_index=True, max_length=20, verbose_name="phone")
    country_code = models.CharField(max_length=20, verbose_name="country_code")
    code_type = models.CharField(max_length=255, choices=VERIFICATION_CODE_TYPE, verbose_name="code_type")
    is_used = models.BooleanField(default=False, verbose_name="is_used")
    verification_code = models.CharField(db_index=True, max_length=20, verbose_name="verification_code")
    expires_at = models.DateTimeField(db_index=True, null=True, blank=True, verbose_name="expires_at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_auth_verification_code'
        verbose_name = 'VerificationCode'
        verbose_name_plural = verbose_name
        app_label = 'auth_service'

    def save(self, *args, expires_in=None, **kwargs):
        if not self.expires_at:
            if expires_in is not None:
                self.expires_at = timezone.now() + timedelta(minutes=expires_in)
            else:
                # expiration_minutes = settings.VERIFICATION_CODE_EXPIRATION_TIMES.get(self.code_type, 5)
                expiration_minutes = VERIFICATION_CODE_LIFE_SPAN
                self.expires_at = timezone.now() + timedelta(minutes=expiration_minutes)
        super().save(*args, **kwargs)


    def is_expired(self):
        return timezone.now() > self.expires_at

    def check_max_attempt(self):
        count = VerificationCode.objects.filter(
            phone=self.phone, is_used=False,
            created_at__gte=datetime.now() - timedelta(minutes=VERIFICATION_CODE_LIFE_SPAN)
        )
        if count >= 3:
            return True
        return False

    def set_used(self):
        self.is_used = True
        self.save()


class TokenBlacklist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(verbose_name="user_id")
    jti = models.CharField(max_length=255, verbose_name="jti")
    active = models.BooleanField(default=True, verbose_name="active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_auth_token_blacklist'
        verbose_name = 'TokenBlacklist'
        verbose_name_plural = verbose_name
        app_label = 'auth_service'
        unique_together = (('user_id', 'jti'),)
        ordering = ['-created_at']
