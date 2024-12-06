import uuid
from django.db import models
from config.settings.s3config import OpenOrderStorage



class OpenAppDeviceModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    device_name = models.CharField(max_length=50, db_index=True, verbose_name="device_name")
    app_id = models.CharField(max_length=50, db_index=True, verbose_name="app_id", unique=True)
    app_secret = models.CharField(max_length=50, verbose_name="app_secret")
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    organization_id = models.UUIDField(db_index=True, verbose_name="organization_id")
    created_by = models.UUIDField(db_index=True, verbose_name="created_by")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_open_app_device_model'
        verbose_name = 'Open App Device'
        verbose_name_plural = verbose_name
        app_label = 'open_service'
        ordering = ['-created_at']


class OpenOrderDeviceModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    order_no = models.CharField(max_length=50, db_index=True, verbose_name="order_no")
    order_image = models.ImageField(upload_to='open_device_order/%Y/%m/%d', storage=OpenOrderStorage(), verbose_name="order_image")
    user_code = models.CharField(max_length=50, db_index=True, verbose_name="user_code")
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="total_weight")
    weight_unit = models.CharField(max_length=10, verbose_name="weight_unit", default='kg')
    device = models.ForeignKey(OpenAppDeviceModel, on_delete=models.CASCADE, verbose_name="device")
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_open_order_device_model'
        verbose_name = 'Open Order Device'
        verbose_name_plural = verbose_name
        app_label = 'open_service'
        ordering = ['-created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._order_image= self.order_image

    def save(self, *args, **kwargs):

        super(OpenOrderDeviceModel, self).save(*args, **kwargs)
        if self.pk and self._order_image != self.order_image:
            self._order_image.delete(save=False)
        self._order_image = self.order_image

    def delete(self, *args, **kwargs):
        if self.order_image:
            self.order_image.delete(save=False)
        super().delete(*args, **kwargs)


class OpenOrderTaskModel(models.Model):
    TASK_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    TASK_TYPE = (
        ("INITIAL", "Initial"),
        ("RETRY", "Retry"),
    )


    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    task_name = models.CharField(max_length=50, db_index=True, verbose_name="task_name")
    task_no = models.CharField(max_length=50, db_index=True, verbose_name="task_no")
    device = models.ForeignKey(OpenAppDeviceModel, on_delete=models.CASCADE, verbose_name="device")
    start_time = models.DateTimeField(verbose_name="start_time")
    end_time = models.DateTimeField(verbose_name="end_time")
    status = models.CharField(max_length=50, verbose_name="status", choices=TASK_STATUS, default='pending')
    task_type = models.CharField(max_length=50, verbose_name="task_type", choices=TASK_TYPE, default='INITIAL')
    created_by = models.UUIDField(db_index=True, verbose_name="created_by")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_open_order_task'
        verbose_name = 'Open Order Task'
        verbose_name_plural = verbose_name
        app_label = 'open_service'
        ordering = ['-created_at']


class OpenDeviceOrderStatusModel(models.Model):
    SEND_STATUS = (
        ('initial', 'Initial'),
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    order = models.ForeignKey(OpenOrderDeviceModel, on_delete=models.CASCADE, verbose_name="order")
    status = models.CharField(max_length=50, verbose_name="status", choices=SEND_STATUS, default='initial')
    station_id = models.UUIDField(db_index=True, verbose_name="station_id", null=True, blank=True)
    user_id = models.UUIDField(db_index=True, verbose_name="user_id", null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name="phone", null=True, blank=True)
    full_address = models.CharField(max_length=255, verbose_name="full_address", null=True, blank=True)
    user_code = models.CharField(max_length=50, db_index=True, verbose_name="vip_code", null=True, blank=True)
    organization_user_id = models.UUIDField(db_index=True, verbose_name="organization_user_id", null=True, blank=True)
    updated_by = models.UUIDField(db_index=True, verbose_name="created_by", null=True, blank=True)
    send_by = models.UUIDField(db_index=True, verbose_name="send_by", null=True, blank=True)
    is_sent = models.BooleanField(default=False, verbose_name="is_sent")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_open_device_order_status'
        verbose_name = 'Device Order Status'
        verbose_name_plural = verbose_name
        app_label = 'open_service'
        ordering = ['-created_at']
