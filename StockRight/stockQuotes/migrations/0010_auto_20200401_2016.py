# Generated by Django 3.0.4 on 2020-04-02 02:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockQuotes', '0009_auto_20200401_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='added_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 20, 16, 46, 809624)),
        ),
    ]
