from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


VISIBILITY_CHOICES = (
    ('public', 'Publiczny'),
    ('private', 'Tylko dla mnie'),
)

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = CKEditor5Field('Text', config_name='extends')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    password = models.CharField(max_length=100, blank=True, null=True)

    def is_protected(self):
        return bool(self.password)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=255)  # zamiast ImageField
