from django.http import HttpResponseRedirect, FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Comment, PostImage
from blog.forms import CommentForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db.models import Q
from django.conf import settings
from utils.supabase_storage import upload_image_to_supabase
import os
import logging

logger = logging.getLogger(__name__)


def serve_protected_image(request, filepath):
    full_path = os.path.join(settings.MEDIA_ROOT, filepath)
    try:
        image = PostImage.objects.select_related("post").get(image=filepath)
        post = image.post
    except PostImage.DoesNotExist:
        logger.error("Plik nie istnieje w bazie: %s", filepath)
        raise Http404("Obraz nie istnieje.")

    if post.is_protected():
        session_key = (
            f"user_{request.user.id}_unlocked_post_{post.pk}"
            if request.user.is_authenticated
            else f"anon_unlocked_post_{post.pk}"
        )
        if not request.session.get(session_key) and request.user != post.author:
            logger.warning("Nieautoryzowany dostęp do obrazu: %s przez %s", filepath, request.user)
            raise Http404("Brak dostępu do chronionego pliku.")

    if os.path.exists(full_path):
        logger.info("Serwowanie pliku: %s", filepath)
        return FileResponse(open(full_path, "rb"), content_type="image/png")
    else:
        logger.error("Plik nie istnieje fizycznie: %s", full_path)
        raise Http404("Plik nie znaleziony.")


def blog_index(request):
    query = request.GET.get("q", "")
    logger.info("Wejście na blog_index – zapytanie: %s", query)

    if request.user.is_authenticated:
        posts = Post.objects.filter(Q(visibility='public') | Q(author=request.user))
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
    logger.info("Wejście do kategorii: %s", category)

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

    logger.info("Użytkownik %s otwiera post ID=%s", request.user, pk)

    if post.visibility == 'private' and post.author != request.user:
        logger.warning("Użytkownik %s próbował otworzyć prywatny post ID=%s", request.user, pk)
        return render(request, "blog/private_forbidden.html", status=403)

    if request.user.is_authenticated:
        session_key = f"user_{request.user.id}_unlocked_post_{post.pk}"
    else:
        session_key = f"anon_unlocked_post_{post.pk}"

    if request.method == "POST" and 'password' in request.POST:
        if request.POST["password"] == post.password:
            request.session[session_key] = True
            logger.info("Post ID=%s odblokowany hasłem przez %s", pk, request.user)
            if not request.user.is_authenticated:
                request.session.set_expiry(0)
            return redirect("blog_detail", pk=post.pk)
        else:
            logger.warning("Błędne hasło do posta ID=%s przez %s", pk, request.user)
            error = "Nieprawidłowe hasło"
            return render(request, "blog/detail_locked.html", {"post": post, "error": error})

    unlocked = request.session.get(session_key, False)

    if post.is_protected() and not unlocked:
        return render(request, "blog/detail_locked.html", {"post": post})

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
            logger.info("Nowy komentarz od '%s' do posta ID=%s", comment.author, pk)
            return HttpResponseRedirect(request.path_info)

    return render(request, "blog/detail.html", {
        "post": post,
        "form": form,
        "comments": comments,
        "unlocked": True,
    })


@login_required
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
                    logger.info("Upload obrazu: %s dla posta %s", img.name, post.title)

            logger.info("Użytkownik %s utworzył post: %s", request.user, post.title)
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

            delete_ids = request.POST.getlist("delete_images")
            if delete_ids:
                for img_id in delete_ids:
                    try:
                        image = post.images.get(id=img_id)
                        image.delete()
                        logger.info("Usunięto zdjęcie ID=%s z posta ID=%s", img_id, pk)
                    except PostImage.DoesNotExist:
                        logger.warning("Nie znaleziono zdjęcia ID=%s do usunięcia", img_id)

            for img in images:
                filename = f"{request.user.id}/{img.name}"
                if upload_image_to_supabase(img, filename):
                    PostImage.objects.create(post=post, image_url=filename)
                    logger.info("Dodano nowe zdjęcie %s do posta ID=%s", img.name, pk)

            logger.info("Użytkownik %s zaktualizował post ID=%s", request.user, pk)
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
        logger.warning("Użytkownik %s usunął post ID=%s", request.user, pk)
        return redirect("blog_index")
    return render(request, "blog/delete_post.html", {"post": post})
