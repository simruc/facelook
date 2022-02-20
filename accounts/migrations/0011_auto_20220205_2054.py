# Generated by Django 3.2.5 on 2022-02-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_relationship'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='relationship',
            name='status',
            field=models.CharField(choices=[('sent', 'sent'), ('accepted', 'accepted'), ('rejected', 'rejected')], max_length=8),
        ),
    ]