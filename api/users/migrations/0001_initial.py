# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('father_name', models.CharField(max_length=255)),
                ('mother_name', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'verbose_name_plural': 'Details',
            },
        ),
        migrations.CreateModel(
            name='GlobalConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'token_exp', max_length=10)),
                ('value', models.TextField(default=b'60')),
            ],
            options={
                'verbose_name_plural': 'Global Config',
            },
        ),
    ]
