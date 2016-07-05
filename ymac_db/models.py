from __future__ import unicode_literals

from os import path

from django.contrib.gis.db import models
from django.utils.encoding import smart_text

from .validators import valid_surveyid

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

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
                 ('Approximate', 'Approximate',),
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

site_classification = [('Ethnographic', 'Ethnographic'),
                       ('Archeological', 'Archeological'),
                       ('Arch & Ethno', 'Arch & Ethno')
                       ]
site_category = [
    ('GEOGRAPHIC FEATURES', 'GEOGRAPHIC FEATURES'),
    ('RESTRICTED OR CEREMONIAL SITE', 'RESTRICTED OR CEREMONIAL SITE'),
    ('CAMPS/ LIVING AREAS', 'CAMPS/ LIVING AREAS')
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
    ('Survey Report', 'Survey Report')
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


class DocumentType(models.Model):
    document_type = models.CharField(max_length=15, choices=document_type)
    sub_type = models.CharField(max_length=30, choices=document_subtype, blank=True, null=True)

    def __unicode__(self):
        doc_string = "%s : %s" % (self.document_type, self.sub_type) if self.sub_type else "%s" % (self.document_type)
        return smart_text(doc_string)


class SurveyDocument(models.Model):
    document_type = models.ForeignKey(DocumentType)
    filepath = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=200, blank=True, null=True)

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

    def __unicode__(self):
        return smart_text("%s : %s" % (self.document_type, self.filename))


class SampleMethodology(models.Model):
    sampling_meth = models.CharField(unique=True, max_length=20)

    def __unicode__(self):
        return smart_text(self.sampling_meth)

    class Meta:
        managed = False
        db_table = 'sample_methodology'


class SamplingConfidence(models.Model):
    sampling_conf = models.CharField(max_length=30)
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return smart_text(self.sampling_conf)

    class Meta:
        managed = False
        db_table = 'sampling_confidence'


class SurveyProponentCode(models.Model):
    """
    For when a survey has a proponent code.
    This used to be the old rio_codes table but expanded.
    This is a one to many table.
    """
    heritage_svy_id = models.IntegerField(null=False)
    proponent_code = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        if self.proponent_code:
            return smart_text("Proponent Code {}".format(self.proponent_code))
        else:
            return smart_text("No code")

    class Meta:
        managed = False


class HeritageCompanies(models.Model):
    """
    Companies who Heritage Surveys have been performed for.
    """
    old_code = models.IntegerField(unique=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False

    def __unicode__(self):
        return smart_text("Company {}".format(self.company_name))


class SurveyCleaning(models.Model):
    """
    These are cleaning comments and data paths that can be attached
    to a heritage survey.
    """
    cleaning_comment = models.TextField(blank=False, null=False)
    data_path = models.TextField(blank=False, null=False)
    path_type = models.CharField(max_length=15, blank=True, null=False, choices=path_type)

    class Meta:
        managed = True
        ordering = ('heritagesurvey__survey_trip__survey_id', 'data_path')

    def __unicode__(self):
        name = self.data_path if self.data_path else self.cleaning_comment
        return smart_text("Cleaning Item {}".format(name))


class SurveyTripCleaning(models.Model):
    """
    These are cleaning comments and data paths that can be attached
    to a heritage survey trip.
    """
    survey_trip = models.ForeignKey('HeritageSurveyTrip')
    cleaning_comment = models.TextField(blank=False, null=False)
    data_path = models.TextField(blank=False, null=False)
    path_type = models.CharField(max_length=15, blank=True, null=False, choices=path_type)

    class Meta:
        managed = True

    def __unicode__(self):
        name = self.data_path if self.data_path else self.cleaning_comment
        return smart_text("Trip Cleaning Item {}".format(name))


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

    def __unicode__(self):
        name = self.data_path if self.data_path else self.cleaning_comment
        return smart_text("Cleaning Item {}".format(name))


class SiteDescriptions(models.Model):
    site_description = models.CharField(max_length=60, choices=site_description)

    def __unicode__(self):
        return smart_text(self.site_description)

    class Meta:
        managed = False
        db_table = 'ymac_db_sitedescriptions'
        verbose_name_plural = "Site Descriptions"


class DaaSite(models.Model):
    objectid = models.AutoField(max_length=200, primary_key=True)
    place_id = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
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
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.name)

    class Meta:
        ordering = ('name',)
        managed = False
        db_table = 'daa_sites'


