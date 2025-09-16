from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserProfile


class Command(BaseCommand):
    help = '创建一个带有谷歌验证器密钥的演示用户。'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'demo'
        password = 'DemoPass123'
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.email = 'demo@example.com'
            user.save()
            self.stdout.write(self.style.SUCCESS('已创建演示用户 demo'))
        else:
            self.stdout.write('演示用户 demo 已存在，更新密码。')
            user.set_password(password)
            user.save(update_fields=['password'])

        profile: UserProfile = user.userprofile
        secret = profile.ensure_totp_secret()
        uri = profile.get_metadata().provisioning_uri(user.username)
        self.stdout.write('\n使用以下信息在谷歌验证器中绑定：')
        self.stdout.write(f'  用户名: {username}')
        self.stdout.write(f'  初始密码: {password}')
        self.stdout.write(f'  验证器密钥: {secret}')
        self.stdout.write(f'  otpauth URI: {uri}')
