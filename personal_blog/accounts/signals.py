from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     else:
#         # sprawdź czy profil istnieje, jeśli nie – utwórz
#         try:
#             instance.profile.save()
#         except Profile.DoesNotExist:
#             Profile.objects.create(user=instance)


User = get_user_model()

@receiver(post_save, sender=User)
def add_default_group(sender, instance, created, **kwargs):
    if created:
        user_group = Group.objects.get(name='Użytkownik')
        instance.groups.add(user_group)