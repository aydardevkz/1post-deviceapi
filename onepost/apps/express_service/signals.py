# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.express_service.models import *
from config.middlewares.current_user_middleware import get_current_user

@receiver(post_save, sender=BatchStatusModel)
def log_user_action(sender, instance, created, **kwargs):
    user = get_current_user()
    if user:
        # 记录用户操作
        print(f"User {user.username} performed an action.")
    else:
        print("No user information available.")
