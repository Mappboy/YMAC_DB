from __future__ import unicode_literals

import datetime
from os import path

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text
from django.utils.html import format_html

from .validators import *

VALID_DRIVES = [
    "X:",
    "V:",
    "W:",
    "Z:",
    "K:",
    "\\\\ymac-dc3-fs1\\spatial_wkg",
    "\\\\ymac-dc3-fs1\\spatial_data",
    "\\\\ymac-dc3-fs1\\spatial_pub",
    "\\\\ymac-dc3-fs1\\heritage",
    "\\\\ymac-dc3-fs1\\research",

]

boundary_description = [('Complete Accurate', 'Complete Accurate'),
                        ('Incomplete Accurate', 'Incomplete Accurate'),
                        ('Complete Inferred', 'Complete Inferred'),
                        ('Incomplete Inferred', 'Incomplete Inferred'),
                        ('Unknown', 'Unknown')]

disturbance_level = [('Negligible', 'Negligible'),
                     ('Minimal', 'Minimal'),
                     ('Moderate', 'Moderate'),
                     ('Significant', 'Significant'),
                     ('Major', 'Major')
                     ]

site_location = [('Located', 'Located'),
                 ('Position Indicative', 'Position Indicative'),
                 ('Approximate', 'Approximate'),
                 ('Unknown', 'Unknown')
                 ]
# TODO: Consider making this a site table

site_description = [
    ('Artefacts / Scatter', 'Artefacts / Scatter'),
    ('Birthplace', 'Birthplace'),
    ('Ceremonial', 'Ceremonial'),
    ('Engravings', 'Engravings'),
    ('Grinding Patch', 'Grinding Patch'),
    ('Gnamma Hole', 'Gnamma Hole'),
    ('Mythological', 'Mythological'),
]

her_site_status = [
    ('Protected', 'Protected'),
    ('Cleared', 'Cleared'),
    ('Restricted', 'Restricted'),
    ('Provisional', 'Provisional'),
    ('Stored Data', 'Stored Data')
]

site_category = [('Ethnographic', 'Ethnographic'),
                       ('Archeological', 'Archeological'),
                       ('Arch & Ethno', 'Arch & Ethno')
                       ]

gender = [('Male', 'Male'),
          ('Female', 'Female')]

document_type = [('Image', 'Image'),
                 ('Audio', 'Audio'),
                 ('Video', 'Video'),
                 ('Document', 'Document'),
                 ('Spatial', 'Spatial'),
                 ('Map', 'Map'),
                 ('Other', 'Other')
                 ]

document_subtype = [
    ('GPX', 'GPX'),
    ('Shapefile', 'Shapefile'),
    ('Mapinfo', 'Mapinfo'),
    ('Geodatabase', 'Geodatabase'),
    ('Google KML', 'Google KML'),
    ('Preliminary Advice', 'Preliminary Advice'),
    ('Survey Report', 'Survey Report'),
    ('HISF', 'Heritage Information Submission Form'),
    ('Zipped', 'Zipped'),
]

states = [
    ('WA', 'WA'),
    ('NSW', 'NSW'),
    ('ACT', 'ACT'),
    ('SA', 'SA'),
    ('QLD', 'QLD'),
    ('TAS', 'TAS'),
    ('VIC', 'VIC'),
    ('NT', 'NT'),
]

survey_methodology = [
    ("Excavation", "Excavation"),
    ("Monitoring", "Monitoring"),
    ("RAB Drilling", "RAB Drilling"),
    ("Reconnaissance", "Reconnaissance"),
    ("Salvage", "Salvage"),
    ("Section 16", "Section 16"),
    ("Section 18", "Section 18"),
    ("Site Avoidance", "Site Avoidance"),
    ("Site Assessment", "Site Assessment"),
    ("Site ID", "Site ID"),
    ("Work Area Clearance", "Work Area Clearance"),
    ("Work Program Clearance", "Work Program Clearance"),
]

project_status = [
    ("On Hold", "On Hold"),
    ("In Progress", "In Progress"),
    ("Date Set", "Date Set"),
    ("Proposed Date", "Proposed Date"),
    ("Cancelled", "Cancelled"),
    ("Completed", "Completed"),
    ("Postponed", "Postponed"),
    ("Heritage Notice Recd", "Heritage Notice Recd"),
    ("PA Received", "PA Received"),
    ("PA Sent to Proponent", "PA Sent to Proponent"),
    ("Draft Report Received", "Draft Report Received"),
    ("Final Report Received", "Final Report Received"),
    ("Field Work Completed", "Field Work Completed"),
    ("Unknown", "Unknown"),
]

ymac_region = [
    ("Pilbara", "Pilbara"),
    ("Yamatji", "Yamatji"),
    ("Both", "Both"),
]

path_type = [
    ("Spatial File", "Spatial File"),
    ("Directory", "Directory"),
    ("Survey Report", "Survey Report"),
    ("Photo", "Photo"),
    ("Prelim Advice", "Prelim Advice"),
    ("HISF", "HISF"),
]

group_status = [
    ('Represented', 'Represented'),
    ('Discontinued', 'Discontinued'),
]

departments = [
    ('Research', 'Research'),
    ('Heritage', 'Heritage'),
    ('Legal', 'Legal'),
    ('Future Acts', 'Future Acts'),
    ('Communications', 'Communications'),
    ('Finance', 'Finance'),
    ('Knowledge Partnerships', 'Knowledge Partnerships'),
    ('Other', 'Other'),
]

map_sizes = [
    ('A0', 'A0'),
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('A3', 'A3'),
    ('A4', 'A4'),
    ('Other', 'Other (Please describe in Other Instructions)'),
]

product_types = [
    ('Digital only', 'Digital only'),
    ('Hard Copy Posted', 'Hard Copy Posted'),
    ('Digital and Hard Copy', 'Digital and Hard Copy'),
    ('Other (please specify below)', 'Other (please specify below)'),
]

cost_centres = [
    ('DPMC', 'DPMC'),
    ('Cost Recovery', 'Cost Recovery'),
    ('Non DPMC/Non Cost Recovery', 'Non DPMC/Non Cost Recovery'),
]

urgency = [
    ("High Urgent", "High Urgent"),
    ("High NOT Urgent", "High NOT Urgent"),
    ("Medium Urgent", "Medium Urgent"),
    ("Medium NOT Urgent", "Medium NOT Urgent"),
    ("Low Urgent", "Low Urgent"),
    ("Low NOT Urgent", "Low NOT Urgent"),
]

