from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class Profile(models.Model):
    GENDER_CHOICES = [
        ("male", "Mężczyzna"),
        ("female", "Kobieta"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    plec = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def get_age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        if self.plec == "female":
            return "/media/default_female.png"
        return "/media/default_male.png"


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