class DataSuppliers(models.Model):
    supplier = models.CharField(primary_key=True, max_length=50)

    def __unicode__(self):
        return smart_text(self.supplier)

    class Meta:
        managed = False
        db_table = 'data_suppliers'


class ExternalClientSite(models.Model):
    external_id = models.AutoField(primary_key=True)
    external_site_id = models.TextField(blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    geom = models.PolygonField(srid=4283)

    def __unicode__(self):
        return smart_text(self.site_name)

    class Meta:
        managed = False
        db_table = 'external_client_sites'


# Status like
# Site Category
# Proponent???
# Site Centroid ???
# WHAT TO DO ABOUT Tracks
# Datum to read in
# Avoidance Buffer
class HeritageSite(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE, blank=True, null=True, help_text="The Spatial Site Data")
    site_description = models.ForeignKey('SiteDescriptions', blank=True, null=True)
    boundary_description = models.CharField(max_length=30, choices=boundary_description, blank=True, null=True)
    disturbance_level = models.CharField(max_length=30, choices=disturbance_level, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True, choices=her_site_status)
    site_comments = models.TextField(blank=True, null=True)
    heritage_surveys = models.ManyToManyField('HeritageSurvey',
                                              related_name='her_sites',
                                              )
    documents = models.ManyToManyField('SiteDocument',
                                       related_name='heritagesites',
                                       )

    def __unicode__(self):
        return smart_text(self.site)

    class Meta:
        managed = True


class HeritageSurvey(models.Model):
    survey_trip = models.ForeignKey('HeritageSurveyTrip', help_text="Trip and related Trip information")
    data_status = models.ForeignKey('SurveyStatus', blank=True, null=True, help_text="For current spatial data is"
                                                                                     " it proposed or after survey completion (Actual)")
    data_source = models.ManyToManyField('SurveyCleaning', blank=True, null=True,
                                         help_text="Any comments or data relating to the data")
    survey_type = models.ForeignKey('SurveyType', on_delete=models.CASCADE, db_column='survey_type', blank=True,
                                    null=True)
    survey_methodologies = models.ManyToManyField('SurveyMethodology', blank=True, null=True, )
    survey_group = models.ForeignKey('SurveyGroup', blank=True, null=True)
    proponent = models.ForeignKey('Proponent', on_delete=models.CASCADE, blank=True, null=True)
    proponent_codes = models.ManyToManyField('SurveyProponentCode', null=True, blank=True,
                                             help_text="Any proponent codes relating to the survey"
                                                       " i.e RIO Area Codes AR-00-00000")
    sampling_meth = models.ForeignKey('SampleMethodology', db_column='sampling_meth',
                                      on_delete=models.CASCADE, default=6, blank=True, null=True)
    sampling_conf = models.ForeignKey('SamplingConfidence', on_delete=models.CASCADE, default=5, blank=True, null=True)
    project_name = models.TextField(blank=True, null=True, help_text="Internal or Survey Project Name")
    project_status = models.CharField(max_length=25, default=3, choices=project_status, blank=True, null=True)
    survey_region = models.CharField(max_length=15, choices=ymac_region, blank=True, null=True)
    survey_description = models.TextField(blank=True, null=True,
                                          help_text="Description of the proposed or actual survey")
    survey_note = models.TextField(blank=True, null=True, help_text="Additional Survey notes")
    created_by = models.ForeignKey('SiteUser', related_name='created_user', blank=True, null=True)
    date_create = models.DateField(blank=True, null=True)
    mod_by = models.ForeignKey('SiteUser', related_name='mod_user', blank=True, null=True)
    date_mod = models.DateField(blank=True, null=True)
    data_qa = models.BooleanField(default=False, help_text="Has Actual data been checked by Spatial Team")
    consultants = models.ManyToManyField('Consultant', blank=True, null=True, help_text="Consultants for survey")
    documents = models.ManyToManyField(SurveyDocument, blank=True, help_text="Related documents")
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __unicode__(self):
        if self.survey_trip.survey_id:
            return smart_text("{} - {}".format(self.survey_trip.survey_id, self.project_name))
        return smart_text(self.project_name)

    class Meta:
        managed = True
        ordering = ('survey_trip__survey_id', 'date_create',)


class SurveyMethodology(models.Model):
    survey_meth = models.CharField(max_length=40)

    def __unicode__(self):
        return smart_text(self.survey_meth)

    class Meta:
        managed = False


class NnttDetermination(models.Model):
    tribid = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
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
    ymacregion = models.CharField(max_length=200, blank=True, null=True)
    hs_officer = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.name)

    class Meta:
        managed = False
        db_table = 'nntt_determinations'


