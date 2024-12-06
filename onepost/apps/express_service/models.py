import uuid
from django.db import models


class ExpressOrder(models.Model):
    MARKET_COMPANY_CHOICES = (
        ("UNKNOWN", "Unknown"),
        ("PINDODO", "Pindodo"),
        ("TEMU", "Temu"),
        ("TAOBAO", "Taobao"),
        ("TMALL", "Tmall"),
        ("JD", "JD"),
        ("1688", "1688"),
        ("DEWU", "Dewu"),
        ("OTHER", "Other"),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    order_no = models.CharField(db_index=True, max_length=50, verbose_name="order no", unique=True)
    extra_no = models.CharField(db_index=True, max_length=50, verbose_name="extra no", null=True, blank=True)
    market_company = models.CharField(max_length=20, choices=MARKET_COMPANY_CHOICES, default="UNKNOWN",
                                      verbose_name="market company")

    full_address = models.TextField(verbose_name="full address", max_length=2200)
    contact_phone = models.CharField(max_length=20, verbose_name="contact phone")

    order_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="order price", default=0),
    price_currency = models.CharField(max_length=10, verbose_name="price currency", default="USD")

    total_weight = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="total weight", default=0)
    weight_unit = models.CharField(max_length=3, verbose_name="weight unit", default="kg")

    amount = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="amount", default=0)
    amount_currency = models.CharField(max_length=10, verbose_name="amount currency", default="KZT")

    user = models.UUIDField(db_index=True, verbose_name="user", null=True, blank=True)
    station = models.UUIDField(db_index=True, verbose_name="station", null=True, blank=True)

    is_payed = models.BooleanField(default=False, verbose_name="is payed")
    is_deleted = models.BooleanField(default=False, verbose_name="is deleted")
    is_user_deleted = models.BooleanField(default=False, verbose_name="is user deleted")
    created_by = models.UUIDField(db_index=True, verbose_name="created by", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created at")

    class Meta:
        verbose_name = "express order"
        verbose_name_plural = "express orders"
        db_table = "mdl_express_order"
        app_label = "express_service"
        ordering = ["-created_at"]


class ExpressOrderStatus(models.Model):
    ORDER_TYPE_CHOICES = (
        ("UNKNOWN", "Unknown"),
        ("WAITING", "Waiting"),
        ("IN_WAREHOUSE", "In warehouse"),
        ("ON_THE_WAY", "On the way"),
        ("AT_THE_BORDER", "At the border"),
        ("ERROR_AT_THE_BORDER", "Error at the border"),
        ("SORTED", "Sorted"),
        ("DELIVERED", "Delivered"),
        ("IN_DEPARTMENT", "In department"),
        ("IS_SHELF", "Is shelf"),
        ("CANCELLED", "Cancelled"),
        ("TAKEN", "Taken"),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    order = models.OneToOneField(ExpressOrder, on_delete=models.PROTECT, verbose_name="order", related_name="order_status")
    status_type = models.CharField(db_index=True, max_length=20, choices=ORDER_TYPE_CHOICES, verbose_name="order type")
    created_by = models.UUIDField(db_index=True, verbose_name="created by")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created at")

    class Meta:
        verbose_name = "express order status"
        verbose_name_plural = "express order statuses"
        db_table = "mdl_express_order_status"
        app_label = "express_service"
        unique_together = ("order", "status_type")
        index_together = ("status_type", "created_at")
        ordering = ("-created_at",)


class ExpressOrderStatusHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    order = models.ForeignKey(ExpressOrder, on_delete=models.CASCADE, verbose_name="order",
                              related_name="order_routes")
    status_description = models.TextField(verbose_name="status description", max_length=1200)
    created_by = models.UUIDField(db_index=True, verbose_name="created by")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created at")

    class Meta:
        verbose_name = "express order status history"
        verbose_name_plural = "express order status histories"
        db_table = "mdl_express_order_status_history"
        index_together = ("order", "created_by")
        app_label = "express_service"
        ordering = ["-created_at"]


class ExpressOrderGoods(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    order = models.ForeignKey(ExpressOrder, on_delete=models.CASCADE, verbose_name="order", related_name="order_goods")
    goods_name_cn = models.TextField(verbose_name="goods_name cn", null=True, blank=True, max_length=2000)
    goods_name_en = models.TextField(verbose_name="goods_name en", null=True, blank=True, max_length=2000)

    goods_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="goods price", default=0)
    price_currency = models.CharField(max_length=3, verbose_name="price currency", null=True, blank=True, )

    goods_count = models.IntegerField(verbose_name="goods count")
    goods_image = models.URLField(verbose_name="order image", null=True, blank=True)

    mailNo = models.CharField(db_index=True, max_length=200, verbose_name="mail no")
    weight = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="weight", default=0)
    volume_weight = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="volume weight", default=0)
    length = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="length", default=0)
    width = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="width", default=0)
    height = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="height", default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="volume", default=0)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created at")

    class Meta:
        verbose_name = "express order goods"
        verbose_name_plural = "express order goods"
        db_table = "mdl_express_order_goods"
        app_label = "express_service"
        ordering = ["-created_at"]


class ShareExpressOrder(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, verbose_name="id")
    order = models.ForeignKey(ExpressOrder, on_delete=models.CASCADE, verbose_name="order", related_name="share_order")
    share_code = models.CharField(db_index=True, max_length=200, verbose_name="share code")
    user = models.UUIDField(db_index=True, verbose_name="user", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="created at")

    class Meta:
        verbose_name = "share express order"
        verbose_name_plural = "share express orders"
        db_table = "mdl_express_share_order"
        app_label = "express_service"
        unique_together = ("order", "share_code")
        ordering = ("-created_at", )
