# Generated by Django 3.2.5 on 2022-02-12 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='photos/post_images/avatar.png', null=True, upload_to='photos/post_images'),
        ),
    ]