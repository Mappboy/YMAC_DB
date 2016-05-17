# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-05-17 07:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ymac_db', '0017_auto_20160517_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heritagesurvey',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='created_user', to='ymac_db.SiteUser'),
        ),
        migrations.AlterField(
            model_name='heritagesurvey',
            name='mod_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='mod_user', to='ymac_db.SiteUser'),
        ),
    ]