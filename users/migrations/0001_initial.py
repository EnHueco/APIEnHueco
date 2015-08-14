# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastUpdated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastUpdated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('login', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('firstNames', models.CharField(max_length=50)),
                ('lastNames', models.CharField(max_length=50)),
                ('imageURL', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastUpdated_on', models.DateTimeField(auto_now=True)),
                ('friends', models.ManyToManyField(related_name='friends+', through='users.Friendship', to='users.User')),
                ('requests_sent', models.ManyToManyField(related_name='requests_received', through='users.FriendRequest', to='users.User')),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='firstUser',
            field=models.ForeignKey(related_name='+', to='users.User'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='secondUser',
            field=models.ForeignKey(related_name='+', to='users.User'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='fromUser',
            field=models.ForeignKey(related_name='+', to='users.User'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='toUser',
            field=models.ForeignKey(related_name='+', to='users.User'),
        ),
    ]
