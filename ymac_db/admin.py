# Register your models here.
# Change lat long and layer models for these geo models
# MAke sure they are converted to 4283
# Set List display
# Create our own map template
from django.contrib import admin as baseadmin
from django.contrib.gis import forms as geoforms
from django.contrib.gis import admin
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from leaflet.admin import LeafletGeoAdmin

from .forms import *


class HasGeomFilter(baseadmin.SimpleListFilter):
    title = _('Spatial Data Exists')

    parameter_name = 'geom'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (True, _('Exists')),
            (False, _('No Spatial Data')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if not self.value():
            return queryset.all()
        else:
            return queryset.filter(geom__isnull=self.value())


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
            return queryset.filter(type__exact='')
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


class YMACModelAdmin(LeafletGeoAdmin):
    default_lat = -27
    default_lon = 121
    # formfield_overrides = {
    #    models.GeometryField: {'widget': OSMWidget},
    # }


basemodels = [SiteUser,
              CaptureOrg,
              HeritageSurveyTrip,
              SiteDocument,
              SiteDescriptions,
              RestrictionStatus,
              SurveyMethodology,
              Consultant,
              Proponent,
              RelatedSurveyCode,
              SurveyProponentCode,
              SurveyCleaning]

for m in basemodels:
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


class HeritageSurveyConsultantInline(admin.TabularInline):
    model = HeritageSurvey.consultants.through


class HeritageSurveyProponentInline(admin.TabularInline):
    model = HeritageSurvey.proponent_codes.through


class HeritageSurveyCleaningInline(admin.TabularInline):
    model = HeritageSurvey.data_source.through


@admin.register(Site)
class SiteAdmin(YMACModelAdmin):
    inlines = [
    ]
    formfield_overrides = {
        models.GeometryField: {'widget': geoforms.OSMWidget},
    }
    list_display = [
        'site_identifier',
        'recorded_by',
        'date_recorded',
        'group_name',
        'restricted_status']
    list_filter = [
        'recorded_by',
        'date_recorded',
        'group_name',
        'restricted_status']

    search_fields = [
        'group_name',
    ]
    form = SiteForm


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


def get_surveyids(modeladmin, request, queryset):
    for qs in queryset:
        print(qs.id)
    print(modeladmin.model._meta.db_table)


get_surveyids.short_description = "Get selected survey ids"


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("geojson", queryset, stream=response)
    return response


def export_as_shz(modeladmin, request, queryset):
    response_dict = {'id_list': [], 'db_table': modeladmin.model._meta.db_table}
    for qs in queryset:
        response_dict['id_list'].append(qs.id)
    ids = ",".join([smart_text(id) for id in response_dict['id_list']])
    url = "http://YMAC-DC3-APP1:8080/fmedatastreaming/YMAC Data delivery/postgisdjangoaction.fmw?" \
          "FEATURE_TYPES={db_table}&id_list=({id_list})&DestDataset_GENERIC=%5C%5Cymac-dc3-app1%5Cspatial_wkg%5CFME_OUTPUT%5C{outfile}.shz&" \
          "GENERIC_OUT_FORMAT_GENERIC=ESRISHAPE".format(id_list=ids,
                                                        db_table=response_dict['db_table'],
                                                        outfile=response_dict['db_table'])
    h = HttpResponseRedirect(url)
    h['token'] = "782b77ba48c390cf8f74f9184a4398a8423d9efa"
    return h


@admin.register(HeritageSurvey)
class HeritageSurveyAdmin(admin.GeoModelAdmin):
    fields = (
        'survey_trip',
        'project_name',
        'project_status',
        'survey_type',
        'survey_methodologies',
        'survey_group',
        'proponent',
        'sampling_meth',
        'sampling_conf',
        'survey_region',
        'survey_description',
        'survey_note',
        'created_by',
        'date_create',
        'mod_by',
        'date_mod',
        'data_qa',
        'data_status',
        'geom',
    )
    inlines = [
        HeritageSurveyConsultantInline,
        HeritageSurveyProponentInline,
        HeritageSurveyCleaningInline
    ]
    actions = [
        get_surveyids,
        export_as_json,
        export_as_shz
    ]

    def survey(self, obj):
        if obj.survey_trip:
            return obj.survey_trip.survey_id
        return ''

    survey.admin_order_field = 'survey_trip'
    survey.short_description = 'Survey Trip'

    def datapath(self, obj):
        if obj.data_source.values():
            return "\n".join([ds.data_path for ds in obj.data_source.all() if ds.data_path])
        return ''

    def datastatus(self, obj):
        if obj.data_status:
            return obj.data_status.status
        return ''

    def propname(self, obj):
        if obj.proponent:
            return obj.proponent.name
        return ''

    def groupname(self, obj):
        if obj.survey_group:
            return obj.survey_group.group_name
        return ''

    list_display = [
        'survey',
        'datastatus',
        'propname',
        'groupname',
        'survey_type',
        'sampling_meth',
        'date_create',
        'created_by',
        'data_qa',
        'datapath'
    ]
    search_fields = [
        'survey_group__group_name',
        'survey_group__group_id',
    ]
    list_filter = [
        'survey_group__group_name',
        'survey_type',
        # HasGeomFilter
    ]


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
    SurveyGroup
]

for gm in geom_models:
    admin.site.register(gm, YMACModelAdmin)
