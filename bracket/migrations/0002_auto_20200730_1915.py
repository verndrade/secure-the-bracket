# Generated by Django 3.0.7 on 2020-07-30 19:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bracket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 6, 19, 15, 16, 491901)),
        ),
        migrations.AddField(
            model_name='team',
            name='team_image',
            field=models.ImageField(blank=True, default='bracket/static/default-team-img.jpg', null=True, upload_to='bracket/static/uploads'),
        ),
        migrations.AlterField(
            model_name='team',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(max_length=500)),
                ('name', models.TextField(max_length=200)),
                ('deadline', models.DateTimeField(default=datetime.datetime(2020, 11, 3, 1, 0))),
                ('teams', models.ManyToManyField(to='bracket.Team')),
            ],
        ),
    ]
