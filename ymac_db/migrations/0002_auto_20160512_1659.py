# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-05-12 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ymac_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heritagesite',
            name='boundary_description',
            field=models.CharField(
                choices=[('Complete Accurate', 'Complete Accurate'), ('Incomplete Accurate', 'Incomplete Accurate'),
                         ('Complete Inferred', 'Complete Inferred'), ('Incomplete Inferred', 'Incomplete Inferred'),
                         ('Unknown', 'Unknown')], max_length=30),
        ),
        migrations.AlterField(
            model_name='heritagesite',
            name='disturbance_level',
            field=models.CharField(
                choices=[('Negligible', 'Negligible'), ('Minimal', 'Minimal'), ('Moderate', 'Moderate'),
                         ('Significant', 'Significant'), ('Major', 'Major')], max_length=30),
        ),
        migrations.AlterField(
            model_name='heritagesite',
            name='site_description',
            field=models.CharField(
                choices=[('Artefacts / Scatter', 'Artefacts / Scatter'), ('Birthplace', 'Birthplace'),
                         ('Ceremonial', 'Ceremonial'), ('Engravings', 'Engravings'),
                         ('Grinding Groove', 'Grinding Groove'), ('Gnamma Hole', 'Gnamma Hole'),
                         ('Mythological', 'Mythological')], max_length=30),
        ),
        migrations.AlterField(
            model_name='researchsite',
            name='site_category',
            field=models.CharField(blank=True, choices=[('GEOGRAPHIC FEATURES', 'GEOGRAPHIC FEATURES'), (
                'RESTRICTED OR CEREMONIAL SITE', 'RESTRICTED OR CEREMONIAL SITE'),
                                                        ('CAMPS/ LIVING AREAS', 'CAMPS/ LIVING AREAS')], max_length=30,
                                   null=True),
        ),
        migrations.AlterField(
            model_name='researchsite',
            name='site_classification',
            field=models.CharField(blank=True,
                                   choices=[('Ethnographic', 'Ethnographic'), ('Archeological', 'Archeological'),
                                            ('Arch & Ethno', 'Arch & Ethno')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='researchsite',
            name='site_location',
            field=models.CharField(blank=True,
                                   choices=[('Located', 'Located'), ('Position Indicative', 'Position Indicative'),
                                            ('Approximate', 'Approximate'), ('Unknown', 'Unknown')], max_length=30,
                                   null=True),
        ),
    ]
