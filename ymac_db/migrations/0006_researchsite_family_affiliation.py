# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-05-13 02:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ymac_db', '0005_auto_20160512_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchsite',
            name='family_affiliation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
