# Generated by Django 4.0 on 2022-09-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]