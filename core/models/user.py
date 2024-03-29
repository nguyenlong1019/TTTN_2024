from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save 
from django.dispatch import receiver 

from .device import BangCangCa 


class CustomUser(AbstractUser):
    user_type_data = (
        (1, "Admin"),
        (2, "Staff"),
        (3, "Provider")
    )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=15)


class AdminHod(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Provider(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Staff(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # ID Cảng
    cangca = models.ForeignKey(BangCangCa, on_delete=models.DO_NOTHING, default=1)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    '''
    sender: class gọi đến hàm này
    instance: là dữ liệu đang chèn vào model
    created: là True/False, True khi data được chèn vào
    '''
    if created:
        if instance.user_type == 1:
            AdminHod.objects.create(admin=instance) 
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Provider.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    '''Phương thức này sẽ gọi sau khi create_user_profile được thực thi'''
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.provider.save()
