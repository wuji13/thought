# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-05 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thought', '0004_auto_20180606_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussone',
            name='content',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='discusstwo',
            name='content',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='thought',
            name='content',
            field=models.TextField(max_length=8192),
        ),
    ]