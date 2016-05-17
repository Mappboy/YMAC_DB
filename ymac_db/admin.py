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
          AssociationDocsTable,
          AssociationSitesSurveyTable,
          RestrictionStatus]

for m in models:
    admin.site.register(m)


# ADD Site Document Inline
# SEe https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-many-to-many-models


class SiteDocumentInline(admin.TabularInline):
    model = Site.documents.through


class SiteSurveyInline(admin.TabularInline):
    model = Site.heritage_surveys.through


class HeritageSiteDocumentInline(admin.TabularInline):
    model = HeritageSite.heritage_surveys.through


class HeritageSiteSurveyInline(admin.TabularInline):
    model = HeritageSite.documents.through


class ResearchSiteDocumentInline(admin.TabularInline):
    model = ResearchSite.researchdocuments.through


@admin.register(Site)
class SiteAdmin(admin.GeoModelAdmin):
    inlines = [
        SiteDocumentInline,
        SiteSurveyInline
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

    form = HeritageSiteForm

@admin.register(ResearchSite)
class ResearchSiteAdmin(SiteAdmin):
    inlines = [
        ResearchSiteDocumentInline
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


geom_models = [
    YmacRegion,
    DaaSite,
    Tenement,
    HeritageSurvey
]
for gm in geom_models:
    admin.site.register(gm, YMACModelAdmin)
