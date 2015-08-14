# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150813_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 27, 0, 941344)),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 27, 0, 942220)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 27, 0, 930673)),
        ),
    ]
