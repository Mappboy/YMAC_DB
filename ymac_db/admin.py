# Register your models here.
# Change lat long and layer models for these geo models
# MAke sure they are converted to 4283
# Set List display
# Create our own map template
from __future__ import unicode_literals

import os

from django.contrib import admin as baseadmin
from django.contrib import messages
from django.contrib.admin.helpers import ActionForm
from django.contrib.gis import admin
from django.contrib.gis import forms as geoforms
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from leaflet.admin import LeafletGeoAdmin

from .forms import *


class HasGeomFilter(baseadmin.SimpleListFilter):
    title = _('Spatial Data Exists')

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
            ('True', _('No Spatial Data')),
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
            return queryset.filter(geom__isnull=bool(self.value()))


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
            return queryset.filter(documents__isnull=True)


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
            queryset = queryset.filter(survey_trip__heritagesurvey__survey_group__group_id=self.value())
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
            queryset = queryset.filter(heritagesurvey__survey_group__group_id=self.value())
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
              DocumentType,
              ]

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


class HeritageSurveyDocumentInline(admin.TabularInline):
    model = HeritageSurvey.documents.through
    #form = SurveyDocumentForm


class HeritageSurveyInline(admin.TabularInline):
    model = HeritageSurvey
    #form = HeritageSurveyInlineForm

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
                surveys = qs.survey_trip.heritagesurvey_set.all()
                for survey in surveys:
                    survey.documents.add(sd)
            surveytrips = SurveyTripCleaning.objects.filter(data_path=qs.data_path)
            for rel_trip_clean in surveytrips:
                rel_trip_clean.delete()
                deleted += 1
            if surveys:
                messages.success(request, "Created new document {}, added to surveys"
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


@admin.register(FileCleanUp)
class FileCleanUpAdmin(baseadmin.ModelAdmin):
    list_display = [
        'data_path',
        'submitted_user'
    ]


@admin.register(SurveyCleaning)
class SurveyCleaningAdmin(baseadmin.ModelAdmin):
    def surveys(self, obj):
        # Todo use prefetch
        print(obj)
        try:
            return ";\n".join([smart_text(hs.survey_trip) for hs in obj.heritagesurvey_set.all()])
        except AttributeError:
            return ''

    surveys.short_description = "Surveys"

    def url_to_edit(self, request, queryset):
        # Use prefetch
        trip_urls = r'<br/>'.join([format_html('<a href="{}">Edit {}</a>',
                                               reverse('admin:%s_%s_change' % (
                                                   hs._meta.app_label, hs._meta.model_name),
                                                       args=[hs.id]),
                                               hs.__unicode__()) for qs in queryset for hs in
                                   qs.heritagesurvey_set.all()])
        messages.info(request, format_html(trip_urls))

    url_to_edit.short_description = "Get Heritage Surveys Links"

    def show_data_pathurl(self, obj):

        return format_html(smart_text('<a href="file:///{}">{}</a>'),
                           obj.data_path,
                           obj.data_path)

    def startdate(self, obj):
        start_date = None
        for hs in obj.heritagesurvey_set.all():
            if not start_date:
                start_date = hs.survey_trip.date_from
            elif hs.survey_trip.date_from < start_date:
                start_date = hs.survey_trip.date_from
            else:
                continue
        return smart_text(start_date)

    startdate.short_description = "Start Date"

    def enddate(self, obj):
        end_date = None
        for hs in obj.heritagesurvey_set.all():
            if not end_date:
                end_date = hs.survey_trip.date_from
            elif hs.survey_trip.date_from > end_date:
                end_date = hs.survey_trip.date_from
            else:
                continue
        return smart_text(end_date)

    enddate.short_description = "End Date"

    fields = (
        'data_path',
        'path_type',
    )
    list_display = [
        'surveys',
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
        'heritagesurvey__survey_trip__survey_id']


@admin.register(YMACSpatialRequest)
class YMACSpatialRequestAdmin(ImportExportModelAdmin):
    pass


@admin.register(SurveyDocument)
class SurveyDocumentAdmin(baseadmin.ModelAdmin):
    def surveys(self, obj):
        print(obj)
        try:
            return ";\n".join([smart_text(hs.survey_trip) for hs in obj.heritagesurvey_set.all()])
        except AttributeError:
            return ''

    surveys.short_description = "Surveys"

    def show_data_pathurl(self, obj):
        full_path = os.path.join(obj.filepath, obj.filename)
        return format_html(smart_text('<a href="file:///{}">{}</a>'),
                           full_path,
                           full_path)

    fields = (
        'document_type',
        'filepath',
        'filename',
    )
    list_display = [
        'surveys',
        'document_type',
        'show_data_pathurl',
    ]
    list_filter = [
        'document_type',
        RelatedClaimFilter,
    ]
    list_display_links = ('surveys',
                          'document_type',
                          )
    inlines = [
        #HeritageSurveyDocumentInline
    ]
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


class SetSurveyActionForm(ActionForm):
    heritage_survey = forms.ModelChoiceField(queryset=HeritageSurvey.objects.all(), required=False)


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


@admin.register(Site)
class SiteAdmin(YMACModelAdmin):
    def get_queryset(self, request):
        my_model = super(SiteAdmin, self).get_queryset(request)
        my_model = my_model.prefetch_related('daa_sites')
        my_model = my_model.prefetch_related('surveys')
        return my_model

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
class HeritageSurveyAdmin(YMACModelAdmin):
    HeritageSurvey.objects.prefetch_related('survey_group')
    HeritageSurvey.objects.prefetch_related('proponent')
    fields = (
        'survey_trip',
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
        'geom',
        'documents',
        'consultants',
        'proponent_codes',
    )
    inlines = [
        # HeritageSurveyConsultantInline,
        # HeritageSurveyProponentInline,
        # HeritageSurveyCleaningInline,
        # HeritageSurveyDocumentInline
    ]
    actions = [
        export_as_json,
        export_as_shz
    ]
    search_fields = ['survey_trip__survey_id',
                     'survey_group__group_id',
                     'project_name']

    def survey(self, obj):
        if obj.survey_trip:
            return obj.survey_trip.survey_id
        return ''

    survey.admin_order_field = 'survey_trip'
    survey.short_description = 'Survey Trip'

    def datapath(self, obj):
        if obj.data_source.values():
            return smart_text(";\n".join([ds.data_path for ds in obj.data_source.all() if ds.data_path]))
        return ''

    def tripnumber(self, obj):
        return smart_text(obj.survey_trip.trip_number)

    tripnumber.short_description = "Trip Number"

    def startdate(self, obj):
        return smart_text(obj.survey_trip.date_from)

    startdate.short_description = "Start Date"

    def enddate(self, obj):
        return smart_text(obj.survey_trip.date_to)

    enddate.short_description = "End Date"

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
        'survey',
        'tripnumber',
        'project_status',
        'propname',
        'groupname',
        'project_name',
        'survey_type',
        'sampling_meth',
        'date_create',
        'created_by',
        'datastatus',
        'data_qa',
        'folder_location',
        'startdate',
        'enddate',
        'datapath'
    ]

    list_filter = [
        'survey_group__group_name',
        'survey_type',
        'project_status',
        HasGeomFilter,
        HasReportFilter,
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
    SurveyGroup
]

for gm in geom_models:
    admin.site.register(gm, YMACModelAdmin)
