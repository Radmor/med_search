# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-22 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('source', models.TextField(blank=True, null=True)),
                ('seq', models.SmallIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('label', models.CharField(blank=True, max_length=256, null=True)),
                ('content', models.TextField()),
                ('truncated', models.BooleanField()),
            ],
            options={
                'managed': False,
                'db_table': 'sections',
            },
        ),
    ]