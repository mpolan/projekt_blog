from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.display_name or self.user.username

# Tworzenie i uzupełnienie display_name automatycznie
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        first = instance.first_name.lower()[0] if instance.first_name else ''
        last = instance.last_name.lower() if instance.last_name else ''
        profile = Profile.objects.create(
            user=instance,
            display_name=f"{first}.{last}"
        )
    else:
        instance.profile.save()
