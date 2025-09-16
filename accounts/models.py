from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import models

from . import totp

User = get_user_model()


@dataclass
class TOTPMetadata:
    secret: str
    issuer: str

    def provisioning_uri(self, username: str) -> str:
        return totp.provisioning_uri(self.secret, username=username, issuer=self.issuer)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    totp_secret = models.CharField('谷歌验证密钥', max_length=64, blank=True)
    issuer_name = models.CharField('发行者', max_length=64, default='AuthSite 演示')

    class Meta:
        verbose_name = '用户安全信息'
        verbose_name_plural = '用户安全信息'

    def ensure_totp_secret(self) -> str:
        if not self.totp_secret:
            self.totp_secret = totp.random_base32_secret(32)
            self.save(update_fields=['totp_secret'])
        return self.totp_secret

    def get_metadata(self) -> TOTPMetadata:
        return TOTPMetadata(secret=self.ensure_totp_secret(), issuer=self.issuer_name)

    def verify_token(self, token: str) -> bool:
        secret = self.ensure_totp_secret()
        return totp.verify_totp(secret, token)

    def __str__(self) -> str:  # pragma: no cover - human readable helper
        return f"UserProfile<{self.user.username}>"
