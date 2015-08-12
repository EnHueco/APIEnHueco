# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gap',
            fields=[
                ('day', models.CharField(max_length=2)),
                ('start_hour', models.CharField(max_length=5)),
                ('end_hour', models.CharField(max_length=5)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 8, 12, 16, 42, 32, 870666))),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(primary_key=True, serialize=False, to='users.User')),
            ],
        ),
    ]
