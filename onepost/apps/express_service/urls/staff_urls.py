from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.express_service.views.staff_views import ExpressOrderViewSet


router = DefaultRouter()


router.register(r"orders", ExpressOrderViewSet, basename="express-orders")

urlpatterns = [
    path("api/v1/", include(router.urls)),

]
