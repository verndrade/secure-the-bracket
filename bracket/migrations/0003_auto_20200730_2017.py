# Generated by Django 3.0.7 on 2020-07-30 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bracket', '0002_auto_20200730_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchup',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 6, 20, 17, 25, 104860)),
        ),
    ]