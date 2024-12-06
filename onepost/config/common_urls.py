# #!/usr/bin/python3
# # -*- coding:utf-8 -*-
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from config.common_views import *


router = DefaultRouter()

router.register(r'info', UserInfoViewSet, basename="info")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
