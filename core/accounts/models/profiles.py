from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .users import User, UserType


class Profile(models.Model):
    """
    This is a class for User Profile.
    """

    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    user_type = models.IntegerField(choices=UserType.choices)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_user_type_display()}"


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    This signal is for creating a Profile based on User data.
    """
    if created:
        Profile.objects.create(user=instance, user_type=instance.type)
    else:
        instance.user_profile.save()
