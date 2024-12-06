import uuid
from django.db import models
from config.settings.s3config import NewsMediaStorage


class AppCountry(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    country_name_kk = models.CharField(max_length=250, verbose_name="country_name", unique=True)
    country_name_en = models.CharField(max_length=250, verbose_name="country_name_en", unique=True)
    country_name_ru = models.CharField(max_length=250, verbose_name="country_name_ru", unique=True)
    country_code = models.CharField(max_length=80, verbose_name="country_code", unique=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_app_country'
        verbose_name = 'AppCountry'
        verbose_name_plural = verbose_name
        app_label = 'app_service'
        ordering = ['-created_at']


class AppArea(models.Model):
    AREA_TYPE = (
        (1, 'province'),
        (2, 'city'),
        (3, 'district'),
    )
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)

    area_name_kk = models.CharField(max_length=250, verbose_name="area_name_kz")
    area_name_en = models.CharField(max_length=250, verbose_name="area_name_en")
    area_name_ru = models.CharField(max_length=250, verbose_name="area_name_ru")

    area_code = models.CharField(db_index=True, max_length=80, verbose_name="area_code", unique=True)
    area_type = models.SmallIntegerField(choices=AREA_TYPE, verbose_name="category_type")
    parent_area = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="parent_area", related_name="sub_area")
    country = models.ForeignKey(AppCountry, on_delete=models.CASCADE, verbose_name="country")
    post_code = models.CharField(max_length=80, verbose_name="post_code", null=True, blank=True)
    latitude = models.FloatField(verbose_name='station_latitude', null=True, blank=True)
    longitude = models.FloatField(verbose_name='station_longitude', null=True, blank=True)
    zoom = models.FloatField(verbose_name='zoom', null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_app_area'
        verbose_name = 'AppArea'
        verbose_name_plural = verbose_name
        app_label = 'app_service'
        ordering = ['-created_at']


class AppValuta(models.Model):
    VALUTA_TYPE = (
        ("USD", "USD"),
        ("RUB", "RUB"),
        ("KZT", "KZT"),
        ("CNY", "CNY"),
    )

    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    valuta_type = models.CharField(max_length=80, choices=VALUTA_TYPE, verbose_name="valuta_type")
    valuta_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="valuta_rate")
    create_by = models.UUIDField(db_index=True, verbose_name="create_by")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_app_valuta'
        verbose_name = 'AppValuta'
        verbose_name_plural = verbose_name
        app_label = 'app_service'
        ordering = ['-created_at']


class AppBanner(models.Model):
    BANNER_TYPE = (
        (1, "Photo"),
        (2, "News"),
    )
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    title = models.TextField(db_index=True, verbose_name="title", max_length=500)
    description = models.TextField(verbose_name="description", max_length=5000)
    image = models.ImageField(verbose_name="image", upload_to="avatar", storage=NewsMediaStorage())
    banner_type = models.SmallIntegerField(choices=BANNER_TYPE, verbose_name="banner_type")
    create_by = models.UUIDField(db_index=True, verbose_name="create_by")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_app_banner'
        verbose_name = 'AppBanner'
        verbose_name_plural = verbose_name
        app_label = 'app_service'
        ordering = ['-created_at']


class AppNews(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="id", unique=True, default=uuid.uuid4)
    title = models.TextField(db_index=True, verbose_name="title", max_length=500)
    description = models.TextField(verbose_name="description", max_length=5000)
    image = models.ImageField(verbose_name="image", upload_to="avatar", storage=NewsMediaStorage())
    source_link = models.URLField(verbose_name="source_link", null=True, blank=True)
    create_by = models.UUIDField(db_index=True, verbose_name="create_by")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created_at")

    class Meta:
        db_table = 'mdl_app_news'
        verbose_name = 'AppNews'
        verbose_name_plural = verbose_name
        app_label = 'app_service'
        ordering = ['-created_at']


