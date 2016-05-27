from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from django.template import Context
from django.core.serializers import serialize
from models import HeritageSurvey


def index(request):
    return HttpResponse("You have reached the YMAC Spatial Database Website")


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