class Proponent(models.Model):
    id = models.AutoField(primary_key=True)
    prop_id = models.CharField(max_length=10)
    name = models.TextField()
    contact = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.name)

    class Meta:
        managed = False
        ordering = ('name',)


class ResearchSite(models.Model):
    research_site_id = models.AutoField(primary_key=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, blank=True, null=True,
                             help_text="The Spatial Site Data (optional)")
    site_classification = models.CharField(max_length=30, choices=site_classification, blank=True, null=True)
    site_category = models.CharField(max_length=30, choices=site_category, blank=True, null=True)
    site_location = models.CharField(max_length=30, choices=site_location, blank=True, null=True)
    site_comments = models.TextField(blank=True, null=True)
    ethno_detail = models.TextField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    site_label = models.TextField(blank=True, null=True)
    alt_site_name = models.TextField(blank=True, null=True)
    site_number = models.IntegerField(blank=True, null=True)
    family_affiliation = models.TextField(blank=True, null=True)
    mapsheet = models.TextField(blank=True, null=True)
    documents = models.ManyToManyField('SiteDocument',
                                       db_column='site_id',
                                       related_name='researchdocuments')

    def __unicode__(self):
        return smart_text("Research Site {} {}".format(self.site_name, self.site_id))

    class Meta:
        managed = False
        db_table = 'research_sites'


class RestrictionStatus(models.Model):
    rid = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=12, choices=gender, blank=True, null=True)
    claim = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
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


class SiteDocument(models.Model):
    doc_id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=15, choices=document_type)  # This field type is a guess.
    filepath = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)

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

    def __unicode__(self):
        return smart_text(self.filename)

    class Meta:
        managed = False
        db_table = 'site_documents'


