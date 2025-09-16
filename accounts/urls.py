from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import TwoFactorLoginView, dashboard, totp_setup

app_name = 'accounts'

urlpatterns = [
    path('login/', TwoFactorLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('setup/', totp_setup, name='setup'),
]
