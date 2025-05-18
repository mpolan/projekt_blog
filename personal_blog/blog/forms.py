from django import forms
from .models import Post

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

# PostImageForm już niepotrzebny
