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
from django.shortcuts import render
from django.template import Context
from django.core.serializers import serialize
from django.http import *
from .forms import *
from .models import HeritageSurvey


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
    return render(request, 'spatial_thanks.html')


def data_download(request):
    return render(request, 'data_download.html')


class RegionDistanceView(FormView):
    """
    This should possibly be using Ajax to send Json back to table
    """
    template_name = 'region_distances.html'
    form_class = RegionDistanceForm
    success_url = '/test/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.display_table()
        return HttpResponse()

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

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        form.update_smartsheet()
        # form.instance.user.name = self.request.name
        # form.instance.required_by = self.request.req_by
        return super(SpatialRequestView, self).form_valid(form)

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
