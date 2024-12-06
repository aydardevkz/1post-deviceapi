from rest_framework.serializers import ModelSerializer
from apps.user_service.models import *


class AdminInfoSerializer(ModelSerializer):
    class Meta:
        model = Admin
        fields = (
            "xid",
            "role",
        )


class AdminInfoUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserBase
        fields = ("id", "first_name", "last_name", "avatar", "gender", "birthday")


class AdminRetrieveSerializer(ModelSerializer):
    admin = AdminInfoSerializer()

    class Meta:
        model = UserBase
        fields = ("id", "first_name", "last_name", "email", "avatar", "gender", "birthday", "phone", "admin", "created_at")


class UserBaseRetrieveSerializer(ModelSerializer):
    class Meta:
        model = UserBase
        fields = ("id", "first_name", "last_name", "email", "avatar", "gender", "birthday", "phone", "created_at")



class UserBaseShortSerializer(ModelSerializer):
    class Meta:
        model = UserBase
        fields = ("id", "first_name", "last_name", "avatar", "created_at")


class AdminShortRetrieveSerializer(ModelSerializer):
    user= UserBaseShortSerializer()
    class Meta:
        model = Admin
        fields = ("user", "role")
