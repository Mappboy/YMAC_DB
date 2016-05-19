# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-05-19 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ymac_db', '0002_auto_20160519_1337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='daasite',
            options={'managed': False, 'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='site',
            name='site_identifier',
            field=models.CharField(blank=True, help_text='Site name to help you identify it', max_length=200,
                                   null=True),
        ),
    ]
