# Generated by Django 5.0.4 on 2024-04-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('rating', models.FloatField()),
                ('episodes', models.PositiveIntegerField()),
                ('genre', models.ManyToManyField(to='api.genre')),
            ],
        ),
    ]