offices = [
    ('Perth', 'Perth'),
    ('Geraldton', 'Geraldton'),
    ('South Hedland', 'South Hedland'),
    ('Tom Price', 'Tom Price'),
    ('Karratha', 'Karratha'),
    ('Pilbara', 'Pilbara'),
]

available_projections = [
    (4326, 'WGS84 LL'),
    (4283, 'GDA94 LL'),
    (4203, 'AGD84 LL'),
    (4202, 'AGD66 LL'),
    (28349, 'MGA Zone 49'),
    (28350, 'MGA Zone 50'),
    (28351, 'MGA Zone 51'),
    (28352, 'MGA Zone 52'),
    (32749, 'UTM Zone 49'),
    (32750, 'UTM Zone 50'),
    (32751, 'UTM Zone 51'),
    (32752, 'UTM Zone 52'),
    (20349, 'AGD84/ Zone 49'),
    (20350, 'AGD84/ Zone 50'),
    (20351, 'AGD84/ Zone 51'),
    (20352, 'AGD84/ Zone 52'),
    (20249, 'AGD66/ Zone 49'),
    (20250, 'AGD66/ Zone 50'),
    (20251, 'AGD66/ Zone 51'),
    (20252, 'AGD66/ Zone 52'),
]


@python_2_unicode_compatible
class Consultant(models.Model):
    """
    Survey Consultants
    """
    name = models.CharField(max_length=70, blank=True, null=True, db_index=True)
    employee = models.NullBooleanField()
    company = models.ForeignKey('CaptureOrg', blank=True, null=True, db_index=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        if self.name:
            return smart_text(self.name)
        else:
            return smart_text("Employee of {}".format(self.company))

    class Meta:
        managed = False
        ordering = ('name',)


@python_2_unicode_compatible
class CaptureOrg(models.Model):
    organisation_name = models.TextField(db_index=True)
    organisation_contact = models.CharField(max_length=100, blank=True, null=True, help_text="Main Contact Name")
    organisation_email = models.EmailField(blank=True, null=True, help_text="Main Contact Email")
    organisation_phone = models.CharField(max_length=16, blank=True, null=True)
    organisation_address = models.TextField(blank=True, null=True)
    organisation_suburb = models.TextField(blank=True, null=True)
    organisation_state = models.CharField(max_length=3, blank=True, null=True, choices=states)
    organisation_postcode = models.IntegerField(blank=True, null=True)
    organisation_website = models.URLField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.organisation_name)

    class Meta:
        managed = False
        db_table = 'ymac_db_captureorg'


@python_2_unicode_compatible
class DaaSite(models.Model):
    id = models.AutoField(primary_key=True)
    place_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    legacy_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    status_reason = models.CharField(max_length=200, blank=True, null=True)
    origin_place_id = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    restrictions = models.CharField(max_length=200, blank=True, null=True)
    file_restricted = models.CharField(max_length=200, blank=True, null=True)
    location_restricted = models.CharField(max_length=200, blank=True, null=True)
    boundary_reliable = models.CharField(max_length=200, blank=True, null=True)
    protected_area = models.CharField(max_length=200, blank=True, null=True)
    protected_area_gazetted_date = models.CharField(max_length=200, blank=True, null=True)
    national_estate_area = models.CharField(max_length=200, blank=True, null=True)
    duplicate_id = models.CharField(max_length=200, blank=True, null=True)
    boundary_last_update_date = models.CharField(max_length=200, blank=True, null=True)
    shape_length = models.CharField(max_length=200, blank=True, null=True)
    shape_area = models.CharField(max_length=200, blank=True, null=True)
    objectid = models.BigIntegerField(blank=True, null=True)
    # source
    # file location
    # daa report
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        ordering = ('name',)
        db_table = 'daa_sites_new'
        verbose_name = 'DAA Site'
        verbose_name_plural = 'DAA Sites'
        unique_together = (('place_id', 'id'),)


