from django.contrib.gis import forms
from django import forms as baseform
from .models import *
from leaflet.forms.widgets import LeafletWidget


# ADD Site Document Inline
# Seee https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-manyto-many-models

class SiteForm(baseform.ModelForm):

    class Meta:
        model = Site
        exclude = []
        widgets = {'geom': LeafletWidget()}


class HeritageSiteForm(baseform.ModelForm):
    site_description = forms.ModelMultipleChoiceField(queryset=SiteDescriptions.objects.all())

    class Meta:
        model = HeritageSite
        exclude = []
