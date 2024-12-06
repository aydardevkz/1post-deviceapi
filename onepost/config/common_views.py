from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from apps.user_service.serializers.common.user_common_serializer import *
from config.permission.permissions import CustomAuthenticationPermission
from config.settings.base import APP_VERSION


class UserInfoViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [CustomAuthenticationPermission, ]

    def get_queryset(self):
        return UserBase.objects.filter(id=self.request.user.user.id)

    def get_serializer_class(self):
        if self.action == "update":
            return AdminInfoUpdateSerializer
        return AdminRetrieveSerializer

    def get_object(self):
        return UserBase.objects.get(id=self.request.user.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            response_dict = serializer.data
            response_dict["app_version"] = APP_VERSION
            return Response(
                data=response_dict,
                status=status.HTTP_200_OK
            )
        raise NotFound("User not found")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=AdminRetrieveSerializer(instance).data,
            status=status.HTTP_200_OK
        )
