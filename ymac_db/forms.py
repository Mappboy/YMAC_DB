from django.contrib.gis import forms
from django import forms as baseform
from dal import autocomplete
from .models import *
import os
from leaflet.forms.widgets import LeafletWidget
from datetimewidget.widgets import DateWidget
from suit.widgets import SuitDateWidget, AutosizedTextarea
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ADD Site Document Inline
# Increase Widget sizes for multiple2Select
# Seee https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#working-with-manyto-many-models

class SiteForm(baseform.ModelForm):

    class Meta:
        model = Site
        exclude = []
        widgets = {'geom': LeafletWidget()}


class SurveyDocumentForm(baseform.ModelForm):
    def clean(self):
        cleaned_data = super(SurveyDocumentForm, self).clean()
        filepath = cleaned_data.get("filepath")
        filename = cleaned_data.get("filename")
        #if not os.path.isfile(os.path.join(filepath, filename)):
        #    raise forms.ValidationError("Not a valid file, check path and file name are correct")

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
        'format': 'dd/mm/yyyy',
        'autoclose': True,
        'showMeridian': True,
        # 'todayBtn': True,
        'startDate': '-1d'
    }, bootstrap_version=3))
    claim = baseform.ModelMultipleChoiceField(YmacClaim.objects.all(), label="Claims (if known)",
                                              widget=forms.SelectMultiple(attrs={'size': 10}))
    sup_data_file = baseform.FileField(label="Data files for upload",
                                       widget=forms.ClearableFileInput(attrs={'multiple': True}))
    #def clean_request_datetime(self):
    #    data = self.cleaned_data.get('request_datetime')
    #    data = datetime.datetime.now()
    #    return data

    def clean(self):
        cleaned_data = super(YMACSpatialRequestForm, self).clean()
        #filepath = cleaned_data.get("filepath")
        #filename = cleaned_data.get("filename")
        #if not os.path.isfile(os.path.join(filepath, filename)):
        #    raise forms.ValidationError("Not a valid file, check path and file name are correct")

    def clean_job_control(self):
        data = self.cleaned_data.get('job_control')
        data = self.generate_job_control()
        return data

    def send_email(self):
        """
        This function will send the usual email to us spatial jobs guys.
        :return:
        """
        msg = MIMEMultipart()
        msg['From'] = email if email else "spatialjobs@ymac.org.au"
        msg['To'] = COMMASPACE.join(toaddr)
        msg['Subject'] = "{map_type} {job_id} request".format(map_type=req_type, job_id=new_jobid)

        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP('ymac-org-au.mail.protection.outlook.com', 25)
        s.sendmail(email, toaddr, msg.as_string())
        s.quit()
        pass

    def update_smartsheet(self):
        """
        This will update smartsheet as we continue to use it.
        :return:
        """
        surl = "https://api.smartsheet.com/2.0/sheets/3001821196248964"

        # Get the top most row and pull out the job control cell and increment and create new id
        r = requests.get(url=surl, headers=headers)
        if r.status_code == 200:
            q = json.loads(r.text)
            jobid = [l for l in q['rows'][0]['cells'] if l.has_key('displayValue') and
                     'J201' in l['displayValue']][0]['value']
            jid = int(jobid.split("-")[1]) + 1
            new_jobid = "J" + time.strftime("%Y") + "-" + str(jid).zfill(3)

        url = surl + "/rows"
        headers["Content-Type"] = "application/json"

        # Column id comes from calling api columns/ can't use name as id
        today = datetime.date.today().strftime("%Y-%m-%d")
        # Todp this should really be in a dict write
        payload = {
            "toTop": 'true',
            "cells": [
                # Task NAME
                {"columnId": 6673625647474564,
                 "value": req_type},
                # Job Description
                {"columnId": 8870449879771012,
                 "value": job_desc
                 },
                # Map Size
                {
                    "columnId": 974271080324,
                    "value": map_size
                },
                # Supplementary Data
                {"columnId": 9006524258379652,
                 "value": sup_data
                 },
                # Job Control #
                {"columnId": 3404520484038532,
                 "value": new_jobid
                 },
                # Requested By
                {"columnId": 4366850252400516,
                 "value": email,
                 "displayValue": name
                 },
                # Map
                {"columnId": 3778411379353476,
                 "value": map
                 },
                # Data
                {"columnId": 8282011006723972,
                 "value": data
                 },
                # Analysis
                {"columnId": 963661612246916,
                 "value": analysis
                 },
                # Other
                {"columnId": 5467261239617412,
                 "value": data
                 },
                # Request Source
                {"columnId": 4533976019822468,
                 "value": "New Spatial Form"
                 },
                # Email ME#
                {"columnId": 30376392451972,
                 "value": "N/A"
                 },
                # CC
                {"columnId": 74356857563012,
                 "value": cc_recip
                 },
                # Priority Urgency
                {"columnId": 8633780001892228,
                 "value": priority
                 },
                # Request Date
                {"columnId": 6248973640984452,
                 "value": today
                 },
                # Due Date
                {"columnId": 4421825833789316,
                 "value": req_by
                 },
                # Comments
                {"columnId": 4632932066322308,
                 "value": other_instructions
                 },
            ]
        }
        # Post directly to smartsheet This is working I am bloody amazing...
        r = requests.post(url=url, headers=headers, data=json.dumps(payload))

        pass

    def generate_folders(self):
        """
        Initially we want to generate our id and create our folders on W: and copy
        any attached files into the directory. This is flipping sweet.
        Need to move data from uploads/<job_control>/ into W:/Jobs/data_recieved/
        Mkdir in here called request and write the job_description as a txt file
        :return:
        """
        pass

    def generate_job_control(self):
        """
        Generate a job control number
        :return:
        """
        if not self.cleaned_data.get('job_control'):
            year = datetime.datetime.now().strftime("%Y")
            try:
                control_number = int(max([qs.job_control for qs in YMACSpatialRequest.objects.filter(
                    job_control__icontains=year)]
                                         ).split("-")[1]
                                     ) + 1
            except ValueError:
                control_number = 1
            return "J{0}-{1:0>3}".format(year, control_number)

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
                   'completed_datetime',
                   'request_area',
                    ]
        widgets = {
            'user': autocomplete.ModelSelect2(url='requestuser-autocomplete'),
            'cc_recipients': autocomplete.ModelSelect2Multiple(url='requestuser-autocomplete'),
            'proponent': autocomplete.ModelSelect2(url='proponent-autocomplete'),
            'job_control': forms.HiddenInput(),
            'request_datetime':forms.HiddenInput(),

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
