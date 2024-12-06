from django_filters import FilterSet
from apps.express_service.models import ExpressOrderStatus


class ExpressOrderStatusFilter(FilterSet):
    class Meta:
        model = ExpressOrderStatus
        fields = {
            "status_type": ["exact"],
            "order__market_company": ["exact"],
            "order__station": ["exact"],
            "order__is_payed": ["exact"],
        }
