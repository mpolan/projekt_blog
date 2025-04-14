from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, EditProfileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

def custom_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔐 logika zapamiętania sesji
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)  # Sesja wygasa po zamknięciu przeglądarki
            else:
                request.session.set_expiry(1209600)  # 2 tygodnie

            return redirect("blog_index")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

@login_required
def account_settings(request):
    return render(request, 'konto/account_settings.html')

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account_settings')
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'konto/edit_profile.html', {'form': form})