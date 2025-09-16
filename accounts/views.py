from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import TwoFactorAuthenticationForm


class TwoFactorLoginView(LoginView):
    form_class = TwoFactorAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form: TwoFactorAuthenticationForm) -> HttpResponse:
        user = form.get_user()
        profile = getattr(user, 'userprofile', None)
        otp_token = form.cleaned_data.get('otp_token')

        if profile is None or not profile.verify_token(otp_token):
            form.add_error('otp_token', form.error_messages['invalid_otp'])
            return self.form_invalid(form)

        messages.success(self.request, '登录成功，二次验证通过。')
        return super().form_valid(form)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    profile = request.user.userprofile
    context = {
        'user': request.user,
        'totp_secret': profile.ensure_totp_secret(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def totp_setup(request: HttpRequest) -> HttpResponse:
    profile = request.user.userprofile
    metadata = profile.get_metadata()
    context = {
        'user': request.user,
        'metadata': metadata,
        'provisioning_uri': metadata.provisioning_uri(request.user.username),
    }
    return render(request, 'accounts/setup_totp.html', context)
