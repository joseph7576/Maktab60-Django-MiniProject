# Generated by Django 3.2.9 on 2021-12-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0005_auto_20211202_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]