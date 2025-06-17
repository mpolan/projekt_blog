# blog/urls.py

from django.urls import path
from . import views
from blog.admin import blog_site


urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("ustawienia_konta/", views.account_settings, name='ustawienia_konta'),
    path("post/new/", views.create_post, name="create_post"),
    path("post/<int:pk>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path("blogadmin/", blog_site.urls),
]