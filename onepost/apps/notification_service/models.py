import uuid
from django.db import models


class SystemNotification(models.Model):
    PUBLISH_STATUS = (
        (1, "Draft"),
        (2, "Published"),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    title = models.TextField(db_index=True, verbose_name="title", max_length=500)
    content = models.TextField(verbose_name="content", max_length=5000)
    image = models.URLField(verbose_name="image", max_length=500, null=True, blank=True)
    link = models.URLField(verbose_name="link", max_length=500, null=True, blank=True)
    publish_status = models.SmallIntegerField(db_index=True, default=1, choices=PUBLISH_STATUS,
                                              verbose_name="publish_status")
    created_by = models.UUIDField(db_index=True, verbose_name="created_by", editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_system_notification'
        verbose_name = 'SystemNotification'
        verbose_name_plural = verbose_name
        app_label = 'notification_service'
        ordering = ['-created_at']
