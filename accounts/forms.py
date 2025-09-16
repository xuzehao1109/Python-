from django import forms
from django.contrib.auth.forms import AuthenticationForm


class TwoFactorAuthenticationForm(AuthenticationForm):
    otp_token = forms.CharField(
        label='谷歌验证码',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '6 位动态验证码',
            'autocomplete': 'one-time-code',
            'inputmode': 'numeric',
        }),
    )

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_otp': '谷歌验证未通过，请重新输入动态验证码。',
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        for field in self.fields.values():
            css_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_class + ' input-control').strip()
        self.fields['username'].widget.attrs.setdefault('placeholder', '用户名')
        self.fields['password'].widget.attrs.setdefault('placeholder', '登录密码')

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        try:
            profile = user.userprofile
        except AttributeError:
            return
        profile.ensure_totp_secret()
