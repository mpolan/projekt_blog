from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Comment
from blog.forms import CommentForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db import models

def blog_index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            models.Q(visibility='public') | models.Q(author=request.user)
        ).order_by("-created_on")
    else:
        posts = Post.objects.filter(visibility='public').order_by("-created_on")

    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
    return render(request, "blog/detail.html", context)



def account_settings(request):
    return render(request, 'konto/account_settings.html')


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("blog_index")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/edit_post.html", {"form": form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("blog_index")
    return render(request, "blog/delete_post.html", {"post": post})
