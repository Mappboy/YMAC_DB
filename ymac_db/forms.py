from django.contrib.gis import forms
from django import forms as baseform
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


class HeritageSiteForm(baseform.ModelForm):
    site_description = forms.ModelMultipleChoiceField(queryset=SiteDescriptions.objects.all())

    class Meta:
        model = HeritageSite
        exclude = []


class YMACSpatialRequestForm(baseform.ModelForm):
    user = forms.ModelChoiceField(RequestUser.objects.all(), label="Name:")
    required_by = forms.DateField(label="Required by:", widget=DateWidget(options={
        'format': 'dd-mm-yyyy',
        'autoclose': True,
        'showMeridian': True,
        # 'todayBtn': True,
        'startDate': '-1d'
    }, bootstrap_version=3))
    claim = forms.ModelMultipleChoiceField(YmacClaim.objects.all(), label="Claims (if known)",
                                           widget=forms.SelectMultiple(attrs={'size': 10}))

    def send_email(self):
        pass

    def update_smartsheet(self):
        pass

    class Meta:
        model = YMACSpatialRequest
        fields = '__all__'
