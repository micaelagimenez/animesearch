# Generated by Django 3.1.10 on 2021-05-12 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='characters_average',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='anime',
            name='plot_average',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='anime',
            name='visuals_average',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]
