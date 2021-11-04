from django.contrib.auth.hashers import make_password

import apps.users.models
from django.db import migrations, models


def set_initial_user_data(apps, schema_editor):
    User = apps.get_model("users", "User")
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).bulk_create([
        User(email="user@freshcode.me", role="user", password=make_password("user")),
        User(email="admin@freshcode.me", role="admin", password=make_password("admin")),
    ])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=190, unique=True)),
                ('role', models.CharField(choices=[('admin', 'ADMIN'), ('user', 'GENERAL')], default='user', max_length=10)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.users.models.CustomUserManager()),
            ],
        ),
        migrations.RunPython(set_initial_user_data),
    ]
