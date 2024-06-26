# Generated by Django 5.0.3 on 2024-05-10 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='/media/defaultprofile.jpg', upload_to='media'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(default='Hey There!', max_length=50),
        ),
    ]
