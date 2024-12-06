# #!/usr/bin/python3
# # -*- coding:utf-8 -*-
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("auth/", include(('apps.auth_service.urls', 'auth'), namespace="auth_service"), ),
    path("express/warehouse-staff/", include(('apps.express_service.urls.staff_urls', 'express'), namespace="express"), ),
    path("common/", include(('config.common_urls', 'user'), namespace="common_urls"),),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
