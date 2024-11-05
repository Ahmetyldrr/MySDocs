# Generated by Django 5.1.1 on 2024-09-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_tournament_unique_season_tournament'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='tournament',
            name='unique_season_tournament',
        ),
        migrations.AddConstraint(
            model_name='tournament',
            constraint=models.UniqueConstraint(fields=('season_id', 'tournament_id'), name='unique_season_tournament'),
        ),
    ]