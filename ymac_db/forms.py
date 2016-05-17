from django.contrib.gis import forms
from models import *


# ADD Site Document Inline
# SEe https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-many-to-many-models

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        exclude = []


class HeritageSiteForm(forms.ModelForm):
    site_description = forms.ModelMultipleChoiceField(queryset=SiteDescriptions.objects.all())

    class Meta:
        model = HeritageSite
        exclude = []


class HeritageSurveyForm(forms.ModelForm):
    sampling_meth = forms.ModelMultipleChoiceField(queryset=SampleMethodology.objects.all())

    class Meta:
        model = HeritageSurvey
        exclude = []
