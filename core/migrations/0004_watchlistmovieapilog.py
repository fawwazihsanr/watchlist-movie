# Generated by Django 4.0 on 2022-09-24 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0003_favoritemovieshows_movie_id_favoritetvshows_tv_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchlistMovieApiLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('method', models.CharField(max_length=10, null=True)),
                ('url_path', models.CharField(max_length=50, null=True)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ApiLog', to='auth.user')),
            ],
            options={
                'db_table': 'watchlist_movie_api_log',
            },
        ),
    ]