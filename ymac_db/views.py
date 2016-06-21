from django.views.generic import View
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
