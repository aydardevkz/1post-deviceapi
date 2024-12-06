from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user_service.models import Admin, ReceivingStation, ReceivingStationStaff


@receiver(post_save, sender=Admin)
def create_admin(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        pass


@receiver(post_save, sender=ReceivingStation)
def create_organization(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        pass


@receiver(post_save, sender=ReceivingStationStaff)
def create_organization_staff(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        pass