class DaaSiteHistory(models.Model):
    place_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200, blank=True, null=True)
    legacy_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    status_reason = models.CharField(max_length=200, blank=True, null=True)
    origin_place_id = models.CharField(max_length=200, blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    restrictions = models.CharField(max_length=200, blank=True, null=True)
    file_restricted = models.CharField(max_length=200, blank=True, null=True)
    location_restricted = models.CharField(max_length=200, blank=True, null=True)
    boundary_reliable = models.CharField(max_length=200, blank=True, null=True)
    protected_area = models.CharField(max_length=200, blank=True, null=True)
    protected_area_gazetted_date = models.DateField(blank=True, null=True)
    national_estate_area = models.CharField(max_length=200, blank=True, null=True)
    duplicate_id = models.CharField(max_length=200, blank=True, null=True)
    boundary_last_update_date = models.DateField(blank=True, null=True)
    shape_length = models.CharField(max_length=200, blank=True, null=True)
    shape_area = models.CharField(max_length=200, blank=True, null=True)
    ymac_update = models.CharField(max_length=200, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)
    modified_time = models.DateTimeField()
    operation = models.CharField(max_length=20)
    area_difference = models.FloatField(blank=True, null=True)
    geom_change = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'daa_site_history'
        unique_together = (('place_id', 'operation', 'modified_time'),)


@python_2_unicode_compatible
class DataSuppliers(models.Model):
    supplier = models.CharField(primary_key=True, max_length=50, db_index=True)

    def __str__(self):
        return smart_text(self.supplier)

    class Meta:
        managed = False
        db_table = 'data_suppliers'


@python_2_unicode_compatible
class Department(models.Model):
    name = models.CharField(max_length=25, choices=departments, db_index=True)
    head = models.ForeignKey('YmacStaff')

    def __str__(self):
        return smart_text(self.name)


@python_2_unicode_compatible
class DocumentType(models.Model):
    document_type = models.CharField(max_length=15, db_index=True, choices=document_type)
    sub_type = models.CharField(max_length=40, db_index=True, choices=document_subtype, blank=True, null=True)

    def __str__(self):
        doc_string = "%s : %s" % (self.document_type, self.sub_type) if self.sub_type else "%s" % (self.document_type)
        return smart_text(doc_string)


@python_2_unicode_compatible
class Emit(models.Model):
    title = models.CharField(primary_key=True, max_length=20)
    content = models.TextField(blank=True, null=True)
    id = models.TextField(blank=True, null=True)
    publisheddate = models.TextField(blank=True, null=True)
    linkuri = models.TextField(blank=True, null=True)
    field_minfield = models.CharField(db_column='_minfield', max_length=200, blank=True,
                                      null=True)  # Field renamed because it started with '_'.
    possibleclaimgroups = models.CharField(max_length=200, blank=True, null=True)
    datereceived = models.DateField()
    markout = models.CharField(max_length=200, blank=True, null=True)
    area = models.CharField(max_length=200, blank=True, null=True)
    shire = models.CharField(max_length=200, blank=True, null=True)
    applicants = models.CharField(max_length=200, blank=True, null=True)
    objectiondate = models.CharField(max_length=200, blank=True, null=True)
    miningregistrar = models.CharField(max_length=200, blank=True, null=True)
    tenement = models.ForeignKey('TenementsAll', blank=True, null=True)

    def __str__(self):
        return smart_text(self.title)

    class Meta:
        managed = True
        db_table = 'emit'


@python_2_unicode_compatible
class ExternalClientSite(models.Model):
    external_id = models.AutoField(primary_key=True)
    external_site_id = models.TextField(blank=True, null=True)
    site_name = models.TextField(blank=True, null=True, db_index=True)
    geom = models.PolygonField(srid=4283)

    def __str__(self):
        return smart_text(self.site_name)

    class Meta:
        managed = False
        db_table = 'external_client_sites'


@python_2_unicode_compatible
class FileCleanUp(models.Model):
    """
    Will clean up all these files after approval
    """
    data_path = models.TextField(db_index=True)
    submitted_user = models.ForeignKey(User)

    def __str__(self):
        return smart_text(self.data_path)


# Status like
# Site Category
# Proponent???
# Site Centroid ???
# WHAT TO DO ABOUT Tracks
# Datum to read in
@python_2_unicode_compatible
class HeritageSite(models.Model):
    site_description = models.ForeignKey('SiteDescriptions', blank=True, null=True)
    boundary_description = models.CharField(max_length=30, choices=boundary_description, blank=True, null=True)
    disturbance_level = models.CharField(max_length=30, choices=disturbance_level, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True, choices=her_site_status)
    site_comments = models.TextField(blank=True, null=True)
    heritage_surveys = models.ManyToManyField('HeritageSurvey',
                                              related_name='her_sites',
                                              )
    recorded_by = models.ForeignKey('SiteUser', on_delete=models.DO_NOTHING, db_column='recorded_by',
                                    related_name='herritage_recorded_by', blank=True, null=True)
    date_recorded = models.DateField(blank=True, null=True)
    group_name = models.TextField(blank=True, null=True, help_text="Is this site part of a group of sites or complex?")
    site_identifier = models.CharField(max_length=200, blank=True, null=True,
                                       help_text="Site name to help you identify it", db_index=True)
    restricted_status = models.ForeignKey('RestrictionStatus', on_delete=models.DO_NOTHING, db_column='restricted_status',
                                          blank=True, null=True)
    date_created = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('SiteUser', on_delete=models.DO_NOTHING, db_column='created_by',
                                   related_name='heritage_created_by', blank=True)
    orig_x_val = models.FloatField(blank=True, null=True, help_text="Latitude/Northing Value")
    orig_y_val = models.FloatField(blank=True, null=True, help_text="Longitude/Easting Value")
    buffer = models.IntegerField(default=10, help_text="Site buffer in meters")
    coordinate_accuracy = models.CharField(max_length=30, choices=site_location, blank = True, null = True)
    active = models.NullBooleanField()
    capture_coord_sys = models.IntegerField(choices=available_projections, blank=True, null=True)
    label_x_ll = models.FloatField(blank=True, null=True, help_text="Used for setting labels in qgis")
    label_y_ll = models.FloatField(blank=True, null=True, help_text="Used for setting labels in qgis")
    documents = models.ManyToManyField('SiteDocument', blank=True)
    surveys = models.ManyToManyField('HeritageSurvey', blank=True)
    daa_sites = models.ManyToManyField('DaaSite', blank=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        if self.site_identifier:
            return smart_text(self.site_identifier)
        return smart_text("Site {}".format(self.site_id))

    class Meta:
        managed = True


@python_2_unicode_compatible
class HeritageSurvey(models.Model):
    survey_id = models.CharField(max_length=10, validators=[valid_surveyid], db_index=True)
    original_ymac_id = models.CharField(max_length=50, blank=True, null=True)
    related_surveys = models.ManyToManyField('RelatedSurveyCode', blank=True)
    trip_number = models.SmallIntegerField(blank=True, null=True, db_index=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    data_status = models.ForeignKey('SurveyStatus',on_delete=models.DO_NOTHING, blank=True, null=True, db_index=True,
                                    help_text="For current spatial data is"
                                              " it proposed or after survey completion (Actual)")
    data_source = models.ManyToManyField('SurveyCleaning', blank=True, related_name="surveys",
                                         help_text="Any comments or data relating to the data")
    survey_type = models.ForeignKey('SurveyType', on_delete=models.DO_NOTHING, db_column='survey_type', blank=True,
                                    null=True)
    survey_methodologies = models.ManyToManyField('SurveyMethodology', db_index=True, blank=True)
    survey_group = models.ForeignKey('SurveyGroup', on_delete=models.DO_NOTHING,db_index=True, blank=True, null=True)
    proponent = models.ForeignKey('Proponent', on_delete=models.DO_NOTHING, blank=True, null=True)
    proponent_codes = models.ManyToManyField('SurveyProponentCode', db_index=True, blank=True,
                                             help_text="Any proponent codes relating to the survey"
                                                       " i.e RIO Area Codes AR-00-00000")
    sampling_meth = models.ForeignKey('SampleMethodology', db_index=True, db_column='sampling_meth',
                                      on_delete=models.DO_NOTHING, default=6, blank=True, null=True)
    sampling_conf = models.ForeignKey('SamplingConfidence', db_index=True, on_delete=models.DO_NOTHING, default=5,
                                      blank=True, null=True)
    project_name = models.TextField(blank=True, db_index=True, null=True, help_text="Internal or Survey Project Name")
    project_status = models.CharField(max_length=25, db_index=True, default="Unknown", choices=project_status, blank=True,
                                      null=True)
    survey_region = models.CharField(max_length=15, choices=ymac_region, blank=True, null=True)
    survey_description = models.TextField(blank=True, null=True,
                                          help_text="Description of the proposed or actual survey")
    survey_note = models.TextField(blank=True, null=True, help_text="Additional Survey notes")
    created_by = models.ForeignKey('SiteUser',on_delete=models.DO_NOTHING, db_index=True, related_name='created_user', blank=True, null=True)
    date_create = models.DateField(blank=True, null=True, default=datetime.date.today)
    mod_by = models.ForeignKey('SiteUser', db_index=True, related_name='mod_user', blank=True, null=True)
    date_mod = models.DateField(blank=True, null=True, default=datetime.date.today)
    data_qa = models.BooleanField(default=False, help_text="Has Actual data been checked by Spatial Team")
    spatial_data_exists = models.BooleanField(default=False,
                                              help_text="Do we know if there is actually spatial data for the survey?")
    consultants = models.ManyToManyField('Consultant', db_index=True, blank=True, help_text="Consultants for survey")
    documents = models.ManyToManyField('SurveyDocument', db_index=True, blank=True, related_name="surveys",
                                       help_text="Related documents")
    folder_location = models.TextField(blank=True, db_index=True,
                                       help_text="Location on Z drive of folder")  # validators=[valid_directory]
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        if self.survey_id:
            return smart_text(
                "{} (Trip {})- {}".format(self.survey_id, self.trip_number, self.project_name))
        return smart_text(self.project_name)

    @property
    def popupContent(self):
        return format_html('<p><Survey Id:{}<br\>Survey Description: {}</p>',
                           self.survey_id,
                           self.survey_description)


    class Meta:
        managed = True
        ordering = ('survey_id', 'date_create',)
        index_together = ['survey_id', 'trip_number']
        unique_together = ['survey_id', 'trip_number']


@python_2_unicode_compatible
class HeritageSurveyData(models.Model):
    survey = models.ForeignKey('HeritageSurvey', help_text="The survey to which the data relates to")
    survey_part = models.IntegerField(help_text="Polygon number for survey, must be unique")
    survey_document = models.ForeignKey('SurveyDocument', help_text="The Document where the data comes from")
    label = models.TextField(blank=True, null=True, help_text="If the data should be labelled")
    notes = models.TextField(blank=True, null=True, help_text="Any notes attached to the data")
    geom = models.PolygonField(srid=4283)

    def __str__(self):
        return "Survey Data for {}".format(self.survey)


@python_2_unicode_compatible
class HeritageCompanies(models.Model):
    """
    Companies who Heritage Surveys have been performed for.
    """
    old_code = models.IntegerField(unique=True)
    company_name = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    class Meta:
        managed = False

    def __str__(self):
        return smart_text("Company {}".format(self.company_name))

class InformantManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

@python_2_unicode_compatible
class SiteInformant(models.Model):
    """
    Site informants
    """
    objects = InformantManager()
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return smart_text(self.name)

    def natural_key(self):
        return (self.name)

    class Meta:
        managed = True
        unique_together = ('name',)


@python_2_unicode_compatible
class NnttDetermination(models.Model):
    tribid = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True, db_index=True)
    fcno = models.CharField(max_length=254, blank=True, null=True)
    fcname = models.CharField(max_length=250, blank=True, null=True)
    detbody = models.CharField(max_length=100, blank=True, null=True)
    detdate = models.DateField(blank=True, null=True)
    detregdate = models.DateField(blank=True, null=True)
    detmethod = models.CharField(max_length=100, blank=True, null=True)
    dettype = models.CharField(max_length=100, blank=True, null=True)
    detoutcome = models.CharField(max_length=70, blank=True, null=True)
    appealdesc = models.CharField(max_length=40, blank=True, null=True)
    judge = models.CharField(max_length=254, blank=True, null=True)
    rntbcname = models.CharField(max_length=254, blank=True, null=True)
    nthold = models.CharField(max_length=254, blank=True, null=True)
    relntda = models.CharField(max_length=200, blank=True, null=True)
    detinfull = models.CharField(max_length=1, blank=True, null=True)
    areasqkm = models.FloatField(blank=True, null=True)
    datasource = models.CharField(max_length=60, blank=True, null=True)
    datecurr = models.DateField(blank=True, null=True)
    seadet = models.CharField(max_length=1, blank=True, null=True)
    zonelwm = models.CharField(max_length=1, blank=True, null=True)
    zone3nm = models.CharField(max_length=1, blank=True, null=True)
    zone12nm = models.CharField(max_length=1, blank=True, null=True)
    zone24nm = models.CharField(max_length=1, blank=True, null=True)
    zoneeez = models.CharField(max_length=1, blank=True, null=True)
    nnttseqno = models.CharField(primary_key=True, max_length=14)
    objectind = models.CharField(max_length=1, blank=True, null=True)
    sptialnote = models.CharField(max_length=120, blank=True, null=True)
    link = models.CharField(max_length=254, blank=True, null=True)
    juris = models.CharField(max_length=10, blank=True, null=True)
    overlap = models.CharField(max_length=20, blank=True, null=True)
    tribno = models.CharField(max_length=20, blank=True, null=True)
    anthro = models.CharField(max_length=200, blank=True, null=True)
    claimgroup = models.CharField(max_length=200, blank=True, null=True)
    lawyer = models.CharField(max_length=200, blank=True, null=True)
    hs_officer = models.CharField(max_length=200, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        return smart_text(self.name.strip())

    class Meta:
        managed = False
        db_table = 'nntt_determinations'


@python_2_unicode_compatible
class PotentialSurvey(models.Model):
    """
    These are cleaning comments and data paths that can be attached
    to a heritage survey.
    """
    survey_id = models.CharField(max_length=15)
    data_path = models.TextField(blank=False, null=False)
    path_type = models.CharField(max_length=15, blank=True, null=False, choices=path_type)

    class Meta:
        managed = True

    def __str__(self):
        name = self.data_path if self.data_path else self.cleaning_comment
        return smart_text("Cleaning Item {}".format(name))


@python_2_unicode_compatible
class Proponent(models.Model):
    id = models.AutoField(primary_key=True)
    prop_id = models.CharField(max_length=40)
    name = models.TextField(db_index=True)
    contact = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        managed = True
        ordering = ('name',)


@python_2_unicode_compatible
class RelatedSurveyCode(models.Model):
    rel_survey_id = models.CharField(max_length=10, db_index=True)

    class Meta:
        managed = False

    def __str__(self):
        return smart_text(self.rel_survey_id)


@python_2_unicode_compatible
class ResearchSite(models.Model):
    #       - Import Tool https://docs.djangoproject.com/en/1.10/ref/contrib/gis/geos/
    #       - Conversions https://docs.djangoproject.com/en/1.10/ref/contrib/gis/gdal/
    research_site_id = models.AutoField(primary_key=True)
    site_type = models.ManyToManyField('SiteType', help_text="Pick match site types or add a new one")
    site_location_desc = models.TextField(blank=True, null=True, help_text="If need, provide a site description")
    site_other_coordinates = models.TextField(blank=True, null=True, help_text="Any other coordinates for the site")
    groups = models.ManyToManyField('YmacClaim', help_text="Site belong to any groups")
    informants = models.ManyToManyField('SiteInformant', blank=True, help_text="Site belong to any groups")
    proponent_codes = models.TextField(blank=True, null=True, help_text="Any proponent codes for matching")
    site_comments = models.TextField(blank=True, null=True)
    ethno_detail = models.TextField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True, help_text="Field Notes")
    site_name = models.TextField(blank=True, unique=True, null=True, db_index=True)
    site_label = models.TextField(blank=True, null=True)
    alt_site_name = models.TextField(blank=True, null=True)
    site_number = models.IntegerField(blank=True, null=True)
    family_affiliation = models.TextField(blank=True, null=True, help_text="The family that speaks for that site")
    mapsheet = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey('SiteUser', on_delete=models.DO_NOTHING, db_column='recorded_by',
                                    related_name='research_recorded_by', blank=True, null=True)
    date_recorded = models.DateField(blank=True, null=True)
    group_name = models.TextField(blank=True, null=True, help_text="Is this site part of a group of sites or complex?")
    restricted_status = models.ForeignKey('RestrictionStatus', on_delete=models.DO_NOTHING, db_column='restricted_status',
                                          blank=True, null=True)

    date_created = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('SiteUser', on_delete=models.DO_NOTHING, db_column='created_by',
                                   related_name='research_created_by', blank=True)
    orig_x_val = models.FloatField(blank=True, null=True, help_text="Latitude/Northing Value")
    orig_y_val = models.FloatField(blank=True, null=True, help_text="Longitude/Easting Value")
    buffer = models.IntegerField(default=10, help_text="Site buffer in meters")
    coordinate_accuracy = models.CharField(max_length=30, choices=site_location, blank = True, null = True)
    active = models.NullBooleanField()
    capture_coord_sys = models.IntegerField(choices=available_projections, blank=True, null=True)
    label_x_ll = models.FloatField(blank=True, null=True, help_text="Used for setting labels in qgis")
    label_y_ll = models.FloatField(blank=True, null=True, help_text="Used for setting labels in qgis")
    documents = models.ManyToManyField('SiteDocument', blank=True)
    daa_sites = models.ManyToManyField('DaaSite', blank=True)
    geom = models.PolygonField(srid=4283, blank=True, null=True)

    def __str__(self):
        return smart_text("Research Site {} ".format(self.site_name))

    class Meta:
        managed = True


@python_2_unicode_compatible
class RestrictionStatus(models.Model):
    rid = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=12, choices=gender, blank=True, null=True, db_index=True)
    claim = models.NullBooleanField(blank=True, null=True, db_index=True)

    def __str__(self):
        if self.claim and self.gender:
            status = "Gender Restricted {} and Claim Restricted".format(self.gender)
        elif self.claim and not self.gender:
            status = "Claim Restricted"
        elif self.gender and not self.claim:
            status = "Gender Restriced {}".format(self.gender)
        else:
            status = "No Restrictions"
        return smart_text(status)

    class Meta:
        managed = False
        db_table = 'restriction_status'
        verbose_name_plural = "Restriction Status"


@python_2_unicode_compatible
class RequestUser(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField()
    department = models.ForeignKey('Department')
    office = models.CharField(max_length=20, choices=offices, default="Perth")
    current_user = models.BooleanField(default=True)

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        ordering = ('name',)


@python_2_unicode_compatible
class RequestType(models.Model):
    name = models.CharField(max_length=45, db_index=True)

    def __str__(self):
        return smart_text(self.name)


@python_2_unicode_compatible
class SiteDocument(models.Model):
    doc_id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=15, choices=document_type)  # This field type is a guess.
    filepath = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    def check_file_exists(self):
        """
        Check file is on one of our drives and not local.
        Also check if file actually exists
        :return:
        """
        fp = path.join(self.filepath, self.filename)
        drive = path.splitdrive(fp)[0] if not path.splitdrive(fp) else path.splitdrive(fp)[0]
        if drive not in VALID_DRIVES:
            return smart_text("Can't find Drive")
        if not path.isfile(fp):
            return smart_text("File does not exist")

    def __str__(self):
        return smart_text(self.filename)

    class Meta:
        managed = False
        db_table = 'site_documents'


class SiteTypeManager(models.Manager):
    def get_by_natural_key(self, site_classification, site_category):
        return self.get(site_classification=site_classification, site_category=site_category)

@python_2_unicode_compatible
class SiteType(models.Model):
    objects = SiteTypeManager()
    site_classification = models.CharField(max_length=100)
    site_category = models.CharField(max_length=30, choices=site_category, blank=True, null=True)

    def __str__(self):
        if self.site_category:
            return smart_text("{} ({})".format(self.site_classification.capitalize(), self.site_category))
        return smart_text("{}".format(self.site_classification))

    def natural_key(self):
        return (self.site_classification, self.site_category)

    class Meta:
        ordering = ('site_classification',)
        unique_together = (('site_classification', 'site_category'),)


@python_2_unicode_compatible
class SamplingConfidence(models.Model):
    sampling_conf = models.CharField(max_length=30, db_index=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return smart_text(self.sampling_conf)

    class Meta:
        managed = False
        db_table = 'sampling_confidence'


@python_2_unicode_compatible
class SampleMethodology(models.Model):
    sampling_meth = models.CharField(unique=True, db_index=True, max_length=20)

    def __str__(self):
        return smart_text(self.sampling_meth)

    class Meta:
        managed = False
        db_table = 'sample_methodology'


@python_2_unicode_compatible
class SiteDescriptions(models.Model):
    site_description = models.CharField(max_length=60, choices=site_description, db_index=True)

    def __str__(self):
        return smart_text(self.site_description)

    class Meta:
        managed = False
        db_table = 'ymac_db_sitedescriptions'
        verbose_name_plural = "Site Descriptions"


@python_2_unicode_compatible
class SurveyDocument(models.Model):
    document_type = models.ForeignKey(DocumentType)
    filepath = models.TextField(blank=True, null=True, db_index=True, )  # validators=[valid_directory]
    filename = models.CharField(max_length=200, blank=True, null=True, db_index=True, validators=[valid_extension])
    file_status = models.ForeignKey('SurveyStatus', blank=True, null=True,
                                    help_text="If Spatial What type of data is it?")
    title = models.TextField(blank=True)

    def check_file_exists(self):
        """
        Check file is on one of our drives and not local.
        Also check if file actually exists
        :return:
        """
        fp = path.join(self.filepath, self.filename)
        drive = path.splitdrive(fp)[0] if not path.splitdrive(fp) else path.splitdrive(fp)[0]
        if drive not in VALID_DRIVES:
            return smart_text("Can't find Drive")
        if not path.isfile(fp):
            return smart_text("File does not exist")

    def __str__(self):
        return smart_text("%s-%s : %s" % (self.document_type.document_type, self.document_type.sub_type, self.filename))

    class Meta:
        unique_together = (('document_type', 'filepath', 'filename'),)

@python_2_unicode_compatible
class SurveyProponentCode(models.Model):
    """
    For when a survey has a proponent code.
    This used to be the old rio_codes table but expanded.
    This is a one to many table.
    """
    proponent = models.ForeignKey('Proponent', blank=True, db_index=True)
    proponent_code = models.CharField(max_length=20, blank=True, null=True, db_index=True)

    def __str__(self):
        if self.proponent_code:
            return smart_text("{} Code {}".format(self.proponent, self.proponent_code))
        else:
            return smart_text("No code")

    class Meta:
        managed = True


@python_2_unicode_compatible
class SurveyCleaning(models.Model):
    """
    These are cleaning comments and data paths that can be attached
    to a heritage survey.
    """
    data_path = models.TextField(blank=False, null=False, db_index=True)
    path_type = models.CharField(max_length=15, blank=True, null=False, db_index=True, choices=path_type)

    class Meta:
        managed = True
        ordering = ('surveys__survey_id', 'data_path')

    def __str__(self):
        if self.data_path:
            return smart_text("Cleaning Item {}".format(path.split(self.data_path)[1]))
        return 'No data_path'


@python_2_unicode_compatible
class SurveyTripCleaning(models.Model):
    """
    These are cleaning comments and data paths that can be attached
    to a heritage survey trip.
    """
    survey_trip = models.ForeignKey('HeritageSurvey')
    cleaning_comment = models.TextField(blank=False, null=False)
    data_path = models.TextField(blank=False, null=False, db_index=True)
    path_type = models.CharField(max_length=15, blank=True, null=False, choices=path_type)

    class Meta:
        managed = True

    def __str__(self):
        name = self.data_path if self.data_path else self.cleaning_comment
        return smart_text("Trip Cleaning Item {}".format(name))


@python_2_unicode_compatible
class SurveyMethodology(models.Model):
    survey_meth = models.CharField(max_length=40, db_index=True)

    def __str__(self):
        return smart_text(self.survey_meth)

    class Meta:
        managed = False


@python_2_unicode_compatible
class SurveyStatus(models.Model):
    survey_status_id = models.AutoField(primary_key=True)
    status = models.CharField(unique=True, max_length=15, blank=True, null=True, db_index=True)

    def __str__(self):
        return smart_text(self.status)

    class Meta:
        managed = True
        ordering = ('status',)
        db_table = 'survey_status'


@python_2_unicode_compatible
class SurveyType(models.Model):
    type_id = models.CharField(unique=True, max_length=4)
    description = models.CharField(unique=True, max_length=25, blank=True, null=True, db_index=True)

    def __str__(self):
        return smart_text(self.description)

    class Meta:
        managed = False
        db_table = 'survey_types'


@python_2_unicode_compatible
class TenementsAll(models.Model):
    fmt_tenid = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    survstatus = models.CharField(max_length=200, blank=True, null=True)
    tenstatus = models.CharField(max_length=200, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    grantdate = models.DateField(blank=True, null=True)
    granttime = models.TimeField(blank=True, null=True)
    legal_area = models.FloatField(blank=True, null=True)
    unit_of_me = models.CharField(max_length=200, blank=True, null=True)
    special_in = models.CharField(max_length=200, blank=True, null=True)
    combined_r = models.CharField(max_length=200, blank=True, null=True)
    all_holder = models.CharField(max_length=300, blank=True, null=True)
    claim_groups = models.CharField(max_length=200, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        return smart_text(self.fmt_tenid)

    class Meta:
        managed = True
        db_table = 'tenements_all'


@python_2_unicode_compatible
class TenementsYmac(models.Model):
    fmt_tenid = models.CharField(max_length=20, blank=True, null=True)
    claim_groups = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    survstatus = models.CharField(max_length=200, blank=True, null=True)
    tenstatus = models.CharField(max_length=200, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    grantdate = models.DateField(blank=True, null=True)
    granttime = models.TimeField(blank=True, null=True)
    legal_area = models.FloatField(blank=True, null=True)
    unit_of_me = models.CharField(max_length=200, blank=True, null=True)
    special_in = models.CharField(max_length=200, blank=True, null=True)
    extract_da = models.CharField(max_length=200, blank=True, null=True)
    combined_r = models.CharField(max_length=200, blank=True, null=True)
    all_holder = models.CharField(max_length=300, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        return smart_text(self.fmt_tenid)

    class Meta:
        managed = False
        db_table = 'tenements_ymac'


@python_2_unicode_compatible
class Tenement(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True)
    survstatus = models.CharField(max_length=15, blank=True, null=True)
    tenstatus = models.CharField(max_length=10, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    starttime = models.CharField(max_length=8, blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    endtime = models.CharField(max_length=8, blank=True, null=True)
    grantdate = models.DateField(blank=True, null=True)
    granttime = models.CharField(max_length=8, blank=True, null=True)
    fmt_tenid = models.CharField(primary_key=True, max_length=16, db_index=True)
    legal_area = models.DecimalField(max_digits=31, decimal_places=15, blank=True, null=True)
    special_in = models.CharField(max_length=1, blank=True, null=True)
    extract_da = models.DateField(blank=True, null=True)
    combined_r = models.CharField(max_length=10, blank=True, null=True)
    all_holder = models.CharField(max_length=254, blank=True, null=True)
    tribid = models.CharField(max_length=200, blank=True, null=True)
    claim_groups = models.CharField(max_length=200, blank=True, null=True)
    ymac_region = models.NullBooleanField()
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        return smart_text(self.fmt_tenid)

    class Meta:
        managed = False
        db_table = 'tenement'


class Tenure(models.Model):
    alt_pityp = models.CharField(max_length=1, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    centlat = models.FloatField(blank=True, null=True)
    centlong = models.FloatField(blank=True, null=True)
    date_execution = models.DateField(blank=True, null=True)
    date_surveyed = models.TextField(blank=True, null=True)
    date_time_boundary_modified = models.DateField(blank=True, null=True)
    date_time_legal = models.DateField(blank=True, null=True)
    date_time_polygon_created = models.DateField(blank=True, null=True)
    date_time_polygon_modified = models.DateField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    dealing_year = models.IntegerField(blank=True, null=True)
    dlg_id = models.IntegerField(blank=True, null=True)
    family_name = models.CharField(max_length=255, blank=True, null=True)
    fol_rec_id = models.IntegerField(blank=True, null=True)
    given_name = models.CharField(max_length=255, blank=True, null=True)
    gprpfx = models.CharField(max_length=2, blank=True, null=True)
    gprsfx = models.CharField(max_length=4, blank=True, null=True)
    land_id_number = models.IntegerField()
    legal_area = models.FloatField(blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)
    lot_name = models.CharField(max_length=60, blank=True, null=True)
    lot_number = models.IntegerField(blank=True, null=True)
    lot_type = models.CharField(max_length=6, blank=True, null=True)
    organisation_code = models.CharField(max_length=4, blank=True, null=True)
    piparcel = models.CharField(max_length=17, blank=True, null=True)
    pityp = models.CharField(max_length=1, blank=True, null=True)
    polygon_number = models.IntegerField()
    postcode = models.CharField(max_length=4, blank=True, null=True)
    proprietor = models.CharField(max_length=255, blank=True, null=True)
    rd_name = models.CharField(max_length=40, blank=True, null=True)
    rd_type = models.CharField(max_length=4, blank=True, null=True)
    region = models.CharField(max_length=5, blank=True, null=True)
    sale_date = models.DateField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)
    usage_code = models.IntegerField(blank=True, null=True)
    zone = models.IntegerField(blank=True, null=True)
    gml_parent_id = models.TextField(blank=True, null=True)
    gml_parent_property = models.TextField(blank=True, null=True)
    gml_id = models.TextField(blank=True, null=True)
    view_scale = models.CharField(max_length=1, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)
    dealing_type = models.CharField(max_length=2, blank=True, null=True)
    register = models.CharField(max_length=13, blank=True, null=True)
    address_no_type = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenure'
        unique_together = (('land_id_number', 'polygon_number'), ('land_id_number', 'polygon_number'),)


@python_2_unicode_compatible
class YmacClaim(models.Model):
    tribid = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=102, blank=True, null=True, db_index=True)
    fcno = models.CharField(max_length=20, blank=True, null=True)
    datelodged = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    datestatus = models.DateField(blank=True, null=True)
    rtstatus = models.CharField(max_length=40, blank=True, null=True)
    datertdec = models.DateField(blank=True, null=True)
    datereg = models.DateField(blank=True, null=True)
    datentri = models.DateField(blank=True, null=True)
    datenotncl = models.DateField(blank=True, null=True)
    datefcord = models.DateField(blank=True, null=True)
    combined = models.CharField(max_length=1, blank=True, null=True)
    parentno = models.CharField(max_length=12, blank=True, null=True)
    rep = models.CharField(max_length=102, blank=True, null=True)
    casemgr = models.CharField(max_length=25, blank=True, null=True)
    member = models.CharField(max_length=254, blank=True, null=True)
    appltype = models.CharField(max_length=50, blank=True, null=True)
    areasqkm = models.FloatField(blank=True, null=True)
    datasource = models.CharField(max_length=60, blank=True, null=True)
    datecurr = models.DateField(blank=True, null=True)
    seaclaim = models.CharField(max_length=1, blank=True, null=True)
    zonelwm = models.CharField(max_length=1, blank=True, null=True)
    zone3nm = models.CharField(max_length=1, blank=True, null=True)
    zone12nm = models.CharField(max_length=1, blank=True, null=True)
    zone24nm = models.CharField(max_length=1, blank=True, null=True)
    zoneeez = models.CharField(max_length=1, blank=True, null=True)
    nnttseqno = models.CharField(max_length=14)
    objectind = models.CharField(max_length=1, blank=True, null=True)
    sptialnote = models.CharField(max_length=120, blank=True, null=True)
    juris = models.CharField(max_length=10, blank=True, null=True)
    overlap = models.CharField(max_length=20, blank=True, null=True)
    tribno = models.CharField(max_length=10, blank=True, null=True)
    ymacregion = models.CharField(max_length=200, blank=True, null=True)
    claimgroup = models.CharField(max_length=200, blank=True, null=True)
    anthro = models.CharField(max_length=200, blank=True, null=True)
    lawyer = models.CharField(max_length=200, blank=True, null=True)
    hs_officer = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)
    claim_group_id = models.CharField(max_length=5, blank=True, null=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return smart_text(self.name.strip())

    class Meta:
        managed = True
        db_table = 'ymac_claims'
        ordering = ('name',)


@python_2_unicode_compatible
class YmacEmitTenements(models.Model):
    title = models.CharField(max_length=20)
    objectiondate = models.TextField(blank=True, null=True)
    datereceived = models.DateField(blank=True, null=True)
    applicants = models.CharField(max_length=200, blank=True, null=True)
    row_to_check = models.NullBooleanField(blank=True, null=True)
    claimgroup = ArrayField(models.TextField(blank=True, null=True))
    ymac_region = models.NullBooleanField(blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True)

    def __str__(self):
        return smart_text(self.title.strip())

    class Meta:
        managed = False
        db_table = 'ymac_db_emits_tenement'
        ordering = ('datereceived', 'title')


@python_2_unicode_compatible
class YmacHeritageStaging(models.Model):
    operation = models.CharField(max_length=7, blank=True, null=True)
    survey_trip_id = models.IntegerField()
    survey_id = models.CharField(max_length=60, blank=True, null=True)
    trip_number = models.SmallIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    claimgroup = models.TextField(blank=True, null=True)
    survey_type = models.CharField(max_length=25, blank=True, null=True)
    sampling_meth = models.CharField(max_length=20, blank=True, null=True)
    sampling_conf = models.CharField(max_length=60, blank=True, null=True)
    ymac_svy_name = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    survey_name = models.CharField(max_length=200, blank=True, null=True)
    date_create = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    date_mod = models.DateField(blank=True, null=True)
    mod_by = models.CharField(max_length=50, blank=True, null=True)
    propref = models.CharField(max_length=200, blank=True, null=True)
    data_supplier = models.CharField(max_length=50, blank=True, null=True)
    data_qa = models.TextField(blank=True, null=True)
    collected_by = models.CharField(max_length=60, blank=True, null=True)
    rio_area_codes = models.TextField(blank=True, null=True)
    survey_methodology = models.TextField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    modified_time = models.DateTimeField()

    def __str__(self):
        return smart_text(self.ymac_svy_name)

    class Meta:
        managed = False
        db_table = 'ymac_heritage_staging'
        unique_together = (('survey_trip_id', 'modified_time'),)


@python_2_unicode_compatible
class YmacRegion(models.Model):
    org = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    gazetted = models.DateField(blank=True, null=True)
    effective = models.DateField(blank=True, null=True)
    comments = models.CharField(max_length=120, blank=True, null=True)
    juris = models.CharField(max_length=20, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    geom = models.GeometryField(srid=4283,blank=True, null=True)

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        managed = True
        db_table = 'YMAC_region'


@python_2_unicode_compatible
class YmacStaff(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    email = models.CharField(max_length=70, blank=True, null=True)
    full_name = models.CharField(max_length=70, blank=True, null=True, db_index=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    current_staff = models.BooleanField(default=True)

    def __str__(self):
        return smart_text(self.full_name)

    class Meta:
        managed = True
        ordering = ('first_name', 'last_name')
        db_table = 'ymac_staff'
        verbose_name_plural = 'YMAC Staff'


def user_directory_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/<jid>/<filename>
    jc = self.request.job_control
    if not jc:
        jc = self.request.job_control
    return '{0}/{1}'.format(jc, filename)


@python_2_unicode_compatible
class YMACRequestFiles(models.Model):
    """
    Will clean up all these files after approval
    """
    request = models.ForeignKey('YMACSpatialRequest')
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return smart_text(self.file)


@python_2_unicode_compatible
class SiteUser(models.Model):
    """
    This needs to be renamed to generic collection person
    """
    user_name = models.CharField(max_length=70, blank=True, null=True, db_index=True)
    employee = models.NullBooleanField()
    capture_org = models.ForeignKey('CaptureOrg', blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return smart_text(self.user_name)

    class Meta:
        managed = False
        ordering = ('user_name',)
        db_table = 'ymac_db_siteuser'


@python_2_unicode_compatible
class SurveyGroup(models.Model):
    """
    The Original Claim group area a heritage survey relates to
    may now be determined. Groups with multiple areas will be aggregated
    """
    group_name = models.CharField(max_length=35, db_index=True)
    group_id = models.CharField(max_length=3)
    determined = models.BooleanField()
    status = models.CharField(max_length=15, choices=group_status, default="Represented",
                              help_text="Does YMAC Represent the Claim")
    heritage_officer = models.ForeignKey(SiteUser, blank=True, related_name='heritageuser', default=72)
    future_act_officer = models.ForeignKey(SiteUser, blank=True, related_name='futureactuser', default=71)
    geom = models.GeometryField(srid=4283, blank=True)

    def __str__(self):
        return smart_text(self.group_name)

    class Meta:
        managed = True
        ordering = ('group_name',)


@python_2_unicode_compatible
class YMACSpatialRequest(models.Model):
    """
    Still need to add in the choices for each
    """
    user = models.ForeignKey(RequestUser, db_index=True)
    request_type = models.ForeignKey('RequestType',
                                     help_text="Please try to determine what sort of request "
                                               "you have before completing this form.")
    region = models.CharField(max_length=15, choices=ymac_region, blank=True)
    claim = models.ManyToManyField(YmacClaim, blank=True)
    job_desc = models.TextField()
    job_control = models.CharField(max_length=9, blank=True, validators=[valid_job_number])
    map_size = models.CharField(max_length=20, choices=map_sizes, help_text="If you know what size map "
                                                                            "you wish then please select.",
                                blank=True, null=True)
    map_title = models.CharField(max_length=300, null=True, default='', blank=True, help_text="Please provide a map title")
    required_by = models.DateField()
    request_datetime = models.DateTimeField(blank=True, auto_now_add=True)
    completed_datetime = models.DateTimeField(blank=True)
    cc_recipients = models.ManyToManyField(RequestUser, related_name='cc_recipients', blank=True, help_text="You can select multiple recipients")
    product_type = models.CharField(max_length=25, choices=product_types, blank=True)
    other_instructions = models.TextField(blank=True)
    # Set this back to false
    cost_centre = models.CharField(max_length=30, choices=cost_centres, blank=True)
    proponent = models.ForeignKey(Proponent, blank=True, null=True, help_text="Proponent (if known)")
    priority = models.CharField(max_length=25, choices=urgency, help_text="Please estimate urgency and priority to "
                                                                          "assist spatial team to prioritise their task list")
    map_requested = models.BooleanField(default=False)
    data = models.BooleanField(default=False)
    analysis = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(YmacStaff, blank=True)
    time_spent = models.FloatField(blank=True)
    related_jobs = models.ManyToManyField("self", blank=True,
                                          help_text="Optional: If this job is related to a past or current job please "
                                                    "select it. Hint: type the name of person who requested it.")
    request_area = models.GeometryField(srid=4283, blank=True, null=True)
    sup_data_text = models.TextField(blank=True,
                                     help_text="For large amounts of data please indicate the folder where it can be "
                                               "found. Alternatively you can upload files below "
                                               "or send an email to spatialjobs@ymac.org.au."
                                     )

    class Meta:
        ordering = ('-job_control', '-required_by',)

    def __str__(self):
        return smart_text("{} : {} : {} - ({}) {} ".format(self.job_control,
                                                       self.request_datetime.strftime("%d/%m/%Y"),
                                                       self.user.name,
                                                       self.request_type.name,
                                                       self.job_desc[:265]))

    def generate_job_control(self):
        """
        Generate a job control number
        :return:
        """
        if not self.job_control:
            year = datetime.datetime.now().strftime("%Y")
            try:
                control_number = int(max([qs.job_control for qs in YMACSpatialRequest.objects.filter(
                    job_control__icontains=year)]
                                         ).split("-")[1]
                                     ) + 1
            except ValueError:
                control_number = 1
            return "J{0}-{1:0>3}".format(year, control_number)


@python_2_unicode_compatible
class YACReturn(models.Model):
    """
    Will clean up all these files after approval
    """
    survey = models.ForeignKey(HeritageSurvey)
    pa = models.BooleanField(default=False)
    report = models.BooleanField(default=False)
    spatial = models.BooleanField(default=False)

    def __str__(self):
        return smart_text("{}".format(self.survey))
