"""
from django.core.mail import send_mail

if form.is_valid():
    subject = form.cleaned_data['subject']
    message = form.cleaned_data['message']
    sender = form.cleaned_data['sender']
    cc_myself = form.cleaned_data['cc_myself']

    recipients = ['info@example.com']
    if cc_myself:
        recipients.append(sender)

    send_mail(subject, message, sender, recipients)
    return HttpResponseRedirect('/thanks/')
"""

import json
from datetime import date
from datetime import timedelta
from django.contrib import messages
from django.contrib.gis.db.models import Union
from django.core.serializers import serialize
from django.db.models import Q
from django.http import *
from django.shortcuts import render, redirect
from django.template import Context
from django.views.generic import DetailView, TemplateView
from django.views.generic import View
from django.views.generic.edit import FormView

from ymac_db.utils import emit_week
from .forms import *
from .models import HeritageSurvey, YMACRequestFiles

try:
    from urllib.parse import quote_plus, urlencode
except:
    from urllib import quote_plus, urlencode

TOKEN = "91e61ba3c8b7101ddf7a6ee8a0ddc935acd77089"
SERVER_URL = "ymac-dc3-app1:8080"
REPO = 'Data Download'
WORKSPACE = 'region_distance_calculator.fmw'


def index(request):
    today = date.today()
    return render(request, 'base.html', context={
        'all_requests': YMACSpatialRequest.objects.filter(done=False),
        })


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def software(request):
    return render(request, 'software.html')


def workbenches(request):
    return render(request, 'workbenches.html')


def spatial_thanks(request):
    return render(request, 'spatial_thanks.html', )


def data_download(request):
    return render(request, 'data_download.html')


def claims(request):
    return render(request, 'claim_overview.html', context={'claim_groups': YmacClaim.objects.filter(current=True)})


class YMACClaimView(DetailView):
    model = YmacClaim
    # Create template
    # We will need a filter for current
    queryset = YmacClaim.objects.filter(current=True)
    template_name = 'ymacclaim_detail.html'

    def get_context_data(self, **kwargs):
        context = super(YMACClaimView, self).get_context_data(**kwargs)
        context['daa_sites'] = serialize('geojson',
                                         DaaSite.objects.filter(geom__intersects=self.object.geom),
                                         geometry_field='geom', fields=('place_id',
                                                                        'name'))
        context['map_data'] = serialize('geojson', YmacClaim.objects.filter(pk=self.object.id), geometry_field='geom')
        # Site History
        # Surveys
        # Old Boundaries
        return context


class EmitsWeekView(TemplateView):
    template_name = 'emits_report.html'

    def get_context_data(self, **kwargs):
        context = super(EmitsWeekView, self).get_context_data(**kwargs)
        start_date, end_date = emit_week(date.today())
        context["heading"] = "From {} to the {}".format(start_date, end_date)
        tenements = YmacEmitTenements.objects.filter(Q(ymac_region=True, datereceived__range=(start_date, end_date)) |
                                                     Q(row_to_check=True, datereceived__range=(start_date, end_date)))
        context['emits'] = json.dumps([{'title': t.title,
                                        'datereceived' : t.datereceived.strftime("%d/%m/%Y"),
                                        'objectiondate': t.objectiondate,
                                        'applicants': t.applicants,
                                        'row_to_check': t.row_to_check,
                                        'claimgroup': ",".join(t.claimgroup)} for t in tenements])
        context['tenements'] = serialize('geojson', tenements,
                                         geometry_field='geom',
                                         fields=('title',
                                                 'pk',
                                                 'datereceived',
                                                 'objectiondate',
                                                 'applicants',
                                                 'row_to_check',
                                                 'claimgroup',))
        context['claims'] = serialize('geojson',
                                      YmacClaim.objects.filter(current=True),
                                      geometry_field='geom',
                                      fields=('name',))
        context['determinations'] = serialize('geojson',
                                              NnttDetermination.objects.filter(
                                                  Q(name__contains="Martu") |
                                                  Q(name__contains="Badimia")).filter(
                                                  geom__intersects=tenements.aggregate(Union('geom'))['geom__union']),
                                              geometry_field='geom',
                                              fields=('name',)
                                              )
        return context


