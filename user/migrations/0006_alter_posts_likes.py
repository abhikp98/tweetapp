# Generated by Django 5.0.3 on 2024-05-10 07:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_posts_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
