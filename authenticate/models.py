from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
class CustomUser(AbstractUser):
    national_code=models.PositiveIntegerField(unique=True, null=True)
    observer_user=models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)
    loan_remain = models.PositiveSmallIntegerField(default=5)
    profile_img = models.ImageField(upload_to="managing/images/profile_images", null=True, blank=True)
    about = models.TextField(blank=True)
    violations = models.PositiveIntegerField(default=0)
    total_damage_cost = models.PositiveIntegerField(default=0)
    wallet_inventory = models.PositiveIntegerField(default=0)

    address = GenericRelation('managing.Address', related_query_name="user")
    