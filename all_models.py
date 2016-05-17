# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.gis.db import models


class AssociationDocsTable(models.Model):
    ymac_site = models.ForeignKey('Sites', models.DO_NOTHING)
    site_doc = models.ForeignKey('SiteDocuments', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'association_docs_table'
        unique_together = (('ymac_site', 'site_doc'),)


class AssociationExtSitesTable(models.Model):
    ymac_site = models.ForeignKey('Sites', models.DO_NOTHING)
    external = models.ForeignKey('ExternalClientSites', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'association_ext_sites_table'
        unique_together = (('ymac_site', 'external'),)


class AssociationSitesSurveyTable(models.Model):
    ymac_site = models.ForeignKey('Sites', models.DO_NOTHING)
    ymac_survey = models.ForeignKey('SurveyTrips', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'association_sites_survey_table'
        unique_together = (('ymac_site', 'ymac_survey'),)


class AssociationSitesTable(models.Model):
    ymac_site = models.ForeignKey('Sites', models.DO_NOTHING)
    daa_site = models.ForeignKey('DaaSites', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'association_sites_table'
        unique_together = (('ymac_site', 'daa_site'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cadastre(models.Model):
    alternate_pi_parcel = models.CharField(max_length=17, blank=True, null=True)
    alternate_pi_type = models.CharField(max_length=1, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    area_derivation_indicator = models.CharField(max_length=1, blank=True, null=True)
    area_derivation_method = models.CharField(max_length=2, blank=True, null=True)
    calculated_area = models.FloatField(blank=True, null=True)
    centroid_coordinate_method = models.CharField(max_length=1, blank=True, null=True)
    centroid_latitude = models.FloatField(blank=True, null=True)
    centroid_longitude = models.FloatField(blank=True, null=True)
    date_poly_boundary_modified = models.DateField(blank=True, null=True)
    date_poly_created = models.DateField(blank=True, null=True)
    date_poly_modified = models.DateField(blank=True, null=True)
    date_poly_retired = models.DateField(blank=True, null=True)
    gml_id = models.TextField(blank=True, null=True)
    gml_parent_id = models.TextField(blank=True, null=True)
    gml_parent_property = models.TextField(blank=True, null=True)
    land_id_number = models.IntegerField()
    land_type = models.CharField(max_length=5, blank=True, null=True)
    lga_name = models.CharField(max_length=60, blank=True, null=True)
    lot_number = models.SmallIntegerField(blank=True, null=True)
    ogc_fid = models.IntegerField(blank=True, null=True)
    pi_parcel = models.CharField(max_length=17, blank=True, null=True)
    pi_type = models.CharField(max_length=1, blank=True, null=True)
    polygon_number = models.IntegerField()
    render_normal = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)
    usage_code = models.IntegerField(blank=True, null=True)
    view_scale = models.CharField(max_length=1, blank=True, null=True)
    geom = models.MultiPolygonField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cadastre'
        unique_together = (('land_id_number', 'polygon_number'), ('land_id_number', 'polygon_number'),)


class DaaSites(models.Model):
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

    class Meta:
        managed = False
        db_table = 'daa_sites'


class DataSuppliers(models.Model):
    supplier = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'data_suppliers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExternalClientSites(models.Model):
    external_id = models.AutoField(primary_key=True)
    external_site_id = models.CharField(max_length=-1, blank=True, null=True)
    site_name = models.CharField(max_length=-1, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'external_client_sites'


class HeritageSites(models.Model):
    heritage_site_id = models.AutoField(primary_key=True)
    site_description = models.ForeignKey('YmacDbSitedescriptions', models.DO_NOTHING, blank=True, null=True)
    boundary_description = models.CharField(max_length=30, blank=True, null=True)
    disturbance_level = models.CharField(max_length=30, blank=True, null=True)
    site_comments = models.CharField(max_length=-1, blank=True, null=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING, blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'heritage_sites'


class HeritageSitesDocuments(models.Model):
    heritagesite = models.ForeignKey(HeritageSites, models.DO_NOTHING)
    sitedocument = models.ForeignKey('SiteDocuments', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'heritage_sites_documents'
        unique_together = (('heritagesite', 'sitedocument'),)


class HeritageSitesHeritageSurveys(models.Model):
    heritagesite = models.ForeignKey(HeritageSites, models.DO_NOTHING)
    heritagesurvey = models.ForeignKey('HeritageSurveys', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'heritage_sites_heritage_surveys'
        unique_together = (('heritagesite', 'heritagesurvey'),)


class HeritageSurveys(models.Model):
    survey_trip_id = models.AutoField(primary_key=True)
    status = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    proponent_id = models.CharField(max_length=5, blank=True, null=True)
    claim_group_id = models.CharField(max_length=5, blank=True, null=True)
    survey_type = models.ForeignKey('SurveyTypes', models.DO_NOTHING, db_column='survey_type', blank=True, null=True)
    sampling_meth = models.ForeignKey('SampleMethodology', models.DO_NOTHING, db_column='sampling_meth', blank=True,
                                      null=True)
    ymac_svy_name = models.CharField(max_length=200, blank=True, null=True)
    survey_name = models.CharField(max_length=200, blank=True, null=True)
    date_create = models.DateField(blank=True, null=True)
    sampling_conf = models.ForeignKey('SamplingConfidence', models.DO_NOTHING, db_column='sampling_conf', blank=True,
                                      null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    date_mod = models.DateField(blank=True, null=True)
    mod_by = models.CharField(max_length=200, blank=True, null=True)
    propref = models.CharField(max_length=200, blank=True, null=True)
    geom = models.GeometryField(srid=28350, blank=True, null=True)
    data_supplier = models.ForeignKey(DataSuppliers, models.DO_NOTHING, db_column='data_supplier', blank=True,
                                      null=True)
    data_qa = models.BooleanField()
    collected_by = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'heritage_surveys'


class HsRioCodes(models.Model):
    survey_trip = models.ForeignKey(HeritageSurveys, models.DO_NOTHING)
    field_rac_table = models.CharField(db_column='_rac_table', max_length=50, blank=True,
                                       null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'hs_rio_codes'


class HsSvmythlgy(models.Model):
    survey_trip = models.ForeignKey(HeritageSurveys, models.DO_NOTHING)
    svy_meth = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hs_svmythlgy'


class Ilua(models.Model):
    name = models.CharField(max_length=102, blank=True, null=True)
    tribid = models.CharField(max_length=30, blank=True, null=True)
    agstatus = models.CharField(max_length=100, blank=True, null=True)
    datelodged = models.DateField(blank=True, null=True)
    datenotif = models.DateField(blank=True, null=True)
    notifclose = models.DateField(blank=True, null=True)
    dateregd = models.DateField(blank=True, null=True)
    subjmatter = models.CharField(max_length=254, blank=True, null=True)
    agtype = models.CharField(max_length=25, blank=True, null=True)
    consentfa = models.CharField(max_length=1, blank=True, null=True)
    rtn = models.CharField(max_length=1, blank=True, null=True)
    surrareas = models.CharField(max_length=1, blank=True, null=True)
    validatefa = models.CharField(max_length=1, blank=True, null=True)
    intermacts = models.CharField(max_length=1, blank=True, null=True)
    agauth = models.CharField(max_length=10, blank=True, null=True)
    applicant = models.CharField(max_length=50, blank=True, null=True)
    rep = models.CharField(max_length=102, blank=True, null=True)
    casemgr = models.CharField(max_length=25, blank=True, null=True)
    timefstart = models.DateField(blank=True, null=True)
    timefend = models.DateField(blank=True, null=True)
    areasqkm = models.FloatField(blank=True, null=True)
    datasource = models.CharField(max_length=60, blank=True, null=True)
    datecurr = models.DateField(blank=True, null=True)
    seailua = models.CharField(max_length=1, blank=True, null=True)
    zonelwm = models.CharField(max_length=1, blank=True, null=True)
    zone3nm = models.CharField(max_length=1, blank=True, null=True)
    zone12nm = models.CharField(max_length=1, blank=True, null=True)
    zone24nm = models.CharField(max_length=1, blank=True, null=True)
    zoneeez = models.CharField(max_length=1, blank=True, null=True)
    nnttseqno = models.CharField(primary_key=True, max_length=14)
    objectind = models.CharField(max_length=1, blank=True, null=True)
    sptialnote = models.CharField(max_length=120, blank=True, null=True)
    gtref = models.CharField(max_length=10, blank=True, null=True)
    s78id = models.CharField(max_length=254, blank=True, null=True)
    dateassist = models.DateField(blank=True, null=True)
    juris = models.CharField(max_length=10, blank=True, null=True)
    overlap = models.CharField(max_length=20, blank=True, null=True)
    tribno = models.CharField(max_length=12, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(srid=3577, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ilua'


class IluaGeog(models.Model):
    nnttseqno = models.CharField(primary_key=True, max_length=14)
    date_created = models.CharField(max_length=30, blank=True, null=True)
    geog = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ilua_geog'


class LandgateHistory(models.Model):
    operation = models.CharField(max_length=7, blank=True, null=True)
    table_name = models.CharField(max_length=8, blank=True, null=True)
    pi_type = models.CharField(max_length=1, blank=True, null=True)
    pi_parcel = models.CharField(max_length=17, blank=True, null=True)
    polygon_number = models.IntegerField()
    land_id_number = models.IntegerField()
    usage_code = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)
    modified_time = models.DateTimeField()
    date_poly_mod = models.DateField(blank=True, null=True)
    date_modified = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'landgate_history'
        unique_together = (('polygon_number', 'land_id_number', 'modified_time'),)


class LayerStyles(models.Model):
    f_table_catalog = models.CharField(max_length=256, blank=True, null=True)
    f_table_schema = models.CharField(max_length=256, blank=True, null=True)
    f_table_name = models.CharField(max_length=256, blank=True, null=True)
    f_geometry_column = models.CharField(max_length=256, blank=True, null=True)
    stylename = models.CharField(max_length=30, blank=True, null=True)
    styleqml = models.TextField(blank=True, null=True)  # This field type is a guess.
    stylesld = models.TextField(blank=True, null=True)  # This field type is a guess.
    useasdefault = models.NullBooleanField()
    description = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=30, blank=True, null=True)
    ui = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layer_styles'


class LotTypes(models.Model):
    lot_type = models.CharField(max_length=6, blank=True, null=True)
    description = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lot_types'


class NnttDeterminations(models.Model):
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
    geom = models.GeometryField(srid=3577, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nntt_determinations'


class NnttDeterminationsGeog(models.Model):
    nnttseqno = models.CharField(primary_key=True, max_length=14)
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nntt_determinations_geog'


class NonYmacClaims(models.Model):
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
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(srid=3577, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'non_ymac_claims'


class NonYmacClaimsGeog(models.Model):
    nnttseqno = models.CharField(primary_key=True, max_length=30)
    date_created = models.CharField(max_length=20, blank=True, null=True)
    geog = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'non_ymac_claims_geog'


class Outcomes(models.Model):
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
    ymac_det = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(srid=3577, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'outcomes'


class OutcomesGeog(models.Model):
    nnttseqno = models.CharField(primary_key=True, max_length=14)
    date_created = models.DateTimeField(blank=True, null=True)
    geog = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'outcomes_geog'


class Proponents(models.Model):
    prop_id = models.CharField(primary_key=True, max_length=10)
    name = models.TextField()
    contact = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proponents'


class ResearchSites(models.Model):
    research_site_id = models.AutoField(primary_key=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING, blank=True, null=True)
    site_classification = models.CharField(max_length=30, blank=True, null=True)
    site_location = models.CharField(max_length=30, blank=True, null=True)
    site_comments = models.CharField(max_length=-1, blank=True, null=True)
    ethno_detail = models.CharField(max_length=-1, blank=True, null=True)
    reference = models.CharField(max_length=-1, blank=True, null=True)
    site_name = models.CharField(max_length=-1, blank=True, null=True)
    site_label = models.CharField(max_length=-1, blank=True, null=True)
    alt_site_name = models.CharField(max_length=-1, blank=True, null=True)
    site_number = models.IntegerField(blank=True, null=True)
    site_category = models.CharField(max_length=30, blank=True, null=True)
    family_affiliation = models.TextField(blank=True, null=True)
    mapsheet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'research_sites'


class ResearchSitesDocuments(models.Model):
    researchsite = models.ForeignKey(ResearchSites, models.DO_NOTHING)
    sitedocument = models.ForeignKey('SiteDocuments', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'research_sites_documents'
        unique_together = (('researchsite', 'sitedocument'),)


class Reserves(models.Model):
    area = models.FloatField(blank=True, null=True)
    area_derivation_indicator = models.CharField(max_length=1, blank=True, null=True)
    area_derivation_method = models.CharField(max_length=2, blank=True, null=True)
    calculated_area = models.FloatField(blank=True, null=True)
    centroid_coordinate_method = models.CharField(max_length=1, blank=True, null=True)
    centroid_latitude = models.FloatField(blank=True, null=True)
    centroid_longitude = models.FloatField(blank=True, null=True)
    current_purpose = models.CharField(max_length=2000, blank=True, null=True)
    date_time_boundary_modified = models.DateField(blank=True, null=True)
    date_time_created = models.DateField(blank=True, null=True)
    date_time_modified = models.DateField(blank=True, null=True)
    date_time_retired = models.DateField(blank=True, null=True)
    detail_text = models.CharField(max_length=2000, blank=True, null=True)
    detail_type = models.CharField(max_length=2000, blank=True, null=True)
    gml_id = models.TextField(blank=True, null=True)
    gml_parent_id = models.TextField(blank=True, null=True)
    gml_parent_property = models.TextField(blank=True, null=True)
    land_id_number = models.IntegerField()
    land_type = models.CharField(max_length=6, blank=True, null=True)
    legal_area = models.FloatField(blank=True, null=True)
    lga = models.CharField(max_length=60, blank=True, null=True)
    lot_number = models.IntegerField(blank=True, null=True)
    lu1 = models.CharField(max_length=255, blank=True, null=True)
    lu2 = models.CharField(max_length=255, blank=True, null=True)
    lu3 = models.CharField(max_length=255, blank=True, null=True)
    lu4 = models.CharField(max_length=255, blank=True, null=True)
    lu5 = models.CharField(max_length=255, blank=True, null=True)
    mo1 = models.CharField(max_length=255, blank=True, null=True)
    mo2 = models.CharField(max_length=255, blank=True, null=True)
    mo3 = models.CharField(max_length=255, blank=True, null=True)
    mo4 = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    ogc_fid = models.IntegerField(blank=True, null=True)
    org_gaz_page = models.IntegerField(blank=True, null=True)
    org_gazl_date = models.TextField(blank=True, null=True)
    pi_parcel = models.CharField(max_length=17, blank=True, null=True)
    pi_type = models.CharField(max_length=1, blank=True, null=True)
    polygon_number = models.IntegerField()
    render_normal = models.CharField(max_length=12, blank=True, null=True)
    reserve_class = models.CharField(max_length=1, blank=True, null=True)
    reserve_date_time_created = models.TextField(blank=True, null=True)
    reserve_date_time_updated = models.TextField(blank=True, null=True)
    reserve_name = models.CharField(max_length=2000, blank=True, null=True)
    reserve_nfn_additional_text = models.CharField(max_length=400, blank=True, null=True)
    reserve_number = models.IntegerField(blank=True, null=True)
    reserveno = models.CharField(max_length=17, blank=True, null=True)
    responsible_agency = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=5, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)
    type_field = models.CharField(db_column='type_', max_length=22, blank=True,
                                  null=True)  # Field renamed because it ended with '_'.
    usage_code = models.IntegerField(blank=True, null=True)
    vesting = models.CharField(max_length=255, blank=True, null=True)
    view_scale = models.CharField(max_length=1, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reserves'
        unique_together = (('land_id_number', 'polygon_number'), ('land_id_number', 'polygon_number'),)


class RestrictionStatus(models.Model):
    rid = models.AutoField(primary_key=True)
    gender = models.TextField(blank=True, null=True)  # This field type is a guess.
    claim = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'restriction_status'


class SampleMethodology(models.Model):
    sampling_meth = models.CharField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_methodology'


class SamplingConfidence(models.Model):
    sampling_conf = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'sampling_confidence'


class SiteDocuments(models.Model):
    doc_id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=15, blank=True, null=True)
    filepath = models.CharField(max_length=-1, blank=True, null=True)
    filename = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_documents'


class Sites(models.Model):
    site_id = models.AutoField(primary_key=True)
    recorded_by = models.ForeignKey('YmacDbSiteuser', models.DO_NOTHING, db_column='recorded_by', blank=True, null=True)
    date_recorded = models.DateField(blank=True, null=True)
    group_name = models.CharField(max_length=-1, blank=True, null=True)
    restricted_status = models.ForeignKey(RestrictionStatus, models.DO_NOTHING, db_column='restricted_status',
                                          blank=True, null=True)
    label_x_ll = models.FloatField(blank=True, null=True)
    label_y_ll = models.FloatField(blank=True, null=True)
    date_created = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey('YmacDbSiteuser', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    active = models.NullBooleanField()
    capture_coord_sys = models.CharField(max_length=-1, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sites'


class SurveyStatus(models.Model):
    status = models.CharField(unique=True, max_length=8, blank=True, null=True)
    survey_status_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'survey_status'


class SurveyTrips(models.Model):
    survey_trip_id = models.AutoField(primary_key=True)
    survey_id = models.CharField(max_length=50, blank=True, null=True)
    trip_number = models.SmallIntegerField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_trips'


class SurveyTypes(models.Model):
    type_id = models.CharField(primary_key=True, max_length=4)
    description = models.CharField(unique=True, max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_types'


class TenGprpfx(models.Model):
    values = models.CharField(primary_key=True, max_length=1)
    description = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ten_gprpfx'


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

    class Meta:
        managed = False
        db_table = 'tenement'


class TenementHistory(models.Model):
    operation = models.CharField(max_length=1)
    stamp = models.DateTimeField()
    userid = models.TextField()
    region = models.CharField(max_length=1)
    type = models.CharField(max_length=50, blank=True, null=True)
    survstatus = models.CharField(max_length=15, blank=True, null=True)
    tenstatus = models.CharField(max_length=10, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    grantdate = models.DateField(blank=True, null=True)
    granttime = models.TimeField(blank=True, null=True)
    fmt_tenid = models.CharField(max_length=16, blank=True, null=True)
    legal_area = models.FloatField(blank=True, null=True)
    unit_of_me = models.CharField(max_length=4, blank=True, null=True)
    special_in = models.CharField(max_length=1, blank=True, null=True)
    extract_date = models.DateField(blank=True, null=True)
    combined_r = models.CharField(max_length=10, blank=True, null=True)
    all_holder = models.CharField(max_length=254, blank=True, null=True)
    field_timestamp = models.DateTimeField(db_column='_timestamp', blank=True,
                                           null=True)  # Field renamed because it started with '_'.
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenement_history'


class TenementsAll(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True)
    survstatus = models.CharField(max_length=15, blank=True, null=True)
    tenstatus = models.CharField(max_length=10, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    grantdate = models.DateField(blank=True, null=True)
    granttime = models.TimeField(blank=True, null=True)
    fmt_tenid = models.CharField(primary_key=True, max_length=16)
    legal_area = models.FloatField(blank=True, null=True)
    unit_of_me = models.CharField(max_length=4, blank=True, null=True)
    special_in = models.CharField(max_length=1, blank=True, null=True)
    extract_da = models.DateField(blank=True, null=True)
    combined_r = models.CharField(max_length=10, blank=True, null=True)
    all_holder = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenements_all'


class TenementsYmac(models.Model):
    type = models.CharField(max_length=50, blank=True, null=True)
    survstatus = models.CharField(max_length=15, blank=True, null=True)
    tenstatus = models.CharField(max_length=10, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    grantdate = models.DateField(blank=True, null=True)
    granttime = models.TimeField(blank=True, null=True)
    fmt_tenid = models.CharField(max_length=16, blank=True, null=True)
    legal_area = models.FloatField(blank=True, null=True)
    unit_of_me = models.CharField(max_length=4, blank=True, null=True)
    special_in = models.CharField(max_length=1, blank=True, null=True)
    extract_da = models.DateField(blank=True, null=True)
    combined_r = models.CharField(max_length=10, blank=True, null=True)
    all_holder = models.CharField(max_length=254, blank=True, null=True)
    field_timestamp = models.DateTimeField(db_column='_timestamp', blank=True,
                                           null=True)  # Field renamed because it started with '_'.
    geom = models.GeometryField(srid=4283, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenements_ymac'


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
    geom = models.MultiPolygonField(srid=0, blank=True, null=True)
    dealing_type = models.CharField(max_length=2, blank=True, null=True)
    register = models.CharField(max_length=13, blank=True, null=True)
    address_no_type = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenure'
        unique_together = (('land_id_number', 'polygon_number'), ('land_id_number', 'polygon_number'),)


class TenureOrgCode(models.Model):
    org_code = models.CharField(primary_key=True, max_length=3)
    legal_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenure_org_code'


class TestDelete(models.Model):
    val1 = models.CharField(max_length=2, blank=True, null=True)
    val2 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'test_delete'


class TrainingResponses(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    proficiency = models.SmallIntegerField(blank=True, null=True)
    qgis_version = models.CharField(max_length=12, blank=True, null=True)
    session1 = models.NullBooleanField()
    session2 = models.NullBooleanField()
    session3 = models.NullBooleanField()
    laptop = models.CharField(max_length=30, blank=True, null=True)
    further_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'training_responses'


class UsageCodes(models.Model):
    code = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usage_codes'


class Wapspaao(models.Model):
    title_id = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    lodged = models.DateField(blank=True, null=True)
    issued = models.DateField(blank=True, null=True)
    spa_expiry = models.DateField(blank=True, null=True)
    ao_expiry = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    act_abbrev = models.CharField(max_length=12, blank=True, null=True)
    blocks = models.FloatField(blank=True, null=True)
    program = models.CharField(max_length=60, blank=True, null=True)
    holder_1 = models.CharField(max_length=70, blank=True, null=True)
    holder_2 = models.CharField(max_length=70, blank=True, null=True)
    holder_3 = models.CharField(max_length=70, blank=True, null=True)
    holder_4 = models.CharField(max_length=70, blank=True, null=True)
    holder_5 = models.CharField(max_length=70, blank=True, null=True)
    holder_6 = models.CharField(max_length=70, blank=True, null=True)
    holder_7 = models.CharField(max_length=70, blank=True, null=True)
    holder_8 = models.CharField(max_length=70, blank=True, null=True)
    mapsheet_1 = models.CharField(max_length=25, blank=True, null=True)
    mapsheet_2 = models.CharField(max_length=25, blank=True, null=True)
    mapsheet_3 = models.CharField(max_length=25, blank=True, null=True)
    mapsheet_4 = models.CharField(max_length=25, blank=True, null=True)
    extract_da = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wapspaao'


class Waptitle(models.Model):
    title_id = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    issued = models.DateField(blank=True, null=True)
    expiry = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    act_abbrev = models.CharField(max_length=12, blank=True, null=True)
    blocks = models.FloatField(blank=True, null=True)
    program = models.CharField(max_length=60, blank=True, null=True)
    coverage = models.CharField(max_length=60, blank=True, null=True)
    holder_1 = models.CharField(max_length=70, blank=True, null=True)
    holder_2 = models.CharField(max_length=70, blank=True, null=True)
    holder_3 = models.CharField(max_length=70, blank=True, null=True)
    holder_4 = models.CharField(max_length=70, blank=True, null=True)
    holder_5 = models.CharField(max_length=70, blank=True, null=True)
    holder_6 = models.CharField(max_length=70, blank=True, null=True)
    holder_7 = models.CharField(max_length=70, blank=True, null=True)
    holder_8 = models.CharField(max_length=70, blank=True, null=True)
    mapsheet_1 = models.CharField(max_length=25, blank=True, null=True)
    mapsheet_2 = models.CharField(max_length=25, blank=True, null=True)
    mapsheet_3 = models.CharField(max_length=25, blank=True, null=True)
    mapsheet_4 = models.CharField(max_length=25, blank=True, null=True)
    extract_da = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waptitle'


class YmacClaims(models.Model):
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
    geom = models.GeometryField(srid=3577, blank=True, null=True)
    claim_group_id = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ymac_claims'


class YmacClaimsGeog(models.Model):
    nnttseqno = models.CharField(primary_key=True, max_length=14)
    date_created = models.DateTimeField(blank=True, null=True)
    geog = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ymac_claims_geog'


class YmacDbCaptureorg(models.Model):
    organisation_name = models.TextField()
    organisation_website = models.TextField(blank=True, null=True)
    organisation_phone = models.CharField(max_length=16, blank=True, null=True)
    organisation_contact = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ymac_db_captureorg'


class YmacDbSitedescriptions(models.Model):
    site_description = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'ymac_db_sitedescriptions'


class YmacDbSiteuser(models.Model):
    employee = models.NullBooleanField()
    email = models.TextField(blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    capture_org = models.ForeignKey(YmacDbCaptureorg, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ymac_db_siteuser'


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
    geom = models.GeometryField(srid=28350, blank=True, null=True)
    modified_time = models.DateTimeField()

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
    geom = models.PolygonField(srid=4283, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ymac_region'


class YmacRegionGeog(models.Model):
    id = models.FloatField(primary_key=True)
    date_created = models.DateTimeField(blank=True, null=True)
    geog = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ymac_region_geog'


class YmacStaff(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    email = models.TextField(blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ymac_staff'
