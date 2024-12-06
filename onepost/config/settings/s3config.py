# s3config.py
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage


class NewsMediaStorage(S3Boto3Storage):
    bucket_name = f"{settings.SYSTEM_NAME}-news"
    file_overwrite = False
    acl = 'public-read'
    location = 'media'
    default_acl = 'public-read'
    custom_domain = f"{settings.AWS_S3_ENDPOINT_HOST}/{bucket_name}"


# 公共文件存储，任何人都可以访问（例如用户头像）
class AccountMediaStorage(S3Boto3Storage):
    bucket_name = f"{settings.SYSTEM_NAME}-account"
    file_overwrite = False
    acl = 'public-read'
    location = 'media'
    default_acl = 'public-read'
    custom_domain = f"{settings.AWS_S3_ENDPOINT_HOST}/{bucket_name}"

    def _save(self, name, content):
        name = name.lower()
        return super()._save(name, content)


# 私密文件存储，仅授权用户可以访问（例如身份验证文件）
class IdCardS3Boto3Storage(S3Boto3Storage):
    bucket_name = f"{settings.SYSTEM_NAME}-id-card"
    file_overwrite = False
    acl = 'private'
    location = 'media'
    default_acl = 'public-read'
    custom_domain = f"{settings.AWS_S3_ENDPOINT_HOST}/{bucket_name}"



class SignatureS3Boto3Storage(S3Boto3Storage):
    bucket_name = f"{settings.SYSTEM_NAME}-signature"
    file_overwrite = False
    acl = 'private'
    location = 'media'
    default_acl = 'public-read'
    custom_domain = f"{settings.AWS_S3_ENDPOINT_HOST}/{bucket_name}"


class OpenOrderStorage(S3Boto3Storage):
    bucket_name = f"{settings.SYSTEM_NAME}-open-order"
    file_overwrite = False
    acl = 'public-read'
    location = 'media'
    default_acl = 'public-read'
    custom_domain = f"{settings.AWS_S3_ENDPOINT_HOST}/{bucket_name}"

    def _save(self, name, content):
        name = name.lower()

        # 压缩和调整大小
        if content.content_type in ['image/jpeg', 'image/png']:
            image = Image.open(content)
            image_format = 'JPEG' if content.content_type == 'image/jpeg' else 'PNG'

            # 调整图片大小（假设宽度 800，高度按比例缩放）
            max_width = 600
            if image.width > max_width:
                height = int((max_width / image.width) * image.height)
                image = image.resize((max_width, height), Image.Resampling.LANCZOS)

            # 压缩图片质量
            compressed_image = BytesIO()
            image.save(
                compressed_image,
                format=image_format,
                quality=85,
                optimize=True,
                exif=None
            )
            compressed_image.seek(0)

            # 替换 content 内容
            content = ContentFile(compressed_image.read(), name=content.name)

        return super()._save(name, content)
