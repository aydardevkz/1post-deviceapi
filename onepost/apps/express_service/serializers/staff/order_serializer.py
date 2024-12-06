import re
from rest_framework import serializers
from apps.express_service.models import *



class ExpressOrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpressOrderGoods
        fields = (
            'id',
            'order',
            'goods_name_en',
            'goods_name_cn',
            'goods_price',
            'goods_image',
            'goods_count',
            'updated_at',
            'created_at'
        )



class ExpressOrderSerializer(serializers.ModelSerializer):
    order_goods = ExpressOrderGoodsSerializer(many=True)

    class Meta:
        model = ExpressOrder
        fields = ('id', 'order_no', 'extra_no', 'full_address', 'contact_phone', 'order_goods', 'is_payed', 'updated_at', 'created_at')



class ExpressOrderDeviceSerializer(serializers.ModelSerializer):


    class Meta:
        model = ExpressOrder
        fields = (
            'id',
            'order_no',
            'full_address',
            'contact_phone',
            'created_at',
        )
