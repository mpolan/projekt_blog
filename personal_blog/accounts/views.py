from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, EditProfileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from utils.supabase_storage import upload_profile_image
import logging
logger = logging.getLogger(__name__)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


def custom_login_view(request):
    if request.method == "POST":
        logger.info("Próba logowania użytkownika: %s", request.POST.get("username"))
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)

            logger.info("Użytkownik %s zalogował się pomyślnie", user.username)
            return redirect("blog_index")
        else:
            logger.warning("Nieudana próba logowania: %s", request.POST.get("username"))
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
def account_settings(request):
    return render(request, 'konto/account_settings.html')


@login_required
def edit_profile(request):
    profile = request.user.profile
    logger.info("Użytkownik %s edytuje profil", request.user.username)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        avatar_file = request.FILES.get("avatar")

        if form.is_valid():
            profile = form.save(commit=False)

            if avatar_file:
                filename = f"{request.user.id}/avatar.jpg"
                if upload_profile_image(avatar_file, filename):
                    profile.avatar_url = filename
                    logger.info("Upload zakończony sukcesem: %s", filename)
                else:
                    logger.error("Błąd podczas uploadu avatara dla %s", request.user.username)

            profile.save()
            logger.info("Profil użytkownika %s został zapisany", request.user.username)
            return redirect('account_settings')
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'konto/edit_profile.html', {
        'form': form,
        'profile': profile,
    })