class Site(models.Model):
    recorded_by = models.ForeignKey('SiteUser', on_delete=models.CASCADE, db_column='recorded_by',
                                    related_name='site_recorded_by', blank=True, null=True)
    date_recorded = models.DateField(blank=True, null=True)
    group_name = models.TextField(blank=True, null=True, help_text="Is this site part of a group of sites or complex?")
    site_identifier = models.CharField(max_length=200, blank=True, null=True,
                                       help_text="Site name to help you identify it")
    restricted_status = models.ForeignKey(RestrictionStatus, on_delete=models.CASCADE, db_column='restricted_status',
                                          blank=True, null=True)
    label_x_ll = models.FloatField(blank=True, null=True)
    label_y_ll = models.FloatField(blank=True, null=True)
    date_created = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('SiteUser', on_delete=models.CASCADE, db_column='created_by',
                                   related_name='site_created_by', blank=True)
    active = models.NullBooleanField()
    capture_coord_sys = models.TextField(blank=True, null=True)
    docs = models.ManyToManyField('SiteDocument', blank=True)
    surveys = models.ManyToManyField('HeritageSurvey', blank=True)
    daa_sites = models.ManyToManyField('DaaSite', blank=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __unicode__(self):
        if self.site_identifier:
            return smart_text(self.site_identifier)
        return smart_text("Site {}".format(self.site_id))

    class Meta:
        managed = True


class SurveyStatus(models.Model):
    survey_status_id = models.AutoField(primary_key=True)
    status = models.CharField(unique=True, max_length=8, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.status)

    class Meta:
        managed = False
        db_table = 'survey_status'


class RelatedSurveyCode(models.Model):
    rel_survey_id = models.CharField(max_length=10)

    class Meta:
        managed = False

    def __unicode__(self):
        return smart_text(self.rel_survey_id)


class HeritageSurveyTrip(models.Model):
    survey_trip_id = models.AutoField(primary_key=True)
    survey_id = models.CharField(max_length=10, validators=[valid_surveyid])
    original_ymac_id = models.CharField(max_length=50, blank=True, null=True)
    related_surveys = models.ManyToManyField('RelatedSurveyCode', blank=True)
    trip_number = models.SmallIntegerField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)

    def __unicode__(self):
        if self.trip_number:
            retstr = "{}_(Trip {})".format(self.survey_id, self.trip_number)
        else:
            retstr = "{}".format(self.survey_id)
        return smart_text(retstr)

    class Meta:
        managed = False
        ordering = ('survey_id',)


class SurveyType(models.Model):
    type_id = models.CharField(unique=True, max_length=4)
    description = models.CharField(unique=True, max_length=25, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.description)

    class Meta:
        managed = False
        db_table = 'survey_types'


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
    fmt_tenid = models.CharField(primary_key=True, max_length=16)
    legal_area = models.DecimalField(max_digits=31, decimal_places=15, blank=True, null=True)
    special_in = models.CharField(max_length=1, blank=True, null=True)
    extract_da = models.DateField(blank=True, null=True)
    combined_r = models.CharField(max_length=10, blank=True, null=True)
    all_holder = models.CharField(max_length=254, blank=True, null=True)
    tribid = models.CharField(max_length=200, blank=True, null=True)
    claim_groups = models.CharField(max_length=200, blank=True, null=True)
    ymac_region = models.NullBooleanField()
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.fmt_tenid)

    class Meta:
        managed = False
        db_table = 'tenement'


class YmacClaim(models.Model):
    tribid = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=102, blank=True, null=True)
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
    nnttseqno = models.CharField(primary_key=True, max_length=14)
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
    geom = models.GeometryField(blank=True, null=True)
    claim_group_id = models.CharField(max_length=5, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.name)

    class Meta:
        managed = False
        db_table = 'ymac_claims'
        ordering = ('name',)


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
    ymac_svy_name = models.CharField(max_length=200, blank=True, null=True)
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

    def __unicode__(self):
        return smart_text(self.ymac_svy_name)

    class Meta:
        managed = False
        db_table = 'ymac_heritage_staging'
        unique_together = (('survey_trip_id', 'modified_time'),)


class YmacRegion(models.Model):
    org = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    gazetted = models.DateField(blank=True, null=True)
    effective = models.DateField(blank=True, null=True)
    comments = models.CharField(max_length=120, blank=True, null=True)
    juris = models.CharField(max_length=20, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.name)

    class Meta:
        managed = True
        db_table = 'YMAC_region'


