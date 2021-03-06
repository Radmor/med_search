# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-22 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abstracts',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('source', models.TextField(blank=True, null=True)),
                ('copyright', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'abstracts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Citations',
            fields=[
                ('pmid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('status', models.TextField()),
                ('year', models.SmallIntegerField()),
                ('title', models.TextField()),
                ('journal', models.CharField(max_length=256)),
                ('pub_date', models.CharField(max_length=256)),
                ('issue', models.CharField(blank=True, max_length=256, null=True)),
                ('pagination', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateField()),
                ('completed', models.DateField(blank=True, null=True)),
                ('revised', models.DateField(blank=True, null=True)),
                ('modified', models.DateField()),
            ],
            options={
                'db_table': 'citations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Databases',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('accession', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'databases',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Descriptors',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('num', models.SmallIntegerField(blank=True, null=True)),
                ('major', models.BooleanField()),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'descriptors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Identifiers',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('namespace', models.CharField(blank=True, max_length=32, null=True)),
                ('value', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'identifiers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('owner', models.TextField(blank=True, null=True)),
                ('cnt', models.SmallIntegerField(blank=True, null=True)),
                ('major', models.BooleanField()),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'keywords',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PublicationTypes',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'publication_types',
                'managed': False,
            },
        ),
    ]
