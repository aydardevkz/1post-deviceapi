from django.urls import path
from apps.auth_service.views import *

urlpatterns = [
    path("api/v1/app-version/", AppVersionViewSet.as_view(), name="app-version"),
    path("api/v1/verify-phone-password/", VerifyPhonePasswordViewSet.as_view(), name="verify-phone-password"),
    path("api/v1/verify-email-password/", VerifyEmailPasswordViewSet.as_view(), name="verify-email-password"),
]
