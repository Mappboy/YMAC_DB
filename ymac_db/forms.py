from django.contrib.gis import forms
from django import forms as baseform
from dal import autocomplete
from .models import *
from leaflet.forms.widgets import LeafletWidget
from datetimewidget.widgets import DateWidget


# ADD Site Document Inline
# Seee https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-manyto-many-models

class SiteForm(baseform.ModelForm):

    class Meta:
        model = Site
        exclude = []
        widgets = {'geom': LeafletWidget()}


class SurveyDocumentForm(baseform.ModelForm):
    class Meta:
        model = SurveyDocument
        exclude = []
        widgets = {'surveys': autocomplete.ModelSelect2Multiple(url='heritagesurvey-autocomplete')}


class HeritageSurveyInlineForm(baseform.ModelForm):
    class Meta:
        model = HeritageSurvey
        fields = []

class HeritageSiteForm(baseform.ModelForm):
    site_description = forms.ModelMultipleChoiceField(queryset=SiteDescriptions.objects.all())

    class Meta:
        model = HeritageSite
        exclude = []


class YMACSpatialRequestForm(baseform.ModelForm):
    user = baseform.ModelChoiceField(RequestUser.objects.all(), label="Name:")
    required_by = baseform.DateField(label="Required by:", widget=DateWidget(options={
        'format': 'dd-mm-yyyy',
        'autoclose': True,
        'showMeridian': True,
        # 'todayBtn': True,
        'startDate': '-1d'
    }, bootstrap_version=3))
    claim = baseform.ModelMultipleChoiceField(YmacClaim.objects.all(), label="Claims (if known)",
                                              widget=forms.SelectMultiple(attrs={'size': 10}))

    def send_email(self):
        pass

    def update_smartsheet(self):
        pass

    class Meta:
        model = YMACSpatialRequest
        fields = '__all__'


class RegionDistanceForm(baseform.Form):
    """
    Model for our region distances
    """
    origin = baseform.CharField(label="Start Point")
    destination = baseform.CharField(label="Destination")
    region = baseform.ChoiceField(label="Region", choices=[('Pilbara', 'Pilbara'),
                                                      ('Geraldton', 'Geraldton')])
    petrol_cost = baseform.FloatField(required=False)
