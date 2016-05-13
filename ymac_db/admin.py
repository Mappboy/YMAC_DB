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


geom_models = [
    YmacRegion,
    Site,
    DaaSite,
    Tenement,
    HeritageSite,
    ResearchSite
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
