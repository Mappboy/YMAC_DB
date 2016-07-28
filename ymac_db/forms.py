from django.contrib.gis import forms
from django import forms as baseform
from dal import autocomplete
from .models import *
import os
from leaflet.forms.widgets import LeafletWidget
from datetimewidget.widgets import DateWidget
from suit.widgets import SuitDateWidget, AutosizedTextarea


# ADD Site Document Inline
# Increase Widget sizes for multiple2Select
# Seee https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-manyto-many-models

class SiteForm(baseform.ModelForm):

    class Meta:
        model = Site
        exclude = []
        widgets = {'geom': LeafletWidget()}


class SurveyDocumentForm(baseform.ModelForm):
    #def clean(self):
    #    cleaned_data = super(SurveyDocumentForm, self).clean()
    #    filepath = cleaned_data.get("filepath")
    #    filename = cleaned_data.get("filename")
    #    if not os.path.isfile(os.path.join(filepath, filename)):
    #        raise forms.ValidationError("Not a valid file, check path and file name are correct")

    class Meta:
        model = SurveyDocument
        fields = '__all__'
        widgets = {'filename': AutosizedTextarea(),
                    'filepath': AutosizedTextarea(),
                   'surveys': autocomplete.ModelSelect2Multiple(
                                                        url='heritagesurvey-autocomplete')}


class HeritageSurveyInlineForm(baseform.ModelForm):
    class Meta:
        model = SurveyDocument.surveys.through
        fields = '__all__'
        widgets = {'heritagesurveys': autocomplete.ModelSelect2Multiple(
                                                        url='heritagesurvey-autocomplete')}

class HeritageSiteForm(baseform.ModelForm):
    site_description = forms.ModelMultipleChoiceField(queryset=SiteDescriptions.objects.all())

    class Meta:
        model = HeritageSite
        exclude = []


class YMACSpatialRequestForm(baseform.ModelForm):
    required_by = baseform.DateField(label="Required by:", widget=DateWidget(options={
        'format': 'dd-mm-yyyy',
        'autoclose': True,
        'showMeridian': True,
        # 'todayBtn': True,
        'startDate': '-1d'
    }, bootstrap_version=3))
    claim = baseform.ModelMultipleChoiceField(YmacClaim.objects.all(), label="Claims (if known)",
                                              widget=forms.SelectMultiple(attrs={'size': 10}))

    def clean(self):
        cleaned_data = super(YMACSpatialRequestForm, self).clean()
        #filepath = cleaned_data.get("filepath")
        #filename = cleaned_data.get("filename")
        #if not os.path.isfile(os.path.join(filepath, filename)):
        #    raise forms.ValidationError("Not a valid file, check path and file name are correct")

    def send_email(self):
        """
        This function will send the usual email to us spatial jobs guys.
        :return:
        """
        pass

    def update_smartsheet(self):
        """
        This will update smartsheet as we continue to use it.
        :return:
        """
        pass

    def generate_folders(self):
        """
        Initially we want to generate our id and create our folders on W: and copy
        any attached files into the directory. This is flipping sweet.
        :return:
        """
        pass

    class Meta:
        model = YMACSpatialRequest
        exclude = ['map',
                   'data',
                   'analysis',
                   'other',
                   'draft',
                   'done',
                   'assigned_to',
                   'time_spent',
                   'request_datetime',
                   'completed_datetime',
                   'job_control']
        widgets = {
            'user': autocomplete.ModelSelect2(url='requestuser-autocomplete'),
            'cc_recipients': autocomplete.ModelSelect2Multiple(url='requestuser-autocomplete'),
            'proponent': autocomplete.ModelSelect2(url='proponent-autocomplete'),
        }

class RegionDistanceForm(baseform.Form):
    """
    Model for our region distances
    """
    origin = baseform.CharField(label="Start Point")
    destination = baseform.CharField(label="Destination")
    region = baseform.ChoiceField(label="Region", choices=[('Pilbara', 'Pilbara'),
                                                      ('Geraldton', 'Geraldton')])
    petrol_cost = baseform.FloatField(required=False)


class HeritageSurveyForm(baseform.ModelForm):
    """
    TODO:   - Add SuitDateWidget
            - LinkedSelect
            - Use ModelSelect2Multiple
    """
    class Meta:
        model = HeritageSurvey
        fields = '__all__'
        widgets = {
            'proponent': autocomplete.ModelSelect2(url='proponent-autocomplete'),
            'date_create': SuitDateWidget(),
            'date_mod': SuitDateWidget(),
            'date_from': SuitDateWidget(),
            'date_to': SuitDateWidget(),
            'trip_number': baseform.NumberInput(),
            'consultants': autocomplete.ModelSelect2Multiple(url='consultant-autocomplete', attrs={'class': 'wide'}),
            'documents': autocomplete.ModelSelect2Multiple(url='surveydocument-autocomplete'),
            'proponent_codes': autocomplete.ModelSelect2Multiple(url='proponentcodes-autocomplete'),
        }


class HeritageSurveyTripForm(baseform.ModelForm):
    """
    TODO:   - Add SuitDateWidget
            - LinkedSelect
            - Use ModelSelect2Multiple
    """

    class Meta:
        model = HeritageSurveyTrip
        fields = '__all__'
        widgets = {
        }


class SurveyTripCleaningForm(baseform.ModelForm):
    class Meta:
        model = SurveyTripCleaning
        fields = '__all__'
        widgets = {
            'survey_trip': autocomplete.ModelSelect2(url='surveytrip-autocomplete'),
        }


class ConsultantForm(baseform.ModelForm):
    class Meta:
        model = Consultant
        fields = '__all__'
        widgets = {
            'company': autocomplete.ModelSelect2(url='captureorg-autocomplete'),
        }
