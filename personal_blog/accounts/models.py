from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

from utils.supabase_storage import get_profile_image_url

class Profile(models.Model):
    GENDER_CHOICES = [
        ("male", "Mężczyzna"),
        ("female", "Kobieta"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    plec = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField(null=True, blank=True)
    
    # zamiast ImageField – ścieżka do pliku w Supabase
    avatar_url = models.CharField(max_length=255, blank=True, null=True)

    def get_age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    @property
    def avatar_signed_url(self):
        """Zwraca podpisany URL avatara (Supabase) lub domyślnego avatara"""
        if self.avatar_url:
            return get_profile_image_url(self.avatar_url)
        default_path = "defaults/default_female.png" if self.plec == "female" else "defaults/default_male.png"
        return get_profile_image_url(default_path)

    def __str__(self):
        return self.display_name or self.user.username


# Tworzenie i uzupełnienie display_name automatycznie
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
