"""Module for creating DB-admin."""
from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.conf import settings


def create_superuser(apps, schema_editor):
    """Create superuser for the app at the first start."""
    User = apps.get_model('auth', 'User')
    User.objects.create(username='admin',
                        email=settings.ADMIN_EMAIL,
                        password=make_password('12345678'),
                        is_superuser=True,
                        is_staff=True,
                        is_active=True)


class Migration(migrations.Migration):
    """Migration plan for superuser creation."""

    dependencies = [
        ('auth', '__latest__')
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
