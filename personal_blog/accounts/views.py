from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, EditProfileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


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