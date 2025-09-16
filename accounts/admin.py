from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'issuer_name', 'has_secret')
    search_fields = ('user__username', 'user__email')

    @admin.display(description='已配置密钥', boolean=True)
    def has_secret(self, obj: UserProfile) -> bool:
        return bool(obj.totp_secret)
