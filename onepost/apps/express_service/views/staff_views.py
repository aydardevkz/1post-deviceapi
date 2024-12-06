from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from apps.express_service.filters import ExpressOrderStatusFilter
from apps.express_service.models import ExpressOrderStatus, ExpressOrder
from apps.express_service.pagination import ExpressStdPageResultsSetPagination
from apps.express_service.serializers.staff.order_serializer import ExpressOrderDeviceSerializer
from config.permission.permissions import IsWarehouseStaffPermission, CustomAuthenticationPermission


class ExpressOrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    pagination_class = ExpressStdPageResultsSetPagination
    permission_classes = [CustomAuthenticationPermission, IsWarehouseStaffPermission]


    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        "order_no",
        "extra_no",
        "contact_phone",
    ]

    def get_serializer_class(self):
        return ExpressOrderDeviceSerializer

    def get_queryset(self):
        return ExpressOrder.objects.filter(is_deleted=False, is_user_deleted=False)



