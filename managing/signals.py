from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import MngUser

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs) :
    if kwargs['created'] :
        MngUser.objects.create(user=kwargs['instance'])

