# Generated by Django 3.2.9 on 2021-11-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]