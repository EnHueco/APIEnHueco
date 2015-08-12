# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 16, 42, 42, 767810)),
        ),
    ]