class RegionDistanceView(FormView):
    """
    This should possibly be using Ajax to send Json back to table.
    """
    template_name = 'region_distances.html'
    form_class = RegionDistanceForm
    success_url = '/test/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        data = form.cleaned_data
        outputs = [
            ('ESRISHAPE', 'Shapefile'),
            ('XLSXW', 'Excel'),
            ('OGCKML', 'Google Earth'),
        ]
        dl_buttons = []
        data['token'] = TOKEN
        for output, name in outputs:
            dl_type = 'fmedatastreaming' if output == 'ESRISHAPE' else 'fmedatadownload'
            button = ("http://{}/{}/{}/{}?{}&Output={}".format(SERVER_URL, dl_type,
                                                               quote_plus(REPO),
                                                               quote_plus(WORKSPACE),
                                                               urlencode(data),
                                                               output), name)
            dl_buttons.append(button)
        data['Output'] = 'JSON'
        if data:
            fme_json = requests.get("http://{}/fmedatastreaming/{}/{}".format(SERVER_URL,
                                                                              quote_plus(REPO),
                                                                              quote_plus(WORKSPACE),
                                                                              ),
                                    params=data
                                    )

            # Couldn't find address
            print(fme_json.status_code)
            if (fme_json.status_code == 422):

                if data['origin'].lower() == 'groningen' or \
                                data['destination'].lower() == 'groningen':
                    messages.error(self.request, "Groningen is a stupid place.")
                else:
                    messages.error(self.request,
                                   "Couldn't find directions from {} to {}. Speak to Cam".format(data['origin'],
                                                                                                 data['destination']))
                return redirect('/workbenches/region_distance/', context={'errormsg': True})
            table_json = fme_json.json()
            print(table_json)
            for ft in table_json:
                if "cent_lat" in ft:
                    result_json = ft
                elif "region" in ft:
                    if ft["region"] == "outer":
                        outer = ft
                    else:
                        inner = ft
                else:
                    region = ft

            return render(self.request, 'dyna_table.html', context={'innerPolyLine':
                                                                        json.dumps([dict(zip(["lng",
                                                                                              "lat"], coords)) for
                                                                                    coords in inner['json_geometry'][
                                                                                        "coordinates"]]),
                                                                    'outterPolyLine':
                                                                        json.dumps([dict(zip(["lng",
                                                                                              "lat"], coords)) for
                                                                                    coords in
                                                                                    outer['json_geometry'][
                                                                                        "coordinates"]]),
                                                                    'regionPolyLine':
                                                                        json.dumps([dict(zip(["lng",
                                                                                              "lat"], coords)) for
                                                                                    coords in
                                                                                    region['json_geometry'][
                                                                                        "coordinates"]]),
                                                                    'centre': json.dumps(
                                                                        {"lng": float(result_json['cent_lat']),
                                                                         "lat": float(result_json['cent_long'])}),
                                                                    'results': result_json,
                                                                    'buttons': dl_buttons})


            # See what happens when we reply wiht JsonResponse
        return super(RegionDistanceView, self).form_valid(form)


def get_site(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SiteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SiteForm()

    return render(request, 'site_form.html', {'form': form})


class SurveyView(View):
    """
    Pass Survey id to filter request
    """

    def get(self, request):
        template = "surveys_map.html"
        modelname = "SurveyView"
        surveys = HeritageSurvey.objects.all()
        # for hs in surveys:
        #    if hs.geom:
        #        hs.geom.transform(4326)
        serialized = serialize('geojson', surveys,
                               geometry_field='geom',
                               fields=('survey_id',
                                       'survey_description',
                                       )
                               )
        return render(request, template, Context({'qs_results': serialized}))


class SpatialRequestView(FormView):
    template_name = 'spatial_request.html'
    form_class = YMACSpatialRequestForm
    success_url = '/spatial_thanks/'

    # def get_initial(self):
    #    return {
    #        'request_datetime': datetime.datetime.now()
    #    }

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('sup_data_file')
        print("Updating files %s" % files)
        form.uploaded_files = []
        if form.is_valid():
            print("Saving files %s")
            data = form.save()
            for f in files:
                yrf = YMACRequestFiles.objects.create(request=data, file=f)
                form.uploaded_files.append(yrf)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.generate_folders()
        form.update_smartsheet()
        form.send_email()
        # form.instance.user.name = self.request.name
        # form.instance.required_by = self.request.req_by
        return render(self.request, 'spatial_thanks.html',
                      context={'rq': form.instance.user,
                               'required_by': form.instance.required_by,
                               'job_control': form.instance.job_control}
                      )


def filter_map(request):
    """
    Simple Server side filter for map data
    :param request:
    :return:
    """
    return HttpResponse()


def convert_shz(request):
    """
    Drag and drop shapefile onto our OpenLayers Map.
    Need to allow users to select fields.
    :param request:
    :return: Return response with serialized geojson of file.
    """
    return HttpResponse()


class HeritageSurveyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #    return HeritageSurvey.objects.none()

        qs = HeritageSurvey.objects.all()

        if self.q:
            qs = qs.filter(survey_id__istartswith=self.q)

        return qs

class DAASiteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #    return HeritageSurvey.objects.none()

        qs = DaaSite.objects.all()

        if self.q:
            qs = qs.filter(Q(place_id__istartswith=self.q)|Q(name__istartswith=self.q))

        return qs

class HeritageSurveyTripAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #    return HeritageSurvey.objects.none()

        qs = HeritageSurvey.objects.all()

        if self.q:
            qs = qs.filter(survey_id__istartswith=self.q)

        return qs


class ProponentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #    return Proponent.objects.none()

        qs = Proponent.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class ProponentCodesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #    return SurveyProponentCode.objects.none()

        qs = SurveyProponentCode.objects.all()

        if self.q:
            qs = qs.filter(proponent_code__istartswith=self.q)

        return qs


class ConsultantAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #    return Consultant.objects.none()

        qs = Consultant.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CaptureOrgAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #   return CaptureOrg.objects.none()

        qs = CaptureOrg.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SurveyDocumentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return SurveyDocument.objects.none()

        qs = SurveyDocument.objects.all()

        if self.q:
            qs = qs.filter(filename__istartswith=self.q)

        return qs


class RequestUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # Don't worry about this
        # if not self.request.user.is_authenticated():
        #    return RequestUser.objects.none()

        qs = RequestUser.objects.filter(current_user=True)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class RequestJobAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # Don't worry about this
        # if not self.request.user.is_authenticated():
        #    return RequestUser.objects.none()

        qs = YMACSpatialRequest.objects.all()

        if self.q:
            qs = qs.filter(Q(job_control__icontains=self.q)|
                           Q(job_desc__icontains=self.q) |
                           Q(user__name__icontains=self.q)).exclude(job_control="").order_by('-job_control')

        return qs

class RequestUserAllAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # Don't worry about this
        # if not self.request.user.is_authenticated():
        #    return RequestUser.objects.none()

        qs = RequestUser.objects.all()

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))

        return qs