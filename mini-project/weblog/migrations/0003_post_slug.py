# Generated by Django 3.2.9 on 2021-11-27 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0002_post_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=40, null=True),
        ),
    ]
