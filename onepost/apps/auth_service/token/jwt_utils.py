import uuid
import jwt
import datetime
from django.core.cache import caches
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from apps.auth_service.models import TokenBlacklist
from config.settings.base import AUTH_CACHE_ALIAS, CACHES


class JWTUtils:
    ACCESS_TOKEN_EXPIRATION = datetime.timedelta(days=30)
    REFRESH_TOKEN_EXPIRATION = datetime.timedelta(days=60)
    ALGORITHM = "RS256"
    ISSUER = "https://auth.1post.kz/"
    CACHE = caches[settings.AUTH_CACHE_ALIAS]
    TIMEOUT = 259200  # 3 days in seconds

    def get_cache_blacklist(self, user_id, phone):
        cache_key = f"black_list_{user_id}_{phone}"
        return self.CACHE.get(cache_key)

    def set_cache_blacklist(self, user_id, phone, jti):
        cache_key = f"black_list_{user_id}_{phone}"
        self.CACHE.set(cache_key, jti, timeout=self.TIMEOUT)
        return True

    def delete_cache_blacklist(self, user_id, phone):
        cache_key = f"black_list_{user_id}_{phone}"
        self.CACHE.delete(cache_key)

    @staticmethod
    def generate_token(user_id, phone, jti, is_refresh=False):
        exp = datetime.datetime.now()+ (
            JWTUtils.REFRESH_TOKEN_EXPIRATION if is_refresh else JWTUtils.ACCESS_TOKEN_EXPIRATION
        )
        payload = {
            "user_id": str(user_id),
            "iss": JWTUtils.ISSUER,
            "auth_time": datetime.datetime.now().timestamp(),
            "sub": str(user_id),
            "iat": datetime.datetime.now().timestamp(),
            "exp": exp.timestamp(),
            "phone": phone,
            "jti": jti,
        }
        token = jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=JWTUtils.ALGORITHM)
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_PUBLIC_KEY,
                algorithms=[JWTUtils.ALGORITHM],
                issuer=JWTUtils.ISSUER
            )
            if self.is_blacklisted(payload.get("user_id"), payload.get("phone"), payload.get("jti")):
                return "Token has been blacklisted"
            return payload
        except ExpiredSignatureError:
            return "Token has expired"
        except InvalidTokenError:
            return "Invalid token"
        except Exception as e:
            return f"Token decoding failed: {e}"

    @staticmethod
    def refresh_token(refresh_token):
        jwt_utils = JWTUtils()
        decoded = jwt_utils.decode_token(refresh_token)
        if isinstance(decoded, str):  # 错误信息
            return decoded

        user_id, phone = decoded.get("user_id"), decoded.get("phone")
        new_jti = uuid.uuid4().hex
        TokenBlacklist.objects.filter(user_id=user_id).update(jti=new_jti)

        access_token = jwt_utils.generate_token(user_id, phone, jti=new_jti, is_refresh=False)
        new_refresh_token = jwt_utils.generate_token(user_id, phone, jti=new_jti, is_refresh=True)
        return access_token, new_refresh_token

    def is_blacklisted(self, user_id, phone, jti):
        cache_blacklist = self.get_cache_blacklist(user_id, phone)
        if cache_blacklist:
            return True
        try:
            TokenBlacklist.objects.get(user_id=user_id, jti=jti)
            self.set_cache_blacklist(user_id, phone, jti)
            return True
        except TokenBlacklist.DoesNotExist:
            return False

