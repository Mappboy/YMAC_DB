# Register your models here.
# Change lat long and layer models for these geo models
# MAke sure they are converted to 4283
# Set List display
# Create our own map template
from __future__ import unicode_literals

from django.contrib import admin as baseadmin
from django.contrib import messages
from django.contrib.admin.helpers import ActionForm
from django.contrib.gis import admin
from django.contrib.gis import forms as geoforms
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from leaflet.admin import LeafletGeoAdmin
from jet.admin import CompactInline
from .validators import valid_surveyid
from .forms import *


def custom_titled_filter(title):
    class Wrapper(baseadmin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = baseadmin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class HasGeomFilter(baseadmin.SimpleListFilter):
    title = _('Geometry Exists')

    parameter_name = 'has_geom'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('False', _('Exists')),
            ('True', _('No Geometry')),
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
        elif self.value() == 'False':
            return queryset.filter(geom__isnull=False)
        else:
            return queryset.filter(geom__isnull=True)


class HasSpatialDataFilter(baseadmin.SimpleListFilter):
    title = _('Spatial Data Exists')

    parameter_name = 'has_sdexists'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('True', _('Exists')),
            ('False', _('No Spatial Data')),
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
        elif self.value() == 'False':
            return queryset.filter(spatial_data_exists=False)
        else:
            return queryset.filter(spatial_data_exists=True)


class IsDoneFilter(baseadmin.SimpleListFilter):
    title = _('Job Completed')

    parameter_name = 'is_done'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('True', _('Completed')),
            ('False', _('Ongoing')),
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
        elif self.value() == 'False':
            return queryset.filter(done=False)
        else:
            return queryset.filter(done=True)


class HasReportFilter(baseadmin.SimpleListFilter):
    title = _('Linked Report')

    parameter_name = 'has_report'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('False', _('Linked')),
            ('True', _('No Report')),
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
        elif self.value() == 'False':
            return queryset.filter(documents__isnull=False)
        else:
            return queryset.exclude(documents__isnull=False)


class HasFolderLocationFilter(baseadmin.SimpleListFilter):
    title = _('Folder Location')

    parameter_name = 'has_folder_loc'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('True', _('Located')),
            ('False', _('No Location')),
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
        elif self.value() == 'True':
            return queryset.exclude(folder_location='')
        else:
            return queryset.filter(Q(folder_location__isnull=True) | Q(folder_location=''))


class HasLinkedSurveyFilter(baseadmin.SimpleListFilter):
    title = _('Linked Survey')

    parameter_name = 'has_survey'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('False', _('Linked')),
            ('True', _('No Survey')),
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
        elif self.value() == 'False':
            return queryset.filter(surveys__isnull=False)
        else:
            return queryset.filter(surveys__isnull=True)


class ClaimDataPathFilter(baseadmin.SimpleListFilter):
    title = _('Potential Claim')

    parameter_name = 'data_path'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('AMA', _('Amangu')),
            ('BAD', _('Badimia')),
            ('BAN', _('Banjima')),
            ('BUD', _('Budina')),
            ('GNU', _('Gnulli')),
            ('HUT', _('Hutt River')),
            ('JUR', _('Jurruru')),
            ('K&M', _('Kuruma Marthadunera')),
            ('KAR', _('Kariyarra')),
            ('MAL', _('Malgana')),
            ('NAA', _('Naaguja')),
            ('NAN', _('Nanda')),
            ('NGA', _('Ngarluma')),
            ('NJA', _('Njamal')),
            ('NLW', _('Ngarlawangga')),
            ('NRL', _('Ngarla')),
            ('NYA', _('Nyangumarta')),
            ('NYI', _('Nyiyaparli')),
            ('PAL', _('Palyku')),
            ('PKK', _('Puutu Kunti Kurrama and Pinikura')),
            ('THU', _('Thudgari')),
            ('WJY', _('Wajarri Yamatji')),
            ('YHW', _('Yinhawangka')),
            ('YIN', _('Yindjibarndi')),
            ('YUG', _('Yugunga-Nya')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(data_path__contains=self.value())
        return queryset


class DocumentTypeFilter(baseadmin.SimpleListFilter):
    title = _('Document Type')

    parameter_name = 'document_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Image', 'Image'),
            ('Audio', 'Audio'),
            ('Video', 'Video'),
            ('Document', 'Document'),
            ('Spatial', 'Spatial'),
            ('Map', 'Map'),
            ('Other', 'Other')
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            queryset = queryset.filter(document_type__document_type=self.value())
        return queryset


class RelatedTripClaimFilter(baseadmin.SimpleListFilter):
    title = _('Related Claim')

    parameter_name = 'related_claim'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('AMA', _('Amangu')),
            ('BAD', _('Badimia')),
            ('BAN', _('Banjima')),
            ('BUD', _('Budina')),
            ('GNU', _('Gnulli')),
            ('HUT', _('Hutt River')),
            ('JUR', _('Jurruru')),
            ('K&M', _('Kuruma Marthadunera')),
            ('KAR', _('Kariyarra')),
            ('MAL', _('Malgana')),
            ('NAA', _('Naaguja')),
            ('NAN', _('Nanda')),
            ('NGA', _('Ngarluma')),
            ('NJA', _('Njamal')),
            ('NLW', _('Ngarlawangga')),
            ('NRL', _('Ngarla')),
            ('NYA', _('Nyangumarta')),
            ('NYI', _('Nyiyaparli')),
            ('PAL', _('Palyku')),
            ('PKK', _('Puutu Kunti Kurrama and Pinikura')),
            ('THU', _('Thudgari')),
            ('WJY', _('Wajarri Yamatji')),
            ('YHW', _('Yinhawangka')),
            ('YIN', _('Yindjibarndi')),
            ('YUG', _('Yugunga-Nya')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(survey_trip__survey_group__group_id=self.value())
        return queryset


class RelatedClaimFilter(baseadmin.SimpleListFilter):
    title = _('Related Claim')

    parameter_name = 'heritagesurvey__survey_group_group_id'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('AMA', _('Amangu')),
            ('BAD', _('Badimia')),
            ('BAN', _('Banjima')),
            ('BUD', _('Budina')),
            ('GNU', _('Gnulli')),
            ('HUT', _('Hutt River')),
            ('JUR', _('Jurruru')),
            ('K&M', _('Kuruma Marthadunera')),
            ('KAR', _('Kariyarra')),
            ('MAL', _('Malgana')),
            ('NAA', _('Naaguja')),
            ('NAN', _('Nanda')),
            ('NGA', _('Ngarluma')),
            ('NJA', _('Njamal')),
            ('NLW', _('Ngarlawangga')),
            ('NRL', _('Ngarla')),
            ('NYA', _('Nyangumarta')),
            ('NYI', _('Nyiyaparli')),
            ('PAL', _('Palyku')),
            ('PKK', _('Puutu Kunti Kurrama and Pinikura')),
            ('THU', _('Thudgari')),
            ('WJY', _('Wajarri Yamatji')),
            ('YHW', _('Yinhawangka')),
            ('YIN', _('Yindjibarndi')),
            ('YUG', _('Yugunga-Nya')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(surveys__survey_group__group_id=self.value())
        return queryset


class RelatedDocClaimFilter(baseadmin.SimpleListFilter):
    title = _('Related Claim')

    parameter_name = 'heritagesurvey__survey_group_group_id'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('AMA', _('Amangu')),
            ('BAD', _('Badimia')),
            ('BAN', _('Banjima')),
            ('BUD', _('Budina')),
            ('GNU', _('Gnulli')),
            ('HUT', _('Hutt River')),
            ('JUR', _('Jurruru')),
            ('K&M', _('Kuruma Marthadunera')),
            ('KAR', _('Kariyarra')),
            ('MAL', _('Malgana')),
            ('NAA', _('Naaguja')),
            ('NAN', _('Nanda')),
            ('NGA', _('Ngarluma')),
            ('NJA', _('Njamal')),
            ('NLW', _('Ngarlawangga')),
            ('NRL', _('Ngarla')),
            ('NYA', _('Nyangumarta')),
            ('NYI', _('Nyiyaparli')),
            ('PAL', _('Palyku')),
            ('PKK', _('Puutu Kunti Kurrama and Pinikura')),
            ('THU', _('Thudgari')),
            ('WJY', _('Wajarri Yamatji')),
            ('YHW', _('Yinhawangka')),
            ('YIN', _('Yindjibarndi')),
            ('YUG', _('Yugunga-Nya')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(surveys__survey_group__group_id=self.value())
        return queryset


class CorrectlyFiledFilter(baseadmin.SimpleListFilter):
    title = _('Correct Filing')

    parameter_name = 'correct_File'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (r"Z:\\?Claim Groups\\\w+\\Heritage Surveys\\\d{4}", _('Correct')),
            (r".*\\0. Old Folder Structure\\.*", _('Old file')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(data_path__regex=self.value())
        return queryset


class NoDataPathfilterFilter(baseadmin.SimpleListFilter):
    title = _('Data Path')

    parameter_name = 'data_path_null'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (True, _('is null')),
            (False, _('is not null')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(data_path__isnull=self.value())
        return queryset


class DriveFilter(baseadmin.SimpleListFilter):
    title = _('Drive Location')

    parameter_name = 'drive_location'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('G', _('General')),
            ('Q', _('Claims')),
            ('K', _('Research')),
            ('Z', _('Heritage')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(data_path__startswith=self.value())
        return queryset


class RelatedClaimContainsFilter(baseadmin.SimpleListFilter):
    title = _('Related Claim')

    parameter_name = 'survey_contains'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('AMA', _('Amangu')),
            ('BAD', _('Badimia')),
            ('BAN', _('Banjima')),
            ('BUD', _('Budina')),
            ('GNU', _('Gnulli')),
            ('HUT', _('Hutt River')),
            ('JUR', _('Jurruru')),
            ('K&M', _('Kuruma Marthadunera')),
            ('KAR', _('Kariyarra')),
            ('MAL', _('Malgana')),
            ('NAA', _('Naaguja')),
            ('NAN', _('Nanda')),
            ('NGA', _('Ngarluma')),
            ('NJA', _('Njamal')),
            ('NLW', _('Ngarlawangga')),
            ('NRL', _('Ngarla')),
            ('NYA', _('Nyangumarta')),
            ('NYI', _('Nyiyaparli')),
            ('PAL', _('Palyku')),
            ('PKK', _('Puutu Kunti Kurrama and Pinikura')),
            ('THU', _('Thudgari')),
            ('WJY', _('Wajarri Yamatji')),
            ('YHW', _('Yinhawangka')),
            ('YIN', _('Yindjibarndi')),
            ('YUG', _('Yugunga-Nya')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            queryset = queryset.filter(survey_id__startswith=self.value())
        return queryset


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


# ADD Site Document Inline
# SEe https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-many-to-many-models


@admin.register(Proponent)
class ProponentAdmin(baseadmin.ModelAdmin):
    search_fields = ['name']
    list_display = ['prop_id', 'name']


@admin.register(SiteType)
class SiteTypeAdmin(baseadmin.ModelAdmin):
    list_display = ['site_classification', 'site_category']
    list_editable = ['site_category']


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


class HeritageSurveyDocumentInline(admin.TabularInline):
    model = HeritageSurvey.documents.through
    form = HeritageDocumentInlineForm


class HeritageSurveyInline(CompactInline):
    model = SurveyDocument.surveys.through
    form = HeritageSurveyInlineForm


class HeritageSurveyCleaningInline(admin.TabularInline):
    max_num = 5
    model = HeritageSurvey.data_source.through


def move_to_surveydocs(modeladmin, request, queryset, linkfiles=True):
    """
    Function to move a SurveyCleaning Document to our cleaned Survey Document area
    TODO add a check if we do want to link or just move to surveyDocuments
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    conv_ext = {
        '.shp': 'Shapefile',
        '.shz': 'Shapefile',
        '.gpx': 'GPX',
        '.gdb': 'Geodatabase',
        '.tab': 'Mapinfo',
        '.kml': 'Google KML',
        '.kmz': 'Google KML',
    }
    for qs in queryset:
        # DocumentType.obejcts.get()
        doc_type = qs.path_type

        file_path, file_name = os.path.split(qs.data_path)
        file_ext = os.path.splitext(qs.data_path)[1]
        if doc_type == 'Prelim Advice':
            did = DocumentType.objects.get(id=2)
        elif doc_type == 'Survey Report':
            did = DocumentType.objects.get(id=1)
        elif doc_type == 'Photo':
            did = DocumentType.objects.get(id=8)
        elif doc_type == 'Spatial File':
            did = DocumentType.objects.filter(sub_type=conv_ext[file_ext])[0]
        else:
            # Just ignore directories
            pass
        sd, created = SurveyDocument.objects.get_or_create(document_type=did,
                                                           filepath=file_path,
                                                           filename=file_name)
        if modeladmin.model == SurveyCleaning:
            surveys = qs.heritagesurvey_set.all()
            if linkfiles:
                for survey in surveys:
                    survey.documents.add(sd)
            else:
                for survey in surveys:
                    survey.data_source.remove(qs)
            qs.delete()
            messages.success(request, "Created new document {} and added to surveys {}".format(sd, surveys))
        elif modeladmin.model == SurveyTripCleaning:
            deleted = 0
            surveys = None
            if linkfiles:
                surveys = qs.survey_trip
                surveys.documents.add(sd)
            surveytrips = SurveyTripCleaning.objects.filter(data_path=qs.data_path)
            for rel_trip_clean in surveytrips:
                rel_trip_clean.delete()
                deleted += 1
            if surveys:
                messages.success(request, "Created new document {}, added to survey"
                                          " {} and deleted {} Trip Cleanings".format(sd, surveys, deleted))
            else:
                messages.success(request, "Created new document {}"
                                          " and deleted {} Trip Cleanings".format(sd, deleted))


def move_to_survey_docs(modeladmin, request, queryset):
    move_to_surveydocs(modeladmin, request, queryset)


move_to_survey_docs.short_description = "Move to Survey Docs and Link"


def move_to_docs(modeladmin, request, queryset):
    move_to_surveydocs(modeladmin, request, queryset, False)


move_to_docs.short_description = "Move to Survey Docs"


def move_to_clean_up(modeladmin, request, queryset):
    """
    Move an object with a datapath to Clean up table. Which is a review table for deleting duplicate or bad items
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    for qs in queryset:
        FileCleanUp.objects.create(data_path=qs.data_path, submitted_user=request.user)
        qs.delete()


move_to_clean_up.short_description = "Move item to File Clean up"


class SetSurveyActionForm(ActionForm):
    heritage_survey = forms.ModelChoiceField(queryset=HeritageSurvey.objects.all(), required=False)


@admin.register(FileCleanUp)
class FileCleanUpAdmin(baseadmin.ModelAdmin):
    list_display = [
        'data_path',
        'submitted_user'
    ]


def url_to_docedit(self, request, queryset):
    doc_urls = r'<br/>'.join([format_html('<a href="{}">Edit {}</a>',
                                          reverse('admin:%s_%s_change' % (
                                              hs._meta.app_label, hs._meta.model_name),
                                                  args=[hs.id]),
                                          hs.__str__()) for qs in queryset for hs in
                              qs.survey.documents.all()])
    messages.info(request, format_html(doc_urls))


url_to_docedit.short_description = "Get Document Links"


def url_to_edit(self, request, queryset):
    # Use prefetch
    trip_urls = r'<br/>'.join([format_html('<a href="{}">Edit {}</a>',
                                           reverse('admin:%s_%s_change' % (
                                               qs.survey._meta.app_label, qs.survey._meta.model_name),
                                                   args=[qs.survey.id]),
                                           qs.survey.__str__()) for qs in queryset])
    messages.info(request, format_html(trip_urls))


url_to_edit.short_description = "Get Heritage Surveys Links"


@admin.register(YACReturn)
class YACReturnAdmin(baseadmin.ModelAdmin):
    list_display = [
        'survey',
        'pa',
        'report',
        'spatial'
    ]
    list_filter = [
        'pa',
        'report',
        'spatial']
    search_fields = [
        'survey__survey_id'
    ]
    actions = [url_to_docedit,
               url_to_edit]


@admin.register(SurveyCleaning)
class SurveyCleaningAdmin(baseadmin.ModelAdmin):
    def survey_list(self, obj):
        print(obj)
        try:
            return ";\n".join([smart_text(hs) for hs in obj.surveys.all()])
        except AttributeError:
            return ''

    survey_list.short_description = "Surveys"

    def url_to_edit(self, request, queryset):
        # Use prefetch
        trip_urls = r'<br/>'.join([format_html('<a href="{}">Edit {}</a>',
                                               reverse('admin:%s_%s_change' % (
                                                   hs._meta.app_label, hs._meta.model_name),
                                                       args=[hs.id]),
                                               hs.__unicode__()) for qs in queryset for hs in
                                   qs.surveys.all()])
        messages.info(request, format_html(trip_urls))

    url_to_edit.short_description = "Get Heritage Surveys Links"

    def show_data_pathurl(self, obj):

        return format_html(smart_text('<a href="file:///{}">{}</a>'),
                           obj.data_path,
                           obj.data_path)

    def startdate(self, obj):
        start_date = None
        for hs in obj.surveys.all():
            if not start_date:
                start_date = hs.date_from
            elif hs.date_from < start_date:
                start_date = hs.date_from
            else:
                continue
        return smart_text(start_date)

    startdate.short_description = "Start Date"

    def enddate(self, obj):
        end_date = None
        for hs in obj.surveys.all():
            if not end_date:
                end_date = hs.date_from
            elif hs.date_from > end_date:
                end_date = hs.date_from
            else:
                continue
        return smart_text(end_date)

    enddate.short_description = "End Date"

    fields = (
        'data_path',
        'path_type',
    )
    list_display = [
        'survey_list',
        'startdate',
        'enddate',
        'show_data_pathurl',
        'path_type',
    ]
    list_filter = [
        'path_type',
        DriveFilter,
        NoDataPathfilterFilter,
        CorrectlyFiledFilter,
        # TODO: fix this claim shiiiiiiit
        RelatedClaimFilter,
        ClaimDataPathFilter,
    ]
    inlines = [
    ]
    actions = [move_to_survey_docs,
               move_to_docs,
               url_to_edit,
               move_to_clean_up]
    search_fields = [
        'data_path',
        'surveys']


def set_as_done(modeladmin, request, queryset):
    """
    Set completed datetime too
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    import smartsheet
    num_requests = len(queryset)
    queryset.update(done=True)
    row_updates = []
    ss = smartsheet.Smartsheet("4104lxpew3jppnp3xvoeff7yp")
    for qs in queryset:
        qs.completed_datetime = datetime.datetime.now()
        try:
            search_result = ss.Search.search_sheet(3001821196248964, qs.job_control)
            row_to_update = ss.Sheets.get_row(3001821196248964, search_result.to_dict()['results'][0]['objectId'])
            # Done column = 8925425461159812
            # check columns = action = ss.Sheets.get_columns(3001821196248964, include_all=True)
            cell = row_to_update.get_column(8925425461159812)
            cell.value = qs.done
            row_to_update.set_column(cell.column_id, cell)
            row_updates.append(row_to_update)
        except:
            messages.info(request, "Couldn't update smartsheet")
    ss.Sheets.update_rows(3001821196248964, row_updates)
    messages.info(request, "Set {} requests to done".format(num_requests))


set_as_done.short_description = "Set Request Done"


@admin.register(YMACSpatialRequest)
class YMACSpatialRequestAdmin(YMACModelAdmin):
    list_display = ['user',
                    'request_type',
                    'map_size',
                    'job_control',
                    'job_desc',
                    'required_by',
                    'done']
    search_fields = ['user__name',
                     'job_control',
                     'job_desc']
    list_filter = [('user__department__name', custom_titled_filter("Department Name")),
                   'required_by',
                   'request_datetime',
                   IsDoneFilter]
    actions = [set_as_done]


@admin.register(SurveyDocument)
class SurveyDocumentAdmin(baseadmin.ModelAdmin):
    action_form = SetSurveyActionForm

    def hsurveys(self, obj):
        try:
            return ";\n".join([smart_text(hs) for hs in obj.surveys.all()])
        except AttributeError:
            return ''

    hsurveys.short_description = "Surveys"

    def show_data_pathurl(self, obj):
        full_path = os.path.join(obj.filepath, obj.filename)
        return format_html(smart_text('<a href="file:///{}">{}</a>'),
                           full_path,
                           full_path)

    show_data_pathurl.short_description = "File Location"

    def link_to_survey(self, request, queryset):
        """
        Function to move a SurveyCleaning Document to our cleaned Survey Document area
        :param modeladmin:
        :param request:
        :param queryset:
        :return:
        """
        for qs in queryset:
            survey = HeritageSurvey.objects.get(id=request.POST['heritage_survey'])
            qs.surveys.add(survey)
            messages.success(request, "Linked survey {} to document {}".format(survey, qs))

    link_to_survey.short_description = "Link to Survey"
    fields = (
        'document_type',
        'filepath',
        'filename',
        'file_status',
        # 'surveys'
    )
    list_display = [
        'hsurveys',
        'document_type',
        'show_data_pathurl',
        'file_status'
    ]
    list_filter = [
        DocumentTypeFilter,
        RelatedDocClaimFilter,
        HasLinkedSurveyFilter,
    ]
    list_display_links = ('hsurveys',
                          'document_type',
                          )
    inlines = [
        HeritageSurveyInline
    ]
    search_fields = [
        'surveys__survey_id',
        'filepath',
        'filename'
    ]
    actions = [link_to_survey]
    list_editable = ['file_status']
    form = SurveyDocumentForm


@admin.register(SurveyTripCleaning)
class SurveyTripCleaningAdmin(baseadmin.ModelAdmin):
    def show_data_pathurl(self, obj):
        return format_html(smart_text('<a href="file:///{}">{}</a>'),
                           obj.data_path,
                           obj.data_path)

    def startdate(self, obj):
        return smart_text(obj.survey_trip.date_from)

    startdate.short_description = "Start Date"

    def enddate(self, obj):
        return smart_text(obj.survey_trip.date_to)

    enddate.short_description = "End Date"

    fields = (
        'survey_trip',
        'data_path',
        'path_type',
    )
    list_display = [
        'survey_trip',
        'startdate',
        'enddate',
        'show_data_pathurl',
        'path_type',
    ]
    list_filter = [
        'path_type',
        CorrectlyFiledFilter,
        DriveFilter,
        RelatedTripClaimFilter,
        ClaimDataPathFilter,
    ]
    inlines = [
    ]

    def url_to_edit(self, request, queryset):
        trip_urls = r'<br/>'.join([format_html('<a href="{}">Edit {}</a>',
                                               reverse('admin:%s_%s_change' % (
                                                   qs._meta.app_label, qs.survey_trip._meta.model_name),
                                                       args=[qs.survey_trip_id]),
                                               qs.survey_trip.__unicode__()) for qs in queryset])
        messages.info(request, format_html(trip_urls))

    url_to_edit.short_description = "Get Survey Trip links"

    def url_to_hsedit(self, request, queryset):
        trip_urls = r'<br/>'.join([format_html('<a href="{}">Edit {}</a>',
                                               reverse('admin:%s_%s_change' % (
                                                   hs._meta.app_label, hs._meta.model_name),
                                                       args=[hs.id]),
                                               hs.__unicode__()) for qs in queryset for hs in
                                   qs.survey_trip.heritagesurvey_set.all()])
        messages.info(request, format_html(trip_urls))

    url_to_hsedit.short_description = "Get Heritage Surveys Links"

    actions = [move_to_survey_docs,
               move_to_docs,
               url_to_edit,
               url_to_hsedit,
               move_to_clean_up
               ]
    ordering = ('data_path', 'survey_trip',)
    search_fields = ['survey_trip__survey_id',
                     'data_path']
    form = SurveyTripCleaningForm


@admin.register(PotentialSurvey)
class PotentialSurveyAdmin(baseadmin.ModelAdmin):
    action_form = SetSurveyActionForm

    def show_data_pathurl(self, obj):
        return format_html('<a href="file:///{}">{}</a>',
                           obj.data_path,
                           obj.data_path)

    def url_to_edit(self, request, queryset):
        trip_urls = r'<br/>'.join([format_html('<a href="{}">Edit {}</a>',
                                               reverse('admin:%s_%s_change' % (
                                                   hs._meta.app_label, hs._meta.model_name),
                                                       args=[hs.id]),
                                               hs.__unicode__()) for qs in queryset for hs in
                                   HeritageSurvey.objects.filter(survey_trip__survey_id__contains=qs.survey_id)])
        messages.info(request, format_html(trip_urls))

    url_to_edit.short_description = "Get Potential Heritage Surveys Links"

    fields = (
        'survey_id',
        'data_path',
        'path_type',
    )
    list_display = [
        'survey_id',
        'show_data_pathurl',
        'path_type',
    ]
    list_filter = [
        'path_type',
        CorrectlyFiledFilter,
        RelatedClaimContainsFilter,
        ClaimDataPathFilter,
        # ('survey_trip', baseadmin.RelatedOnlyFieldListFilter)
    ]
    inlines = [
    ]
    actions = ['move_to_surveydocs',
               url_to_edit]
    ordering = ('data_path', 'survey_id',)

    def move_to_surveydocs(self, request, queryset):
        """
        Function to move a SurveyCleaning Document to our cleaned Survey Document area
        :param modeladmin:
        :param request:
        :param queryset:
        :return:
        """
        conv_ext = {
            '.shp': 'Shapefile',
            '.shz': 'Shapefile',
            '.gpx': 'GPX',
            '.gdb': 'Geodatabase',
            '.tab': 'Mapinfo',
            '.kml': 'Google KML',
            '.kmz': 'Google KML',
        }
        for qs in queryset:
            # DocumentType.obejcts.get()
            doc_type = qs.path_type

            file_path, file_name = os.path.split(qs.data_path)
            file_ext = os.path.splitext(qs.data_path)[1]
            if doc_type == 'Prelim Advice':
                did = DocumentType.objects.get(id=2)
            elif doc_type == 'Survey Report':
                did = DocumentType.objects.get(id=1)
            elif doc_type == 'Photo':
                did = DocumentType.objects.get(id=8)
            elif doc_type == 'Spatial File':
                did = DocumentType.objects.filter(sub_type=conv_ext[file_ext])[0]
            else:
                # Just ignore directories
                pass
            sd, created = SurveyDocument.objects.get_or_create(document_type=did,
                                                               filepath=file_path,
                                                               filename=file_name)
            survey = HeritageSurvey.objects.get(id=request.POST['heritage_survey'])
            survey.documents.add(sd)
            qs.delete()
            messages.success(request, "Created document {} and moved to survey {}".format(sd, survey))


class SiteAdmin(YMACModelAdmin):
    def get_queryset(self, request):
        my_model = super(SiteAdmin, self).get_queryset(request)
        my_model = my_model.prefetch_related('daa_sites')
        my_model = my_model.prefetch_related('surveys')
        return my_model

    inlines = [
    ]
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
    def type_list(self, obj):
        try:
            return ";\n".join([smart_text(hs.site_classification) for hs in obj.site_type.all()])
        except AttributeError:
            return ''

    type_list.short_description = "Site Classification"

    inlines = [
    ]
    list_display = [
        'type_list',
        'site_comments',
        'site_name'
    ]
    list_filter = [
        'site_location_desc',
        'site_comments',
        'site_name'
    ]

    search_fields = [
        'site_name',
    ]


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("geojson", queryset, stream=response)
    return response


def export_as_csv(modeladmin, request, queryset):
    import sys
    import csv, codecs
    class UnicodeWriter:
        """
        A CSV writer which will write rows to CSV file "f",
        which is encoded in the given encoding.
        """

        def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
            from cStringIO import StringIO
            # Redirect output to a queue
            self.queue = StringIO()
            self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
            self.stream = f
            self.encoder = codecs.getincrementalencoder(encoding)()

        def writerow(self, row):
            self.writer.writerow([s.encode("utf-8") for s in row])
            # Fetch UTF-8 output from the queue ...
            data = self.queue.getvalue()
            data = data.decode("utf-8")
            # ... and reencode it into the target encoding
            data = self.encoder.encode(data)
            # write to the target stream
            self.stream.write(data)
            # empty queue
            self.queue.truncate(0)

        def writerows(self, rows):
            for row in rows:
                self.writerow(row)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="heritage_surveys.csv"'
    if sys.version_info[0] == 2:
        writer = UnicodeWriter(response)
    else:
        writer = csv.writer(response)
    fields = (
        'survey_id',
        'date_from',
        'date_to',
        'trip_number',
        'project_name',
        'project_status',
        'survey_type',
        'survey_group',
        'sampling_meth',
        'sampling_conf',
        'survey_region',
        'survey_description',
        'survey_note',
        'proponent',
        'data_status',
         'consultants',
        'survey_methodology'
    )
    writer.writerow(fields)
    for qs in queryset:
        row = [getattr(qs, f) for f in fields if f not in ['survey_methodology','consultants']]
        if qs.consultants.all():
            row.append(";".join([ q.name for q in qs.consultants.all()]))
        else:
            row.append("")
        if qs.survey_methodologies.all():
            row.append(";".join([ q.survey_meth for q in qs.survey_methodologies.all()]))
        else:
            row.append("")
        writer.writerow(row)

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


def set_as_completed(modeladmin, request, queryset):
    for qs in queryset:
        qs.update(project_status="Completed")
    messages.info(request, "Set {} surveys to completed".format(len(queryset)))


set_as_completed.short_description = "Set to Completed"


class SetSurveyId(ActionForm):
    heritage_survey = forms.CharField(max_length=10, validators=[valid_surveyid], required=False)


@admin.register(HeritageSurvey)
class HeritageSurveyAdmin(YMACModelAdmin):
    action_form = SetSurveyId

    def show_data_pathurl(self, obj):
        return format_html('<a href="file:///{}">{}</a>',
                           obj.folder_location,
                           obj.folder_location)

    def clone_survey(self, request, queryset):
        """
        Function Clone a Survey and Set Survey Id = to new Survey Id
        :param modeladmin:
        :param request:
        :param queryset:
        :return:
        """
        if len(queryset) > 1:
            messages.error(request, "Can only clone one survey at a time".format())
        for qs in queryset:
            survey_id = request.POST['heritage_survey']
            obj, created = HeritageSurvey.objects.get_or_create(
                survey_id=survey_id,
                trip_number=qs.trip_number,
            )
            attrs = ["original_ymac_id",
                     "data_status",
                     "date_from",
                     "date_to",
                     "survey_type",
                     "survey_group",
                     "proponent",
                     "sampling_meth",
                     "sampling_conf",
                     "project_name",
                     "project_status",
                     "survey_region",
                     "survey_description",
                     "survey_note",
                     "created_by",
                     "date_create",
                     "mod_by",
                     "date_mod",
                     "data_qa",
                     "spatial_data_exists",
                     "folder_location",
                     "geom"]
            for attr in attrs:
                if not getattr(obj, attr):
                    setattr(obj, attr, getattr(qs, attr))
            obj.data_source.add(*[d.id for d in qs.data_source.all()])
            obj.survey_methodologies.add(*[s.id for s in qs.survey_methodologies.all()])
            obj.proponent_codes.add(*[p.id for p in qs.proponent_codes.all()])
            obj.consultants.add(*[c.id for c in qs.consultants.all()])
            related_code, created = RelatedSurveyCode.objects.get_or_create(rel_survey_id=qs.survey_id)
            obj.related_surveys.add(related_code)
            obj.documents.add(*[d.id for d in qs.documents.all()])
            messages.success(request, "Cloned survey {} to new Survey {}".format(qs, survey_id, ))

    clone_survey.short_description = "Clone Current Survey To New Id"

    show_data_pathurl.short_description = "Z: Location"
    fields = (
        'survey_id',
        'date_from',
        'date_to',
        'trip_number',
        'project_name',
        'project_status',
        'survey_type',
        'survey_methodologies',
        'survey_group',
        'sampling_meth',
        'sampling_conf',
        'survey_region',
        'survey_description',
        'survey_note',
        'proponent',
        'created_by',
        'date_create',
        'mod_by',
        'date_mod',
        'data_qa',
        'data_status',
        'folder_location',
        'documents',
        'consultants',
        'proponent_codes',
        'related_surveys',
        'geom',
    )
    actions = [
        export_as_json,
        export_as_shz,
        set_as_completed,
        clone_survey,
        export_as_csv
    ]
    search_fields = ['survey_id',
                     'survey_group__group_id',
                     'project_name',
                     'original_ymac_id']

    def documentpath(self, obj):
        if obj.documents.values():
            return format_html("<br>".join([format_html('<a href="file:///{}">{}</a>',
                                                        os.path.join(ds.filepath, ds.filename),
                                                        ds.filename) for ds
                                            in obj.documents.all() if ds.filepath]))
        return ''

    documentpath.short_description = "Linked Files"

    def show_document_pathurl(self, obj):
        return format_html('<a href="file:///{}">{}</a>',
                           obj.folder_location,
                           obj.folder_location)

    show_document_pathurl.short_description = "Folder Location"

    def datastatus(self, obj):
        if obj.data_status:
            return smart_text(obj.data_status.status)
        return ''

    datastatus.short_description = "Status"

    def propname(self, obj):

        if obj.proponent:
            return smart_text(obj.proponent.name)
        return ''

    propname.short_description = "Proponent"

    def groupname(self, obj):
        if obj.survey_group:
            return smart_text(obj.survey_group.group_name)
        return ''

    groupname.short_description = "Claim"

    list_display = [
        'survey_id',
        'trip_number',
        'date_from',
        'date_to',
        'project_status',
        'propname',
        'groupname',
        'project_name',
        'original_ymac_id',
        'survey_type',
        'spatial_data_exists',
        # 'sampling_meth',
        # 'datastatus',
        # 'data_qa',
        'show_document_pathurl',
        'documentpath',
    ]
    # list_editable = ['spatial_data_exists']

    list_filter = [
        'survey_group__group_name',
        'survey_type',
        'project_status',
        'date_create',
        'date_from',
        HasSpatialDataFilter,
        HasReportFilter,
        HasFolderLocationFilter,
    ]
    form = HeritageSurveyForm


@admin.register(DaaSite)
class DAASiteAdmin(YMACModelAdmin):
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


basemodels = [SiteUser,
              CaptureOrg,
              SiteDocument,
              SiteDescriptions,
              RestrictionStatus,
              SurveyMethodology,
              Consultant,
              RelatedSurveyCode,
              SurveyProponentCode,
              DocumentType,
              RequestUser,
              RequestType,
              Department,
              YmacStaff,
              ]

for m in basemodels:
    admin.site.register(m)

geom_models = [
    YmacRegion,
    Tenement,
    SurveyGroup,
]

for gm in geom_models:
    admin.site.register(gm, YMACModelAdmin)