class YmacStaff(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    email = models.CharField(max_length=70, blank=True, null=True)
    full_name = models.CharField(max_length=70, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.full_name)

    class Meta:
        managed = False
        db_table = 'ymac_staff'


class Consultant(models.Model):
    """
    Survey Consultants
    """
    name = models.CharField(max_length=70, blank=True, null=True)
    employee = models.NullBooleanField()
    company = models.ForeignKey('CaptureOrg', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        if self.name:
            return smart_text(self.name)
        else:
            return smart_text("Employee of {}".format(self.company))

    class Meta:
        managed = False
        ordering = ('name',)


class CaptureOrg(models.Model):
    organisation_name = models.TextField()
    organisation_contact = models.CharField(max_length=100, blank=True, null=True, help_text="Main Contact Name")
    organisation_email = models.EmailField(blank=True, null=True, help_text="Main Contact Email")
    organisation_phone = models.CharField(max_length=16, blank=True, null=True)
    organisation_address = models.TextField(blank=True, null=True)
    organisation_suburb = models.TextField(blank=True, null=True)
    organisation_state = models.CharField(max_length=3, blank=True, null=True, choices=states)
    organisation_postcode = models.IntegerField(blank=True, null=True)
    organisation_website = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.organisation_name)

    class Meta:
        managed = False
        db_table = 'ymac_db_captureorg'


class SiteUser(models.Model):
    """
    This needs to be renamed to generic collection person
    """
    user_name = models.CharField(max_length=70, blank=True, null=True)
    employee = models.NullBooleanField()
    capture_org = models.ForeignKey('CaptureOrg', blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return smart_text(self.user_name)

    class Meta:
        managed = False
        ordering = ('user_name',)
        db_table = 'ymac_db_siteuser'


class SurveyGroup(models.Model):
    """
    The Original Claim group area a heritage survey relates to
    may now be determined. Groups with multiple areas will be aggregated
    """
    group_name = models.CharField(max_length=35)
    group_id = models.CharField(max_length=3)
    determined = models.BooleanField()
    status = models.CharField(max_length=15, choices=group_status, default="Represented",
                              help_text="Does YMAC Represent the Claim")
    heritage_officer = models.ForeignKey(SiteUser, blank=True, related_name='heritageuser', default=72)
    future_act_officer = models.ForeignKey(SiteUser, blank=True, related_name='futureactuser', default=71)
    geom = models.GeometryField(srid=4283, blank=True)

    def __unicode__(self):
        return smart_text(self.group_name)

    class Meta:
        managed = True
        ordering = ('group_name',)


class Department(models.Model):
    name = models.CharField(max_length=25, choices=departments)
    head = models.ForeignKey(YmacStaff)

    def __unicode__(self):
        return smart_text(self.name)


class RequestUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey('Department')
    office = models.CharField(max_length=20, choices=offices, default="Perth")
    region = models.CharField(max_length=15, choices=ymac_region, default="Yamatji")

    def __unicode__(self):
        return smart_text(self.name)


class RequestType(models.Model):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return smart_text(self.name)


class YMACSpatialRequest(models.Model):
    """
    Still need to add in the choices for each
    """
    user = models.ForeignKey(RequestUser)
    request_type = models.ForeignKey('RequestType',
                                     help_text="Please try to determine what sort of request "
                                               "you have before completing this form.")
    region = models.CharField(max_length=15, choices=ymac_region, default="Yamatji")
    claim = models.ManyToManyField(YmacClaim, blank=True)
    job_desc = models.TextField()
    map_size = models.CharField(max_length=20, choices=map_sizes, help_text="If you know what size map "
                                                                            "you wish then please select.",
                                blank=True, null=True)
    sup_data = models.TextField(blank=True, help_text="If you have any data with this then please "
                                                      "provide instructions as to where it can be located. "
                                                      "Alternatively send a separate email to "
                                                      "spatial@ymac.org.au with directions or as attachments.")
    required_by = models.DateField()
    cc_recipients = models.ManyToManyField(RequestUser, related_name='cc_recipients', blank=True)
    product_type = models.CharField(max_length=20, choices=product_types)
    other_instructions = models.TextField(blank=True)
    cost_centre = models.CharField(max_length=20, choices=cost_centres)
    proponent = models.ForeignKey(Proponent, blank=True, null=True, help_text="Proponent (if known)")
    priority = models.CharField(max_length=25, choices=urgency, help_text="Please estimate urgency and priority to "
                                                                          "assist spatial team to prioritise their task list")
