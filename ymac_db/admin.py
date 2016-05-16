# Register your models here.
# Change lat long and layer models for these geo models
# MAke sure they are converted to 4283
# Set List display
# Create our own map template
from django.contrib.gis import admin

from .models import *


class YMACModelAdmin(admin.GeoModelAdmin):
    default_lat = -27
    default_lon = 121


@admin.register(Site)
class SiteAdmin(admin.GeoModelAdmin):
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
    list_display = [
        'site',
        'site_description',
        'boundary_description',
        'disturbance_level',
        'status',
        'site_comments'
    ]
    list_filter = [
        'site',
        'site_description',
        'boundary_description',
        'disturbance_level',
        'status',
        'site_comments'
    ]


@admin.register(ResearchSite)
class ResearchSiteAdmin(SiteAdmin):
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
]
for gm in geom_models:
    admin.site.register(gm, YMACModelAdmin)

models = [YmacStaff,
          Ymacuser,
          SurveyTrip,
          SiteDocument,
          AssociationDocsTable,
          AssociationSitesSurveyTable,
          RestrictionStatus]

for m in models:
    admin.site.register(m)
