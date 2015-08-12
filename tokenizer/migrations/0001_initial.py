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
            name='Token',
            fields=[
                ('value', models.CharField(max_length=256)),
                ('owner', models.ForeignKey(primary_key=True, serialize=False, to='users.User')),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 8, 12, 16, 42, 32, 831957))),
            ],
        ),
        migrations.CreateModel(
            name='Tokenizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
    ]
