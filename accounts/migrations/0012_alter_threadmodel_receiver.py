# Generated by Django 3.2.5 on 2022-02-09 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20220205_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadmodel',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.user'),
        ),
    ]
