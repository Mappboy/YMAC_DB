from django.contrib.gis import forms
from models import *


# ADD Site Document Inline
# Seee https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-manyto-many-models

class SiteForm(forms.ModelForm):
    geom = forms.OpenLayersWidget()

    class Meta:
        model = Site
        exclude = []


class HeritageSiteForm(forms.ModelForm):
    site_description = forms.ModelMultipleChoiceField(queryset=SiteDescriptions.objects.all())

    class Meta:
        model = HeritageSite
        exclude = []
