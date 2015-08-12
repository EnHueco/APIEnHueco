# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 16, 42, 42, 754428)),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 16, 42, 42, 755278)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 16, 42, 42, 742959)),
        ),
    ]
