#  user_service/models.py
import string
import uuid
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from config.settings.s3config import AccountMediaStorage



class UserBase(AbstractBaseUser):
    GENDER_TYPE = (
        (1, "secret"),
        (2, "male"),
        (3, "female"),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    first_name = models.CharField(max_length=128, verbose_name='first_name', null=True, blank=True)
    last_name = models.CharField(max_length=128, verbose_name='last_name', null=True, blank=True)
    firebase_id = models.CharField(max_length=128, verbose_name='user_code', unique=True, null=True, blank=True)
    phone = models.CharField(db_index=True, max_length=20, verbose_name="phone", unique=True)
    email = models.EmailField(db_index=True, max_length=255, verbose_name="email", null=True, blank=True)
    birthday = models.DateField(verbose_name="birthday", null=True, blank=True, default="2000-01-01")
    avatar = models.ImageField(verbose_name="avatar",  upload_to="avatar/%Y/%m/%d", storage=AccountMediaStorage(), null=True, blank=True)
    gender = models.SmallIntegerField(default=1, choices=GENDER_TYPE, verbose_name="gender")
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    status = models.BooleanField(default=True, verbose_name="status")
    is_deleted = models.BooleanField(default=False, verbose_name="is_deleted")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='created_at')
    USERNAME_FIELD = 'phone'
    _original_avatar = None

    class Meta:
        db_table = 'mdl_user_base'
        verbose_name = 'Users'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        ordering = ("-created_at",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_avatar = self.avatar

    def update_avatar(self, avatar_file):
        self.avatar = avatar_file
        self.save(update_fields=["avatar"])

    def set_custom_password(self, password):
        self.set_password(password)
        self.save(update_fields=["password"])

    def save(self, *args, **kwargs):
        if not self.firebase_id:
            self.firebase_id = str(uuid.uuid4())
        super(UserBase, self).save(*args, **kwargs)
        if self.pk and self._original_avatar != self.avatar:
            self._original_avatar.delete(save=False)
        self._original_avatar = self.avatar

    def delete(self, *args, **kwargs):
        if self.avatar:
            self.avatar.delete(save=False)
        super().delete(*args, **kwargs)


class Users(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.PROTECT, primary_key=True, verbose_name="user", related_name="user")
    idn = models.CharField(max_length=30, verbose_name='idn', null=True, blank=True)
    is_identity_verified = models.BooleanField(default=False, verbose_name="is_identity_verified")
    is_address_verified = models.BooleanField(default=False, verbose_name="is_address_verified")
    is_station_verified = models.BooleanField(default=False, verbose_name="is_station_verified")

    class Meta:
        db_table = 'mdl_user_users'
        app_label = 'user_service'
        verbose_name = 'Users'
        verbose_name_plural = verbose_name
        ordering = ("-user__created_at",)


class BaseAdmin(models.Model):
    BASE_ADMIN_ROLE = (
        ("SUPER_ADMIN", "super_admin"),
        ("BASE_ORGANIZATION_OWNER", "base_organization_owner"),
        ("BASE_ORGANIZATION_STAFF", "base_organization_staff"),
        ("THIRD_PARTY_APP", "third_party_app"),
    )
    user = models.OneToOneField(UserBase, on_delete=models.PROTECT, primary_key=True, verbose_name="user",
                                related_name="base_admin")
    role = models.CharField(max_length=50, choices=BASE_ADMIN_ROLE, verbose_name="role")

    class Meta:
        db_table = 'mdl_user_base_admin'
        verbose_name = 'BaseAdmin'
        verbose_name_plural = verbose_name
        app_label = 'user_service'


class Admin(models.Model):
    ADMIN_ROLE = (
        ("ORGANIZATION_OWNER", "organization_owner"),
        ("ORGANIZATION_STAFF", "organization_staff"),
        ("WAREHOUSE_OWNER", "warehouse_owner"),
        ("WAREHOUSE_STAFF", "warehouse_staff"),
        ("STAFF", "staff"),
        ("DRIVER", "driver"),
    )
    avatar = models.ImageField(verbose_name="avatar", upload_to="avatar", storage=AccountMediaStorage(),
                               default="default-user.jpg")
    xid = models.CharField(unique=True,  max_length=20, verbose_name="xid", null=True, blank=True)
    user = models.OneToOneField(UserBase, on_delete=models.PROTECT, primary_key=True, verbose_name="user", related_name="admin")
    role = models.CharField(max_length=20, choices=ADMIN_ROLE, verbose_name="role")

    class Meta:
        db_table = 'mdl_user_admin'
        verbose_name = 'Admin'
        verbose_name_plural = verbose_name
        app_label = 'user_service'


class BaseOrganization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    organization_name = models.CharField(max_length=128, verbose_name='organization_name')
    organization_code = models.CharField(max_length=128, verbose_name='organization_code', unique=True)
    organization_tel = models.CharField(max_length=20, verbose_name='organization_tel', null=True, blank=True)
    organization_owner = models.ForeignKey(BaseAdmin, on_delete=models.PROTECT, verbose_name='organization_owner')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_base_organization'
        verbose_name = 'BaseOrganization'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        ordering = ("-created_at",)


class ThirdPartyApp(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    appid = models.CharField(max_length=128, verbose_name='appid', unique=True)
    app_secret = models.CharField(max_length=128, verbose_name='app_secret')
    name = models.CharField(max_length=128, verbose_name='name')
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    user = models.OneToOneField(BaseAdmin, on_delete=models.PROTECT, verbose_name='user', related_name='third_party_app')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_third_party_app'
        verbose_name = 'ThirdPartyApp'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        ordering = ("-created_at",)


class ReceivingStation(models.Model):
    STATION_TYPE = (
        (1, 'other'),
        (2, 'station'),
        (3, 'warehouse'),
        (4, 'office'),
        (5, 'market'),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    station_name = models.CharField(max_length=128, verbose_name='station_name')
    extra_station_name = models.CharField(max_length=128, verbose_name='extra_station_name', null=True, blank=True)
    station_code = models.CharField(max_length=128, verbose_name='station_code', unique=True)
    extra_code = models.CharField(max_length=128, verbose_name='extra_code', null=True, blank=True)
    station_tel = models.CharField(max_length=20, verbose_name='station_tel', null=True, blank=True)
    station_area = models.UUIDField(db_index=True, verbose_name='station_area', null=True, blank=True)
    station_region = models.UUIDField(db_index=True, verbose_name='station_region', null=True, blank=True)
    station_address = models.JSONField(verbose_name='station_address', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='station_latitude', null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='station_longitude', null=True, blank=True)
    station_type = models.SmallIntegerField(db_index=True, choices=STATION_TYPE, verbose_name='station_type', default=1)
    is_active = models.BooleanField(db_index=True, default=True, verbose_name="is_active")
    is_deleted = models.BooleanField(db_index=True, default=False, verbose_name="is_deleted")
    station_owner = models.ForeignKey(Admin, on_delete=models.PROTECT, verbose_name='station_owner')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_receiving_station'
        verbose_name = 'ReceivingStation'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        unique_together = ('station_code', 'extra_code')
        ordering = ("-created_at",)


class StationWorkTime(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    station = models.ForeignKey(ReceivingStation, on_delete=models.CASCADE, verbose_name='station', related_name='work_times')
    week_days = models.JSONField(verbose_name='week_days')
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_station_work_time'
        verbose_name = 'StationWorkTime'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        ordering = ("-created_at",)


class ReceivingStationStaff(models.Model):
    STAFF_TYPE = (
        (1, 'staff'),
        (2, 'driver'),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    user = models.OneToOneField(Admin, on_delete=models.DO_NOTHING, verbose_name="user", related_name="staff")
    station = models.ForeignKey(ReceivingStation, on_delete=models.PROTECT, verbose_name='station', null=True, blank=True)
    staff_type = models.SmallIntegerField(default=1, choices=STAFF_TYPE, verbose_name="staff_type")
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_receiving_station_staff'
        verbose_name = 'ReceivingStationStaff'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        ordering = ("-created_at",)


class WarehouseOrganization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    warehouse_name = models.CharField(max_length=128, verbose_name='warehouse_name')
    warehouse_code = models.CharField(max_length=128, verbose_name='warehouse_code', unique=True)
    warehouse_tel = models.CharField(max_length=20, verbose_name='station_tel', null=True, blank=True)
    warehouse_area = models.UUIDField(db_index=True, verbose_name='station_area', null=True, blank=True)
    warehouse_region = models.UUIDField(db_index=True, verbose_name='station_region', null=True, blank=True)
    warehouse_address = models.JSONField(verbose_name='warehouse_address', null=True, blank=True)
    latitude = models.FloatField(verbose_name='station_latitude', null=True, blank=True)
    longitude = models.FloatField(verbose_name='station_longitude', null=True, blank=True)
    is_active = models.BooleanField(db_index=True, default=True, verbose_name="is_active")
    is_deleted = models.BooleanField(db_index=True, default=False, verbose_name="is_deleted")
    warehouse_owner = models.ForeignKey(Admin, on_delete=models.PROTECT, verbose_name='warehouse_owner')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_warehouse_organization'
        verbose_name = 'WarehouseOrganization'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        unique_together = ('warehouse_code',)
        ordering = ("-created_at",)


class WarehouseOrganizationStaff(models.Model):
    STAFF_TYPE = (
        (1, 'staff'),
        (2, 'driver'),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    user = models.OneToOneField(Admin, on_delete=models.PROTECT, verbose_name="user", related_name="warehouse_staff")
    organization = models.ForeignKey(WarehouseOrganization, on_delete=models.PROTECT, verbose_name="organization")
    staff_type = models.SmallIntegerField(default=1, choices=STAFF_TYPE, verbose_name="staff_type")
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_warehouse_organization_staff'
        verbose_name = 'WarehouseOrganizationStaff'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        ordering = ("-created_at",)


class MyReceivingStation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    user = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='user')
    station = models.ForeignKey(ReceivingStation, on_delete=models.PROTECT, verbose_name='station')
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_my_receiving_station'
        verbose_name = 'MyReceivingStation'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        unique_together = ('user', 'station')


class UserThirdPartyApp(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    user = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='user')
    user_code = models.CharField(max_length=128, verbose_name='user_code', null=True, blank=True)
    third_party_app = models.ForeignKey(ThirdPartyApp, on_delete=models.PROTECT, verbose_name='third_party_app')
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_user_third_party_app'
        verbose_name = 'UserThirdPartyApp'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        unique_together = [
            ('user', 'third_party_app'),
            ('user_code', 'third_party_app')
        ]


class ThirdPartyAppWarehouseAddress(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    third_party_app = models.ForeignKey(ThirdPartyApp, on_delete=models.PROTECT, verbose_name='third_party_app',
                                        related_name='warehouse_address')
    warehouse_name = models.CharField(max_length=128, verbose_name='warehouse_name')
    warehouse_contact = models.CharField(max_length=128, verbose_name='warehouse_contact')
    warehouse_tel = models.CharField(max_length=20, verbose_name='warehouse_tel')
    warehouse_address = models.CharField(max_length=128, verbose_name='warehouse_address')

    is_active = models.BooleanField(db_index=True, default=True, verbose_name="is_active")
    is_deleted = models.BooleanField(db_index=True, default=False, verbose_name="is_deleted")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_user_third_party_app_warehouse_address'
        verbose_name = 'ThirdPartyAppWarehouseAddress'
        verbose_name_plural = verbose_name
        app_label = 'user_service'
        ordering = ("-created_at",)
