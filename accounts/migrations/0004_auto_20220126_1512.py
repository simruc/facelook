# Generated by Django 3.2.5 on 2022-01-26 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='confirm_password',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]
