from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totp_secret', models.CharField(blank=True, max_length=64, verbose_name='谷歌验证密钥')),
                ('issuer_name', models.CharField(default='AuthSite 演示', max_length=64, verbose_name='发行者')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户安全信息',
                'verbose_name_plural': '用户安全信息',
            },
        ),
    ]
