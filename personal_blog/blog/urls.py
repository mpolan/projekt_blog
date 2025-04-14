# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("ustawienia_konta/", views.account_settings, name='ustawienia_konta'),
    path("post/new/", views.create_post, name="create_post"),  # 👈 nowy URL
]