# Generated by Django 3.1.10 on 2021-05-08 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210507_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='animes',
        ),
        migrations.AddField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorited_by', to='core.Anime'),
        ),
    ]
