from rest_framework.authentication import BaseAuthentication
from apps.auth_service.token.jwt_utils import JWTUtils
from apps.user_service.models import Users, Admin, BaseAdmin
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from config.settings.base import AUTH_CACHE_ALIAS
from utils.cache_response import get_cache_value_func, set_cache_value_func

User = get_user_model()


class CustomStandardAdminAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        # 检查 Authorization 头是否存在且格式正确
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        # 提取 Token
        token = auth_header.split(" ")[1]

        # 解码 Token
        payload = JWTUtils().decode_token(token)

        # 如果解码失败或返回错误信息
        if isinstance(payload, str):
            raise AuthenticationFailed(payload)  # 返回解码失败信息

        # 获取 user_id，查找用户
        user_id = payload.get("user_id", None)
        if not user_id:
            raise AuthenticationFailed("Invalid Token: Missing user_id")
        admin = get_cache_value_func(cache_name=AUTH_CACHE_ALIAS, unique_identifier=f"auth_user:{user_id}")
        if not admin:
            admin = Admin.objects.select_related("user").only(
                "user__id", "user__is_active"
            ).get(
                user__id=user_id,
                user__is_active=True
            )
            print("auth_user:", admin)
            if admin.role == "WAREHOUSE_STAFF" or admin.role == "WAREHOUSE_OWNER":
                try:
                    set_cache_value_func(
                        cache_name=AUTH_CACHE_ALIAS,
                        unique_identifier=f"auth_user:{user_id}",
                        queryset=admin,
                        timeout=60 * 60 * 24
                    )
                except Admin.DoesNotExist:
                    raise AuthenticationFailed("User not found")
            else:
                raise AuthenticationFailed("Warehouse owner not found or not warehouse staff")
        return admin, token

    def authenticate_header(self, request):
        return 'Bearer'


class CustomStandardBaseAdminAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        # 检查 Authorization 头是否存在且格式正确
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        # 提取 Token
        token = auth_header.split(" ")[1]

        # 解码 Token
        payload = JWTUtils().decode_token(token)

        # 如果解码失败或返回错误信息
        if isinstance(payload, str):
            raise AuthenticationFailed(payload)  # 返回解码失败信息

        # 获取 user_id，查找用户
        user_id = payload.get("user_id", None)
        if not user_id:
            raise AuthenticationFailed("Invalid Token: Missing user_id")
        user = get_cache_value_func(cache_name=AUTH_CACHE_ALIAS, unique_identifier=f"auth_user:{user_id}")
        if not user:
            user = BaseAdmin.objects.select_related("user").only(
                "user__id", "user__is_active"
            ).get(
                user__id=user_id,
                user__is_active=True
            )
            try:
                set_cache_value_func(
                    cache_name=AUTH_CACHE_ALIAS,
                    unique_identifier=f"auth_user:{user_id}",
                    queryset=user,
                    timeout=60 * 60 * 24
                )
            except Users.DoesNotExist:
                raise AuthenticationFailed("User not found")
        return user, token

    def authenticate_header(self, request):
        return 'Bearer'
