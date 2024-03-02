# Generated by Django 5.0.2 on 2024-03-01 10:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_platform', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='max_users',
        ),
        migrations.RemoveField(
            model_name='group',
            name='min_users',
        ),
        migrations.AddField(
            model_name='product',
            name='max_users_in_group',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='product',
            name='min_users_in_group',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='user_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
