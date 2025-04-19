from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput
from .models import Profile
from datetime import date, timedelta


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(required=True, widget=DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get("date_of_birth")

        if dob:
            min_date = date(1900, 1, 1)
            max_date = date.today() - timedelta(days=13*365)

            if dob < min_date:
                self.add_error("date_of_birth", "Data urodzenia nie może być wcześniejsza niż 1900 rok.")
            elif dob > max_date:
                self.add_error("date_of_birth", "Musisz mieć co najmniej 13 lat, by założyć konto.")

    GENDER_CHOICES = [
        ("male", "Mężczyzna"),
        ("female", "Kobieta"),
    ]

    plec = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True,
        label="Płeć"
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "date_of_birth", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)
            first = user.first_name.lower()[0] if user.first_name else ''
            last = user.last_name.lower() if user.last_name else ''
            profile.display_name = f"{first}.{last}"
            profile.plec = self.cleaned_data["plec"]
            profile.date_of_birth = self.cleaned_data["date_of_birth"]
            profile.save()

        return user




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'date_of_birth', 'plec']


