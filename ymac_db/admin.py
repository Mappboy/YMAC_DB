# Register your models here.
# Change lat long and layer models for these geo models
# MAke sure they are converted to 4283
# Set List display
# Create our own map template
from django.contrib.gis import admin
from django.contrib import admin as baseadmin
from django.utils.translation import ugettext_lazy as _
from .forms import *
import re


class SiteTypeFilter(baseadmin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Site Type')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Arch', _('Archeological')),
            ('Ethno', _('Ethnographic')),
            ('Unknown', _('Unknown')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'Unknown':
            return queryset.filter(type_exact='')
        if self.value() == 'Ethno':
            return queryset.filter(type__iregex=('^(Birth Place|'
                                                 'Camp|'
                                                 'Ceremonial|'
                                                 'Engraving|'
                                                 'Historical|'
                                                 'Hunting Place|'
                                                 'Man-Made Structure|'
                                                 'Massacre|'
                                                 'Meeting Place|'
                                                 'Mythological|'
                                                 'Named Place|'
                                                 'Natural Feature|'
                                                 'Ochre|'
                                                 'Other: CONFIDENTIAL'
                                                 'Other: DEATH PLACE|'
                                                 'Other: DEATH SITE|'
                                                 'Other: FEATURE|'
                                                 'Other: FOOD RESOURCE|'
                                                 'Other: Former camp|'
                                                 'Other: LOCAL GROUP SITE|'
                                                 'Other: SIGN SHOWS ABORIGINAL DESIGN|'
                                                 'Other: Significant Tree|'
                                                 'Other: SPRING|'
                                                 'Other: WALLED CAVE|'
                                                 'Other: Watercourse|'
                                                 'Painting|'
                                                 'Plant Resource|'
                                                 'Rockshelter|'
                                                 'Skeletal Material / Burial|'
                                                 'Water Source)'))
        if self.value() == 'Arch':
            return queryset.filter(type__iregex=('^(Arch Deposit|'
                                                 'Artefacts / Scatter|'
                                                 'Fish Trap|'
                                                 'Grinding Patches / Grooves|'
                                                 'Midden / Scatter|'
                                                 'Modified Tree|'
                                                 'Other: \(NOT A SITE\)|'
                                                 'Other:|'
                                                 'Other: \[EXCLUDED FROM MARANDOO ACT\]|'
                                                 'Other: Aboriginal track|'
                                                 'Other: ANIMAL REMAINS|'
                                                 'Other: Circular mounds|'
                                                 'Other: CLAYPAN|'
                                                 'Other: Exploited Stone Sources|'
                                                 'Other: FOSSILISED FOOTPRINT|'
                                                 'Other: GNAMMA HOLE|'
                                                 'Other: GNAMMA HOLES|'
                                                 'Other: IMP. AREA - JIG PPL|'
                                                 'Other: KANGAROO TRAPS|'
                                                 'Other: LIZARD TRAP|'
                                                 'Other: MANUFACTURE SITE|'
                                                 'Other: MARKED TREE|'
                                                 'Other: MARKED TREES|'
                                                 'Other: MATERIAL RESOURCE|'
                                                 'Other: MULTI TRAIT|'
                                                 'Other: No|'
                                                 'Other: one circular mound|'
                                                 'Other: PA 67|'
                                                 'Other: Proposed|'
                                                 'Other: ROCK CAIRNS|'
                                                 'Other: ROCKHOLE|'
                                                 'Other: SCARRED TREES?|'
                                                 'Other: WORKSHOP|'
                                                 'Quarry|'
                                                 'Repository / Cache|'
                                                 'Shell)'))

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
class SiteAdmin(YMACModelAdmin):
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
        SiteTypeFilter
    ]

geom_models = [
    YmacRegion,
    Tenement,

]
for gm in geom_models:
    admin.site.register(gm, YMACModelAdmin)

