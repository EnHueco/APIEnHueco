# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150813_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=2)),
                ('start_hour', models.CharField(max_length=5)),
                ('end_hour', models.CharField(max_length=5)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 26, 50, 335749))),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to='users.User')),
            ],
        ),
    ]
