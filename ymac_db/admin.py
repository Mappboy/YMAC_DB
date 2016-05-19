# Register your models here.
# Change lat long and layer models for these geo models
# MAke sure they are converted to 4283
# Set List display
# Create our own map template
from django.contrib.gis import admin

from .forms import *


class YMACModelAdmin(admin.GeoModelAdmin):
    default_lat = -27
    default_lon = 121


models = [SiteUser,
          CaptureOrg,
          SurveyTrip,
          SiteDocument,
          SiteDescriptions,
          RestrictionStatus]

for m in models:
    admin.site.register(m)


# ADD Site Document Inline
# SEe https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-many-to-many-models


class SiteDocumentInline(admin.TabularInline):
    model = Site.docs.through


class SiteSurveyInline(admin.TabularInline):
    model = Site.surveys.through


class HeritageSiteDocumentInline(admin.TabularInline):
    model = HeritageSite.heritage_surveys.through


class HeritageSiteSurveyInline(admin.TabularInline):
    model = HeritageSite.documents.through


class ResearchSiteDocumentInline(admin.TabularInline):
    model = ResearchSite.documents.through


@admin.register(Site)
class SiteAdmin(admin.GeoModelAdmin):
    inlines = [
    ]
    list_display = ['site_id',
                    'recorded_by',
                    'date_recorded',
                    'group_name',
                    'restricted_status']
    list_filter = ['site_id',
                   'recorded_by',
                   'date_recorded',
                   'group_name',
                   'restricted_status']

    search_fields = [
        'group_name',
    ]


@admin.register(HeritageSite)
class HeritageSiteAdmin(SiteAdmin):
    inlines = [
    ]
    list_display = [
        'site_description',
        'boundary_description',
        'disturbance_level',
        'status',
        'site_comments'
    ]
    list_filter = [
        'site_description',
        'boundary_description',
        'disturbance_level',
        'status',
        'site_comments'
    ]
    search_fields = [
        'site_comments',
    ]
    form = HeritageSiteForm

@admin.register(ResearchSite)
class ResearchSiteAdmin(SiteAdmin):
    inlines = [
    ]
    list_display = [
        'site_classification',
        'site_category',
        'site_location',
        'site_comments',
        'site_name'
    ]
    list_filter = [
        'site_classification',
        'site_category',
        'site_location',
        'site_comments',
        'site_name'
    ]

    search_fields = [
        'site_name',
    ]

@admin.register(HeritageSurvey)
class HeritageSurveyAdmin(admin.GeoModelAdmin):
    list_display = [
        'survey_trip',
        'status',
        'source',
        'comments',
        'proponent_id',
        'claim_group_id',
        'survey_type',
        'sampling_meth',
        'ymac_svy_name',
        'date_create',
        'sampling_conf',
        'created_by',
        'data_supplier',
        'collected_by'
    ]
    search_fields = [
        'ymac_svy_name',
        'proponent_id',
    ]
    list_filter = [
        'survey_type',
    ]
    form = HeritageSurveyForm


@admin.register(DaaSite)
class DAASiteAdmin(admin.GeoModelAdmin):
    list_display = [
        'place_id',
        'status',
        'name',
        'status_reason',
        'origin_place_id',
        'type',
        'region',
        'restrictions',
        'file_restricted',
        'location_restricted',
        'boundary_reliable',
        'protected_area',
        'protected_area_gazetted_date',
        'national_estate_area',
        'boundary_last_update_date',
        'shape_length',
        'shape_area',
    ]
    search_fields = ['name', 'place_id']
    list_filter = [
        'status',
        'region',
        'type'
    ]

geom_models = [
    YmacRegion,
    Tenement,

]
for gm in geom_models:
    admin.site.register(gm, YMACModelAdmin)

