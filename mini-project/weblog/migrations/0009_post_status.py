# Generated by Django 3.2.9 on 2021-12-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0008_alter_post_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('PU', 'Publish'), ('DR', 'Draft')], default='DR', max_length=2),
        ),
    ]
