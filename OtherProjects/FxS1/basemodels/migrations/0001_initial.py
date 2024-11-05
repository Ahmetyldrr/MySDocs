# Generated by Django 4.2.7 on 2024-10-22 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FikstureModelData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_id', models.CharField(max_length=255, unique=True)),
                ('tarih', models.DateField()),
                ('data', models.JSONField()),
                ('count', models.IntegerField()),
                ('isprogress', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Model Data',
                'verbose_name_plural': 'Model Datas',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('tournament_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tournament_name', models.CharField(max_length=255)),
                ('tournament_slug', models.CharField(max_length=255)),
                ('tournament_category_name', models.CharField(max_length=255)),
                ('tournament_category_slug', models.CharField(max_length=255)),
                ('tournament_uniqueTournament_category_id', models.IntegerField()),
                ('tournament_uniqueTournament_hasEventPlayerStatistics', models.BooleanField(default=False)),
                ('tournament_model_id', models.IntegerField()),
                ('tournament_isGroup', models.BooleanField(blank=True, default=False, null=True)),
                ('tournament_uniqueTournament_hasPerformanceGraphFeature', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'verbose_name': 'Tournament',
                'verbose_name_plural': 'Tournaments',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('season_id', models.IntegerField(primary_key=True, serialize=False)),
                ('season_name', models.CharField(max_length=255)),
                ('season_year', models.CharField(max_length=9)),
                ('tournament', models.ForeignKey(db_column='tournament_id', on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='basemodels.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=255)),
                ('team_slug', models.SlugField(max_length=255)),
                ('team_shortName', models.CharField(max_length=100)),
                ('team_nameCode', models.CharField(max_length=10)),
                ('team_national', models.BooleanField(default=False)),
                ('season', models.ForeignKey(db_column='season_id', on_delete=django.db.models.deletion.CASCADE, related_name='teams2', to='basemodels.season')),
                ('tournament', models.ForeignKey(db_column='tournament_id', on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='basemodels.tournament')),
            ],
            options={
                'unique_together': {('team_id', 'tournament', 'season')},
            },
        ),
    ]