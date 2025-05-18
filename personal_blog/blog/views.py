from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Comment, PostImage
from blog.forms import CommentForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db import models
from django.db.models import Q

from django.http import FileResponse, Http404
from django.conf import settings
from blog.models import PostImage
import os

from utils.supabase_storage import upload_image_to_supabase


def serve_protected_image(request, filepath):
    try:
        image = PostImage.objects.select_related("post").get(image=filepath)
        post = image.post
    except PostImage.DoesNotExist:
        raise Http404("Obraz nie istnieje.")

    # Sprawdzenie dostępu
    if post.is_protected():
        session_key = (
            f"user_{request.user.id}_unlocked_post_{post.pk}"
            if request.user.is_authenticated
            else f"anon_unlocked_post_{post.pk}"
        )
        if not request.session.get(session_key) and request.user != post.author:
            raise Http404("Brak dostępu do chronionego pliku.")

    # Serwowanie pliku
    full_path = os.path.join(settings.MEDIA_ROOT, filepath)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, "rb"), content_type="image/png")
    else:
        raise Http404("Plik nie znaleziony.")


def blog_index(request):
    query = request.GET.get("q", "")

    if request.user.is_authenticated:
        posts = Post.objects.filter(
            Q(visibility='public') | Q(author=request.user)
        )
    else:
        posts = Post.objects.filter(visibility='public')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(author__profile__display_name__icontains=query)
        ).distinct()

    context = {
        "posts": posts.order_by("-created_on"),
        "query": query,
    }
    return render(request, "blog/index.html", context)



def blog_category(request, category):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            Q(categories__name__icontains=category),
            Q(visibility='public') | Q(author=request.user)
        ).order_by("-created_on")
    else:
        posts = Post.objects.filter(
            categories__name__icontains=category,
            visibility='public'
        ).order_by("-created_on")

    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)



def blog_detail(request, pk):
    post = get_object_or_404(
        Post.objects
            .select_related("author__profile")
            .prefetch_related("images", "comments")
            .only("title", "body", "created_on", "author", "author__profile__display_name"),
        pk=pk
    )


    # Jeśli post jest prywatny i użytkownik to nie autor → błąd 403
    if post.visibility == 'private' and post.author != request.user:
        return render(request, "blog/private_forbidden.html", status=403)
    # Klucz sesji zależny od użytkownika
    if request.user.is_authenticated:
        session_key = f"user_{request.user.id}_unlocked_post_{post.pk}"
    else:
        session_key = f"anon_unlocked_post_{post.pk}"

    # Obsługa formularza hasła – sprawdź najpierw POST
    if request.method == "POST" and 'password' in request.POST:
        if request.POST["password"] == post.password:
            request.session[session_key] = True
            if not request.user.is_authenticated:
                request.session.set_expiry(0)  # sesja dla niezalogowanego – do zamknięcia przeglądarki
            return redirect("blog_detail", pk=post.pk)
        else:
            error = "Nieprawidłowe hasło"
            return render(request, "blog/detail_locked.html", {"post": post, "error": error})

    # Sprawdź czy post został wcześniej odblokowany
    unlocked = request.session.get(session_key, False)

    # Jeśli post zabezpieczony i NIE odblokowany → pokaż formularz hasła
    if post.is_protected() and not unlocked:
        return render(request, "blog/detail_locked.html", {"post": post})

    # Normalny widok posta
    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    if request.method == "POST" and "author" in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog/detail.html", {
    "post": post,
    "form": form,
    "comments": comments,
    "unlocked": True,  # ← DODAJ TO
})




def account_settings(request):
    return render(request, 'konto/account_settings.html')

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        images = request.FILES.getlist("images")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            for img in images:
                filename = f"{request.user.id}/{img.name}"
                if upload_image_to_supabase(img, filename):
                    PostImage.objects.create(post=post, image_url=filename)

            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})



@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        images = request.FILES.getlist("images")

        if form.is_valid():
            post = form.save()

            # usuń stare zdjęcia
            delete_ids = request.POST.getlist("delete_images")
            if delete_ids:
                for img_id in delete_ids:
                    try:
                        image = post.images.get(id=img_id)
                        image.delete()
                    except PostImage.DoesNotExist:
                        pass

            # dodaj nowe zdjęcia
            for img in images:
                filename = f"{request.user.id}/{img.name}"
                if upload_image_to_supabase(img, filename):
                    PostImage.objects.create(post=post, image_url=filename)

            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {
        "form": form,
        "post": post
    })



@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("blog_index")
    return render(request, "blog/delete_post.html", {"post": post})
