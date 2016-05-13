# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-05-12 08:40
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationDocsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'association_docs_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssociationExtSitesTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'association_ext_sites_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssociationSitesSurveyTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'association_sites_survey_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssociationSitesTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'association_sites_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DaaSite',
            fields=[
                ('id', models.FloatField(primary_key=True, serialize=False)),
                ('siteid', models.CharField(blank=True, max_length=30, null=True)),
                ('siteuniqid', models.FloatField(blank=True, null=True)),
                ('sitetoid', models.CharField(blank=True, max_length=50, null=True)),
                ('recordorg', models.CharField(blank=True, max_length=50, null=True)),
                ('svysqnceid', models.FloatField(blank=True, null=True)),
                ('sitename', models.CharField(blank=True, max_length=60, null=True)),
                ('atlsitenam', models.CharField(blank=True, max_length=60, null=True)),
                ('steident', models.CharField(blank=True, max_length=20, null=True)),
                ('sitecatid', models.CharField(blank=True, max_length=20, null=True)),
                ('recordby', models.CharField(blank=True, max_length=40, null=True)),
                ('daterecord', models.DateTimeField(blank=True, null=True)),
                ('complexnme', models.CharField(blank=True, max_length=50, null=True)),
                ('accssstat', models.CharField(blank=True, max_length=20, null=True)),
                ('siteclass', models.CharField(blank=True, max_length=25, null=True)),
                ('bndrytype', models.CharField(blank=True, max_length=25, null=True)),
                ('captaccy', models.CharField(blank=True, max_length=20, null=True)),
                ('dstblevel', models.CharField(blank=True, max_length=25, null=True)),
                ('sitedocs', models.CharField(blank=True, max_length=100, null=True)),
                ('comments', models.CharField(blank=True, max_length=254, null=True)),
                ('fldnotref', models.CharField(blank=True, max_length=50, null=True)),
                ('lbl_x_ll', models.FloatField(blank=True, null=True)),
                ('lbl_y_ll', models.FloatField(blank=True, null=True)),
                ('captdvc', models.CharField(blank=True, max_length=75, null=True)),
                ('capcordsys', models.CharField(blank=True, max_length=25, null=True)),
                ('datecreate', models.DateTimeField(blank=True, null=True)),
                ('createby', models.CharField(blank=True, max_length=50, null=True)),
                ('crrptid', models.CharField(blank=True, max_length=12, null=True)),
                ('section_5', models.CharField(blank=True, max_length=10, null=True)),
                ('spatialnte', models.CharField(blank=True, max_length=70, null=True)),
                ('bufdist_mr', models.FloatField(blank=True, null=True)),
                ('daasite_no', models.CharField(blank=True, max_length=15, null=True)),
                ('datemod', models.DateTimeField(blank=True, null=True)),
                ('modby', models.CharField(blank=True, max_length=50, null=True)),
                ('restsentve', models.CharField(blank=True, max_length=10, null=True)),
                ('locnrest', models.CharField(blank=True, max_length=15, null=True)),
                ('filerest', models.CharField(blank=True, max_length=15, null=True)),
                ('negbndy', models.CharField(blank=True, max_length=25, null=True)),
                ('rschmthlgy', models.CharField(blank=True, max_length=30, null=True)),
                ('agreareaid', models.CharField(blank=True, max_length=10, null=True)),
                ('agreetype', models.CharField(blank=True, max_length=50, null=True)),
                ('geom',
                 django.contrib.gis.db.models.fields.GeometryField(blank=True, geography=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'daa_sites',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataSuppliers',
            fields=[
                ('supplier', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'data_suppliers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalClientSite',
            fields=[
                ('external_id', models.AutoField(primary_key=True, serialize=False)),
                ('external_site_id', models.TextField(blank=True, null=True)),
                ('site_name', models.TextField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4283)),
            ],
            options={
                'db_table': 'external_client_sites',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HsRioCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_rac_table', models.CharField(blank=True, db_column='_rac_table', max_length=50, null=True)),
            ],
            options={
                'db_table': 'hs_rio_codes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HsSvmythlgy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('svy_meth', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'hs_svmythlgy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NnttDetermination',
            fields=[
                ('tribid', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('fcno', models.CharField(blank=True, max_length=254, null=True)),
                ('fcname', models.CharField(blank=True, max_length=250, null=True)),
                ('detbody', models.CharField(blank=True, max_length=100, null=True)),
                ('detdate', models.DateField(blank=True, null=True)),
                ('detregdate', models.DateField(blank=True, null=True)),
                ('detmethod', models.CharField(blank=True, max_length=100, null=True)),
                ('dettype', models.CharField(blank=True, max_length=100, null=True)),
                ('detoutcome', models.CharField(blank=True, max_length=70, null=True)),
                ('appealdesc', models.CharField(blank=True, max_length=40, null=True)),
                ('judge', models.CharField(blank=True, max_length=254, null=True)),
                ('rntbcname', models.CharField(blank=True, max_length=254, null=True)),
                ('nthold', models.CharField(blank=True, max_length=254, null=True)),
                ('relntda', models.CharField(blank=True, max_length=200, null=True)),
                ('detinfull', models.CharField(blank=True, max_length=1, null=True)),
                ('areasqkm', models.FloatField(blank=True, null=True)),
                ('datasource', models.CharField(blank=True, max_length=60, null=True)),
                ('datecurr', models.DateField(blank=True, null=True)),
                ('seadet', models.CharField(blank=True, max_length=1, null=True)),
                ('zonelwm', models.CharField(blank=True, max_length=1, null=True)),
                ('zone3nm', models.CharField(blank=True, max_length=1, null=True)),
                ('zone12nm', models.CharField(blank=True, max_length=1, null=True)),
                ('zone24nm', models.CharField(blank=True, max_length=1, null=True)),
                ('zoneeez', models.CharField(blank=True, max_length=1, null=True)),
                ('nnttseqno', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('objectind', models.CharField(blank=True, max_length=1, null=True)),
                ('sptialnote', models.CharField(blank=True, max_length=120, null=True)),
                ('link', models.CharField(blank=True, max_length=254, null=True)),
                ('juris', models.CharField(blank=True, max_length=10, null=True)),
                ('overlap', models.CharField(blank=True, max_length=20, null=True)),
                ('tribno', models.CharField(blank=True, max_length=20, null=True)),
                ('anthro', models.CharField(blank=True, max_length=200, null=True)),
                ('claimgroup', models.CharField(blank=True, max_length=200, null=True)),
                ('lawyer', models.CharField(blank=True, max_length=200, null=True)),
                ('ymacregion', models.CharField(blank=True, max_length=200, null=True)),
                ('hs_officer', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'nntt_determinations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Proponents',
            fields=[
                ('prop_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('contact', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'proponents',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RestrictionStatus',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.TextField(choices=[('Male', 'Male'), ('Female', 'Female')])),
                ('claim', models.NullBooleanField()),
            ],
            options={
                'db_table': 'restriction_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SampleMethodology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampling_meth', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'sample_methodology',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SamplingConfidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampling_conf', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'sampling_confidence',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('site_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_recorded', models.DateField(blank=True, null=True)),
                ('group_name', models.TextField(blank=True, null=True)),
                ('label_x_ll', models.FloatField(blank=True, null=True)),
                ('label_y_ll', models.FloatField(blank=True, null=True)),
                ('date_created', models.DateField(blank=True, null=True)),
                ('active', models.NullBooleanField()),
                ('capture_coord_sys', models.TextField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4283)),
            ],
            options={
                'db_table': 'sites',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SiteDocument',
            fields=[
                ('doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('document_type', models.TextField(
                    choices=[('Image', 'Image'), ('Audio', 'Audio'), ('Video', 'Video'), ('Document', 'Document'),
                             ('Map', 'Map'), ('Other', 'Other')])),
                ('filepath', models.TextField(blank=True, max_length=255, null=True)),
                ('filename', models.TextField(blank=True, max_length=-1, null=True)),
            ],
            options={
                'db_table': 'site_documents',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=8, null=True, unique=True)),
            ],
            options={
                'db_table': 'survey_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyTrip',
            fields=[
                ('survey_trip_id', models.AutoField(primary_key=True, serialize=False)),
                ('survey_id', models.CharField(blank=True, max_length=50, null=True)),
                ('trip_number', models.SmallIntegerField(blank=True, null=True)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'survey_trips',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.CharField(blank=True, max_length=4, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=25, null=True, unique=True)),
            ],
            options={
                'db_table': 'survey_types',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tenement',
            fields=[
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('survstatus', models.CharField(blank=True, max_length=15, null=True)),
                ('tenstatus', models.CharField(blank=True, max_length=10, null=True)),
                ('startdate', models.DateField(blank=True, null=True)),
                ('starttime', models.CharField(blank=True, max_length=8, null=True)),
                ('enddate', models.DateField(blank=True, null=True)),
                ('endtime', models.CharField(blank=True, max_length=8, null=True)),
                ('grantdate', models.DateField(blank=True, null=True)),
                ('granttime', models.CharField(blank=True, max_length=8, null=True)),
                ('fmt_tenid', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('legal_area', models.DecimalField(blank=True, decimal_places=15, max_digits=31, null=True)),
                ('special_in', models.CharField(blank=True, max_length=1, null=True)),
                ('extract_da', models.DateField(blank=True, null=True)),
                ('combined_r', models.CharField(blank=True, max_length=10, null=True)),
                ('all_holder', models.CharField(blank=True, max_length=254, null=True)),
                ('tribid', models.CharField(blank=True, max_length=200, null=True)),
                ('claim_groups', models.CharField(blank=True, max_length=200, null=True)),
                ('ymac_region', models.NullBooleanField()),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4283)),
            ],
            options={
                'db_table': 'tenement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='YmacClaim',
            fields=[
                ('tribid', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(blank=True, max_length=102, null=True)),
                ('fcno', models.CharField(blank=True, max_length=20, null=True)),
                ('datelodged', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('datestatus', models.DateField(blank=True, null=True)),
                ('rtstatus', models.CharField(blank=True, max_length=40, null=True)),
                ('datertdec', models.DateField(blank=True, null=True)),
                ('datereg', models.DateField(blank=True, null=True)),
                ('datentri', models.DateField(blank=True, null=True)),
                ('datenotncl', models.DateField(blank=True, null=True)),
                ('datefcord', models.DateField(blank=True, null=True)),
                ('combined', models.CharField(blank=True, max_length=1, null=True)),
                ('parentno', models.CharField(blank=True, max_length=12, null=True)),
                ('rep', models.CharField(blank=True, max_length=102, null=True)),
                ('casemgr', models.CharField(blank=True, max_length=25, null=True)),
                ('member', models.CharField(blank=True, max_length=254, null=True)),
                ('appltype', models.CharField(blank=True, max_length=50, null=True)),
                ('areasqkm', models.FloatField(blank=True, null=True)),
                ('datasource', models.CharField(blank=True, max_length=60, null=True)),
                ('datecurr', models.DateField(blank=True, null=True)),
                ('seaclaim', models.CharField(blank=True, max_length=1, null=True)),
                ('zonelwm', models.CharField(blank=True, max_length=1, null=True)),
                ('zone3nm', models.CharField(blank=True, max_length=1, null=True)),
                ('zone12nm', models.CharField(blank=True, max_length=1, null=True)),
                ('zone24nm', models.CharField(blank=True, max_length=1, null=True)),
                ('zoneeez', models.CharField(blank=True, max_length=1, null=True)),
                ('nnttseqno', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('objectind', models.CharField(blank=True, max_length=1, null=True)),
                ('sptialnote', models.CharField(blank=True, max_length=120, null=True)),
                ('juris', models.CharField(blank=True, max_length=10, null=True)),
                ('overlap', models.CharField(blank=True, max_length=20, null=True)),
                ('tribno', models.CharField(blank=True, max_length=10, null=True)),
                ('ymacregion', models.CharField(blank=True, max_length=200, null=True)),
                ('claimgroup', models.CharField(blank=True, max_length=200, null=True)),
                ('anthro', models.CharField(blank=True, max_length=200, null=True)),
                ('lawyer', models.CharField(blank=True, max_length=200, null=True)),
                ('hs_officer', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('claim_group_id', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'ymac_claims',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='YmacHeritageStaging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(blank=True, max_length=7, null=True)),
                ('survey_trip_id', models.IntegerField()),
                ('survey_id', models.CharField(blank=True, max_length=60, null=True)),
                ('trip_number', models.SmallIntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('claimgroup', models.TextField(blank=True, null=True)),
                ('survey_type', models.CharField(blank=True, max_length=25, null=True)),
                ('sampling_meth', models.CharField(blank=True, max_length=20, null=True)),
                ('sampling_conf', models.CharField(blank=True, max_length=60, null=True)),
                ('ymac_svy_name', models.CharField(blank=True, max_length=200, null=True)),
                ('survey_name', models.CharField(blank=True, max_length=200, null=True)),
                ('date_create', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('date_mod', models.DateField(blank=True, null=True)),
                ('mod_by', models.CharField(blank=True, max_length=50, null=True)),
                ('propref', models.CharField(blank=True, max_length=200, null=True)),
                ('data_supplier', models.CharField(blank=True, max_length=50, null=True)),
                ('data_qa', models.TextField(blank=True, null=True)),
                ('collected_by', models.CharField(blank=True, max_length=60, null=True)),
                ('rio_area_codes', models.TextField(blank=True, null=True)),
                ('survey_methodology', models.TextField(blank=True, null=True)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('modified_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'ymac_heritage_staging',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='YmacRegion',
            fields=[
                ('org', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('gazetted', models.DateField(blank=True, null=True)),
                ('effective', models.DateField(blank=True, null=True)),
                ('comments', models.CharField(blank=True, max_length=120, null=True)),
                ('juris', models.CharField(blank=True, max_length=20, null=True)),
                ('id', models.FloatField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'ymac_region',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='YmacStaff',
            fields=[
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('email', models.TextField(blank=True, null=True)),
                ('full_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('first_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ymac_staff',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ymacuser',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField(blank=True, null=True)),
                ('employee', models.NullBooleanField()),
                ('email', models.TextField(blank=True, null=True)),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ymacusers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HeritageSite',
            fields=[
                ('heritage_site_id', models.AutoField(primary_key=True, serialize=False)),
                ('site_description', models.TextField(
                    choices=[('Artefacts / Scatter', 'Artefacts / Scatter'), ('Birthplace', 'Birthplace'),
                             ('Ceremonial', 'Ceremonial'), ('Engravings', 'Engravings'),
                             ('Grinding Groove', 'Grinding Groove'), ('Gnamma Hole', 'Gnamma Hole'),
                             ('Mythological', 'Mythological')])),
                ('boundary_description', models.TextField(
                    choices=[('Complete Accurate', 'Complete Accurate'), ('Incomplete Accurate', 'Incomplete Accurate'),
                             ('Complete Inferred', 'Complete Inferred'), ('Incomplete Inferred', 'Incomplete Inferred'),
                             ('Unknown', 'Unknown')])),
                ('disturbance_level', models.TextField(
                    choices=[('Negligible', 'Negligible'), ('Minimal', 'Minimal'), ('Moderate', 'Moderate'),
                             ('Significant', 'Significant'), ('Major', 'Major')])),
                ('status', models.TextField(blank=True, null=True)),
                ('site_comments', models.TextField(blank=True, null=True)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ymac_db.Site')),
            ],
            options={
                'db_table': 'heritage_sites',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ResearchSite',
            fields=[
                ('research_site_id', models.AutoField(primary_key=True, serialize=False)),
                ('site_classification', models.TextField(blank=True, choices=[('Ethnographic', 'Ethnographic'),
                                                                              ('Archeological', 'Archeological'),
                                                                              ('Arch & Ethno', 'Arch & Ethno')],
                                                         null=True)),
                ('site_category', models.TextField(blank=True, choices=[('GEOGRAPHIC FEATURES', 'GEOGRAPHIC FEATURES'),
                                                                        ('RESTRICTED OR CEREMONIAL SITE',
                                                                         'RESTRICTED OR CEREMONIAL SITE'),
                                                                        ('CAMPS/ LIVING AREAS', 'CAMPS/ LIVING AREAS')],
                                                   null=True)),
                ('site_location', models.TextField(blank=True, choices=[('Located', 'Located'),
                                                                        ('Position Indicative', 'Position Indicative'),
                                                                        ('Approximate', 'Approximate'),
                                                                        ('Unknown', 'Unknown')], null=True)),
                ('site_comments', models.TextField(blank=True, null=True)),
                ('ethno_detail', models.TextField(blank=True, null=True)),
                ('reference', models.TextField(blank=True, null=True)),
                ('site_name', models.TextField(blank=True, null=True)),
                ('site_label', models.TextField(blank=True, null=True)),
                ('alt_site_name', models.TextField(blank=True, null=True)),
                ('site_number', models.IntegerField(blank=True, null=True)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                           to='ymac_db.Site')),
            ],
            options={
                'db_table': 'research_sites',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HeritageSurvey',
            fields=[
                ('survey_trip_id',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                      to='ymac_db.SurveyTrip')),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('proponent_id', models.CharField(blank=True, max_length=5, null=True)),
                ('claim_group_id', models.CharField(blank=True, max_length=5, null=True)),
                ('ymac_svy_name', models.CharField(blank=True, max_length=200, null=True)),
                ('survey_name', models.CharField(blank=True, max_length=200, null=True)),
                ('date_create', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('date_mod', models.DateField(blank=True, null=True)),
                ('mod_by', models.CharField(blank=True, max_length=200, null=True)),
                ('propref', models.CharField(blank=True, max_length=200, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=28350)),
                ('data_qa', models.BooleanField()),
                ('collected_by', models.CharField(blank=True, max_length=60, null=True)),
                ('data_supplier', models.OneToOneField(blank=True, db_column='data_supplier', null=True,
                                                       on_delete=django.db.models.deletion.CASCADE,
                                                       to='ymac_db.DataSuppliers')),
                ('heriage_sites',
                 models.ManyToManyField(through='ymac_db.AssociationSitesSurveyTable', to='ymac_db.Site')),
                ('sampling_conf', models.ForeignKey(blank=True, db_column='sampling_conf', default='Unknown', null=True,
                                                    on_delete=django.db.models.deletion.CASCADE,
                                                    to='ymac_db.SamplingConfidence')),
                ('sampling_meth', models.ForeignKey(blank=True, db_column='sampling_meth', default='UNKNOWN', null=True,
                                                    on_delete=django.db.models.deletion.CASCADE,
                                                    to='ymac_db.SampleMethodology')),
                ('status', models.ForeignKey(blank=True, db_column='status', null=True,
                                             on_delete=django.db.models.deletion.CASCADE, to='ymac_db.SurveyStatus')),
                ('survey_type', models.ForeignKey(blank=True, db_column='survey_type', null=True,
                                                  on_delete=django.db.models.deletion.CASCADE,
                                                  to='ymac_db.SurveyType')),
            ],
            options={
                'db_table': 'heritage_surveys',
                'managed': True,
            },
        ),
    ]
