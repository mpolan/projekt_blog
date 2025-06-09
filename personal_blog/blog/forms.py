from django import forms
from .models import Post
import logging

logger = logging.getLogger(__name__)


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        logger.info("Nowy komentarz od autora: %s", cleaned_data.get("author"))
        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "categories", "visibility", "password"]
        labels = {
            "title": "Tytuł posta",
            "body": "Treść",
            "categories": "Kategorie",
            "visibility": "Widoczność",
            "password": "Hasło (opcjonalne)",
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            logger.info("Zapisano post: %s (ID=%s)", instance.title, instance.pk)
        return instance
