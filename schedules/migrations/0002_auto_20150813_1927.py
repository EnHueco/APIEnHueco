# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gap',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 27, 0, 993810)),
        ),
    ]
