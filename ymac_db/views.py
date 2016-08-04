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

from django.views.generic import View
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.template import Context
from django.contrib import messages
from django.core.serializers import serialize
from dal import autocomplete
from django.http import *
from .forms import *
from .models import HeritageSurvey, YMACRequestFiles
import requests
import json
import datetime

try:
    from urllib.parse import quote_plus, urlencode
except:
    from urllib import quote_plus, urlencode

TOKEN = "91e61ba3c8b7101ddf7a6ee8a0ddc935acd77089"
SERVER_URL = "ymac-dc3-app1:8080"
REPO = 'Data Download'
WORKSPACE = 'nats_halfwaycalcs.fmw'

def index(request):
    return render(request, 'base.html')


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
            button = ("http://{}/fmedatadownload/{}/{}?{}&Output={}".format(SERVER_URL,
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
            for ft in table_json:
                del ft['json_featuretype']
                del ft['json_geometry']
                del ft['json_ogc_wkt_crs']
            return render(self.request, 'dyna_table.html', context={'data': table_json, 'buttons': dl_buttons})


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
        template = "ymac_openlayers.html"
        modelname = "SurveyView"
        surveys = HeritageSurvey.objects.all()
        for hs in surveys:
            hs.geom.transform(4326)
        serialized = serialize('geojson', surveys,
                               geometry_field='geom',
                               fields=('ymac_svy_name',))
        return render(request, template, Context({'serialized': serialized,
                                                  'modelname': modelname}))


class SpatialRequestView(FormView):
    template_name = 'spatial_request.html'
    form_class = YMACSpatialRequestForm
    success_url = '/spatial_thanks/'

    #def get_initial(self):
    #    return {
    #        'request_datetime': datetime.datetime.now()
    #    }

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('sup_data_file')
        print("Updating files %s" % files)
        uploaded_files = []
        print("Form is ", form)
        if form.is_valid():
            print("Saving files %s")
            data = form.save()
            for f in files:
                YMACRequestFiles.objects.create(request=data, file=f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.generate_folders()
        form.send_email()
        form.update_smartsheet()
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
        if not self.request.user.is_authenticated():
            return HeritageSurvey.objects.none()

        qs = HeritageSurvey.objects.all()

        if self.q:
            qs = qs.filter(survey_id__istartswith=self.q)

        return qs

class HeritageSurveyTripAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return HeritageSurvey.objects.none()

        qs = HeritageSurvey.objects.all()

        if self.q:
            qs = qs.filter(survey_id__istartswith=self.q)

        return qs


class ProponentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Proponent.objects.none()

        qs = Proponent.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class ProponentCodesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return SurveyProponentCode.objects.none()

        qs = SurveyProponentCode.objects.all()

        if self.q:
            qs = qs.filter(proponent_code__istartswith=self.q)

        return qs

class ConsultantAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Consultant.objects.none()

        qs = Consultant.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CaptureOrgAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return CaptureOrg.objects.none()

        qs = CaptureOrg.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SurveyDocumentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return SurveyDocument.objects.none()

        qs = SurveyDocument.objects.all()

        if self.q:
            qs = qs.filter(filename__istartswith=self.q)

        return qs

class RequestUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return RequestUser.objects.none()

        qs = RequestUser.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q, current_user=True)

        return qs