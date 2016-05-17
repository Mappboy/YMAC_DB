from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils.encoding import smart_text

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

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
                 ('Map', 'Map'),
                 ('Other', 'Other')
                 ]


class SiteDescriptions(models.Model):
    site_description = models.CharField(max_length=60, choices=site_description)

    def __str__(self):
        return smart_text(self.site_description)


class AssociationDocsTable(models.Model):
    ymac_site = models.ForeignKey('Site', on_delete=models.CASCADE)
    site_doc = models.ForeignKey('SiteDocument', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'association_docs_table'
        unique_together = (('ymac_site', 'site_doc'),)


class AssociationExtSitesTable(models.Model):
    ymac_site = models.ForeignKey('Site', on_delete=models.CASCADE)
    external = models.ForeignKey('ExternalClientSite', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'association_ext_sites_table'
        unique_together = (('ymac_site', 'external'),)


class AssociationSitesSurveyTable(models.Model):
    ymac_site = models.ForeignKey('Site', on_delete=models.CASCADE)
    ymac_survey = models.ForeignKey('HeritageSurvey', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'association_sites_survey_table'
        unique_together = (('ymac_site', 'ymac_survey'),)


class AssociationSitesTable(models.Model):
    ymac_site = models.ForeignKey('Site', on_delete=models.CASCADE)
    daa_site = models.ForeignKey('DaaSite', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'association_sites_table'
        unique_together = (('ymac_site', 'daa_site'),)


class DaaSite(models.Model):
    id = models.FloatField(primary_key=True)
    siteid = models.CharField(max_length=30, blank=True, null=True)
    siteuniqid = models.FloatField(blank=True, null=True)
    sitetoid = models.CharField(max_length=50, blank=True, null=True)
    recordorg = models.CharField(max_length=50, blank=True, null=True)
    svysqnceid = models.FloatField(blank=True, null=True)
    sitename = models.CharField(max_length=60, blank=True, null=True)
    atlsitenam = models.CharField(max_length=60, blank=True, null=True)
    steident = models.CharField(max_length=20, blank=True, null=True)
    sitecatid = models.CharField(max_length=20, blank=True, null=True)
    recordby = models.CharField(max_length=40, blank=True, null=True)
    daterecord = models.DateTimeField(blank=True, null=True)
    complexnme = models.CharField(max_length=50, blank=True, null=True)
    accssstat = models.CharField(max_length=20, blank=True, null=True)
    siteclass = models.CharField(max_length=25, blank=True, null=True)
    bndrytype = models.CharField(max_length=25, blank=True, null=True)
    captaccy = models.CharField(max_length=20, blank=True, null=True)
    dstblevel = models.CharField(max_length=25, blank=True, null=True)
    sitedocs = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=254, blank=True, null=True)
    fldnotref = models.CharField(max_length=50, blank=True, null=True)
    lbl_x_ll = models.FloatField(blank=True, null=True)
    lbl_y_ll = models.FloatField(blank=True, null=True)
    captdvc = models.CharField(max_length=75, blank=True, null=True)
    capcordsys = models.CharField(max_length=25, blank=True, null=True)
    datecreate = models.DateTimeField(blank=True, null=True)
    createby = models.CharField(max_length=50, blank=True, null=True)
    crrptid = models.CharField(max_length=12, blank=True, null=True)
    section_5 = models.CharField(max_length=10, blank=True, null=True)
    spatialnte = models.CharField(max_length=70, blank=True, null=True)
    bufdist_mr = models.FloatField(blank=True, null=True)
    daasite_no = models.CharField(max_length=15, blank=True, null=True)
    datemod = models.DateTimeField(blank=True, null=True)
    modby = models.CharField(max_length=50, blank=True, null=True)
    restsentve = models.CharField(max_length=10, blank=True, null=True)
    locnrest = models.CharField(max_length=15, blank=True, null=True)
    filerest = models.CharField(max_length=15, blank=True, null=True)
    negbndy = models.CharField(max_length=25, blank=True, null=True)
    rschmthlgy = models.CharField(max_length=30, blank=True, null=True)
    agreareaid = models.CharField(max_length=10, blank=True, null=True)
    agreetype = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(geography=True, blank=True, null=True)

    def __str__(self):
        return smart_text(self.sitename)

    class Meta:
        managed = False
        db_table = 'daa_sites'


class DataSuppliers(models.Model):
    supplier = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return smart_text(self.supplier)

    class Meta:
        managed = False
        db_table = 'data_suppliers'


class ExternalClientSite(models.Model):
    external_id = models.AutoField(primary_key=True)
    external_site_id = models.TextField(blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    geom = models.PolygonField(srid=4283)

    def __str__(self):
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
    heritage_site_id = models.AutoField(primary_key=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, null=True)
    site_description = models.ForeignKey(SiteDescriptions)
    boundary_description = models.CharField(max_length=30, choices=boundary_description)
    disturbance_level = models.CharField(max_length=30, choices=disturbance_level)
    status = models.CharField(max_length=15, blank=True, null=True, choices=her_site_status)
    site_comments = models.TextField(blank=True, null=True)
    heritage_surveys = models.ManyToManyField('HeritageSurvey',
                                              related_name='heritagesurveys',
                                              db_column='site_id')
    documents = models.ManyToManyField('SiteDocument',
                                       db_column='site_id',
                                       related_name='heritagedocuments')

    def __str__(self):
        return smart_text(self.site)

    class Meta:
        managed = True
        db_table = 'heritage_sites'


class HeritageSurvey(models.Model):
    survey_trip = models.OneToOneField('SurveyTrip', primary_key=True, on_delete=models.CASCADE)
    status = models.ForeignKey('SurveyStatus', on_delete=models.CASCADE, db_column='status', blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    proponent_id = models.ForeignKey('Proponents', on_delete=models.CASCADE, db_column='proponent_id', blank=True,
                                     null=True)
    claim_group_id = models.CharField(max_length=5, blank=True, null=True)
    survey_type = models.ForeignKey('SurveyType', on_delete=models.CASCADE, db_column='survey_type', blank=True,
                                    null=True)
    sampling_meth = models.ForeignKey('SampleMethodology', on_delete=models.CASCADE, db_column='sampling_meth',
                                      default='UNKNOWN', blank=True, null=True)
    ymac_svy_name = models.CharField(max_length=200, blank=True, null=True)
    survey_name = models.CharField(max_length=200, blank=True, null=True)
    date_create = models.DateField(blank=True, null=True)
    sampling_conf = models.ForeignKey('SamplingConfidence', on_delete=models.CASCADE, db_column='sampling_conf',
                                      default='Unknown', blank=True, null=True)
    created_by = models.ForeignKey('SiteUser', related_name='created_user', blank=True, null=True)
    date_mod = models.DateField(blank=True, null=True)
    mod_by = models.ForeignKey('SiteUser', related_name='mod_user', blank=True, null=True)
    propref = models.CharField(max_length=200, blank=True, null=True)
    geom = models.GeometryField(srid=28350, blank=True, null=True)
    data_supplier = models.OneToOneField(DataSuppliers, on_delete=models.CASCADE, db_column='data_supplier', blank=True,
                                         null=True)
    data_qa = models.BooleanField()
    collected_by = models.CharField(max_length=60, blank=True, null=True)

    heritage_sites = models.ManyToManyField('Site', through=AssociationSitesSurveyTable)

    def __str__(self):
        return smart_text(self.ymac_svy_name)

    class Meta:
        managed = True
        db_table = 'heritage_surveys'


class HsRioCode(models.Model):
    survey_trip = models.ForeignKey(HeritageSurvey, on_delete=models.CASCADE)
    field_rac_table = models.CharField(db_column='_rac_table', max_length=50, blank=True, null=True)

    def __str__(self):
        return smart_text(self.field_rac_table)

    class Meta:
        managed = False
        db_table = 'hs_rio_codes'


class HsSvmythlgy(models.Model):
    survey_trip = models.ForeignKey(HeritageSurvey, on_delete=models.CASCADE)
    svy_meth = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return smart_text(self.svy_meth)

    class Meta:
        managed = False
        db_table = 'hs_svmythlgy'


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

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        managed = False
        db_table = 'nntt_determinations'


class Proponents(models.Model):
    prop_id = models.CharField(primary_key=True, max_length=10)
    name = models.TextField()
    contact = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        managed = False
        db_table = 'proponents'


class ResearchSite(models.Model):
    research_site_id = models.AutoField(primary_key=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, blank=True, null=True)
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

    def __str__(self):
        return smart_text("Research Site {} {}".format(self.site_name, self.site_id))

    class Meta:
        managed = True
        db_table = 'research_sites'


class RestrictionStatus(models.Model):
    rid = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=12, choices=gender, blank=True, null=True)
    claim = models.NullBooleanField(blank=True, null=True)

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


class SampleMethodology(models.Model):
    sampling_meth = models.CharField(primary_key=True, unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'sample_methodology'

    def __str__(self):
        return smart_text(self.sampling_meth)

class SamplingConfidence(models.Model):
    sampling_conf = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'sampling_confidence'

    def __str__(self):
        return smart_text(self.sampling_conf)

class SiteDocument(models.Model):
    doc_id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=15, choices=document_type)  # This field type is a guess.
    filepath = models.TextField(max_length=255, blank=True, null=True)
    filename = models.TextField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.filename)

    class Meta:
        managed = True
        db_table = 'site_documents'


class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    recorded_by = models.ForeignKey('SiteUser', on_delete=models.CASCADE, db_column='recorded_by',
                                    related_name='site_recorded_by', blank=True, null=True)
    date_recorded = models.DateField(blank=True, null=True)
    group_name = models.TextField(blank=True, null=True)
    restricted_status = models.ForeignKey(RestrictionStatus, on_delete=models.CASCADE, db_column='restricted_status',
                                          blank=True, null=True)
    label_x_ll = models.FloatField(blank=True, null=True)
    label_y_ll = models.FloatField(blank=True, null=True)
    date_created = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('SiteUser', on_delete=models.CASCADE, db_column='created_by',
                                   related_name='site_created_by', blank=True, null=True)
    active = models.NullBooleanField()
    capture_coord_sys = models.TextField(blank=True, null=True)
    documents = models.ManyToManyField(SiteDocument, related_name='documents', through=AssociationDocsTable)
    heritage_surveys = models.ManyToManyField(HeritageSurvey, through=AssociationSitesSurveyTable)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    def __str__(self):
        return smart_text("Site {}".format(self.site_id))

    class Meta:
        managed = False
        db_table = 'sites'


class SurveyStatus(models.Model):
    survey_status_id = models.AutoField(primary_key=True)
    status = models.CharField(unique=True, max_length=8, blank=True, null=True)

    def __str__(self):
        return smart_text(self.status)

    class Meta:
        managed = True
        db_table = 'survey_status'


class SurveyTrip(models.Model):
    survey_trip_id = models.AutoField(primary_key=True)
    survey_id = models.CharField(max_length=50, blank=True, null=True)
    trip_number = models.SmallIntegerField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)

    def __str__(self):
        str = ""
        if self.trip_number:
            str = "{}_(Trip {})".format(self.survey_id, self.trip_number)
        else:
            str = "{}".format(self.survey_id)
        return smart_text(str)

    class Meta:
        managed = False
        db_table = 'survey_trips'


class SurveyType(models.Model):
    type_id = models.CharField(unique=True, max_length=4, primary_key=True)
    description = models.CharField(unique=True, max_length=25, blank=True, null=True)

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        managed = False
        db_table = 'ymac_claims'


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

    def __str__(self):
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
    id = models.FloatField(primary_key=True)
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.name)

    class Meta:
        managed = False
        db_table = 'ymac_region'


class YmacStaff(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    email = models.TextField(blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.full_name)

    class Meta:
        managed = False
        db_table = 'ymac_staff'


class CaptureOrg(models.Model):
    organisation_name = models.TextField()
    organisation_website = models.TextField(blank=True, null=True)
    organisation_phone = models.CharField(max_length=16, blank=True, null=True)
    organisation_contact = models.TextField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.organisation_name)


class SiteUser(models.Model):
    user_name = models.TextField(blank=True, null=True)
    employee = models.NullBooleanField()
    capture_org = models.ForeignKey('CaptureOrg', blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    def __str__(self):
        return smart_text(self.user_name)
