import shutil

import smartsheet
from dal import autocomplete
from datetimewidget.widgets import DateWidget
from django import forms as baseform
from django.conf import settings
from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget
from suit.widgets import SuitDateWidget, AutosizedTextarea

from .models import *


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
        # if not os.path.isfile(os.path.join(filepath, filename)):
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
    claim = baseform.ModelMultipleChoiceField(YmacClaim.objects.all(), required=False, label="Claims (if known)",
                                              widget=forms.SelectMultiple(attrs={'size': 10}))
    sup_data_file = baseform.FileField(label="Data files for upload", required=False,
                                       widget=forms.ClearableFileInput(attrs={'multiple': True}))

    # def clean_request_datetime(self):
    #    data = self.cleaned_data.get('request_datetime')
    #    data = datetime.datetime.now()
    #    return data

    def clean(self):
        cleaned_data = super(YMACSpatialRequestForm, self).clean()
        # filepath = cleaned_data.get("filepath")
        # filename = cleaned_data.get("filename")
        # if not os.path.isfile(os.path.join(filepath, filename)):
        #    raise forms.ValidationError("Not a valid file, check path and file name are correct")
        # DO SOME PROCESSING OF MAP TYPE FIRST
        MAP_REQUESTS = [u"Claim Map",
                        u"Quarterly Maps",
                        u"Customised Map",
                        u"Boundary Research Map",
                        u"Site Map"]
        ANALYSIS = [u"Spatial Analysis",
                    u"Boundary Technical Description",
                    u"Map and Technical Description",
                    u"Heritage Mapping",
                    u"Negotiation Mapping"]
        DATA = [
            u"ArcPad Form",
            u"ArcGIS Collector setup",
            u"Data Supply",
            u"Data Update"]
        OTHER = [
            u"Field Work",
            u"Other",
            u"Uncertain"]
        req_type = cleaned_data.get('request_type').name.rstrip()
        self.instance.map_requested = "true" if req_type in MAP_REQUESTS else "false"
        self.instance.analysis = "true" if req_type in ANALYSIS else "false"
        self.instance.data = "true" if req_type in DATA else "false"
        self.instance.other = "true" if req_type in OTHER else "false"
        # By default assign the job to Steve so he can delegate
        self.instance.assigned_to = YmacStaff.objects.get(pk="spashby")

        # Set geom according to if either region or claim groups are set
        #if self.instance.claim:


    def clean_job_control(self):
        data = self.cleaned_data.get('job_control')
        data = self.generate_job_control()
        return data

    def send_email(self):
        """
        This function will send the usual email to us spatial jobs guys.
        :return:
        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        msg = MIMEMultipart()
        email = self.instance.user.email
        toaddr = "cjpoole@ymac.org.au"
        msg_from = email if email else "spatialjobs@ymac.org.au"
        msg['From'] = msg_from
        msg['To'] = "cjpoole@ymac.org.au"
        # ', '.join(["spashby@ymac.org.au",
        #  "cjpoole@ymac.org.au",
        #  "cforsey@ymac.org.au"])
        msg['Subject'] = "{map_type} {job_id} request".format(map_type=self.instance.request_type,
                                                              job_id=self.instance.job_control)
        body = """
        Name: {user}\n
        Email: {user.email}\n
        Department: {user.department}\n
        Request Type: {request_type}\n
        Office: {user.office}\n
        Region: {region}\n
        Job Description: {job_desc}\n
        Supplementary Data: {sup_data_text}\n
        Map Size: {map_size}\n
        Required by: {required_by} \n
        Delivery and/or Product Instructions: {product_type} {other_instructions}\n
        Cost Centre: {cost_centre}\n
        Priority and urgency: {priority}\n""".format(
            **self.cleaned_data
        )
        print(body)
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP('ymac-org-au.mail.protection.outlook.com', 25)
        s.sendmail(msg_from, toaddr, msg.as_string())
        s.quit()

    def update_smartsheet(self):
        """
        This will update smartsheet as we continue to use it.
        :return:
        """
        surl = "https://api.smartsheet.com/2.0/sheets/3001821196248964"

        # Get the top most row and pull out the job control cell and increment and create new id
        ss = smartsheet.Smartsheet("4104lxpew3jppnp3xvoeff7yp")
        # Column id comes from calling api columns/ can't use name as id
        today = datetime.date.today().strftime("%Y-%m-%d")
        # Todp this should really be in a dict write
        row = ss.models.Row()
        row.to_top = True

        cells_to_add = [
            # Task NAME
            {"columnId": 6673625647474564,
             "value": self.cleaned_data['request_type'].name
             },
            # Job Description
            {"columnId": 8870449879771012,
             "value": self.cleaned_data['job_desc']
             },
            # Map Size
            {
                "columnId": 974271080324,
                "value": self.cleaned_data['map_size']
            },
            # Supplementary Data
            {"columnId": 9006524258379652,
             "value": self.cleaned_data['sup_data_text']
             },
            # Job Control #
            {"columnId": 3404520484038532,
             "value": self.cleaned_data['job_control']
             },
            # Requested By
            {"columnId": 4366850252400516,
             "value": self.cleaned_data['user'].email,
             "displayValue": self.cleaned_data['user'].name
             },
            # Map
            {"columnId": 3778411379353476,
             "value": self.instance.map_requested
             },
            # Data
            {"columnId": 8282011006723972,
             "value": self.instance.data
             },
            # Analysis
            {"columnId": 963661612246916,
             "value": self.instance.analysis
             },
            # Other
            {"columnId": 5467261239617412,
             "value": self.instance.data
             },
            # Request Source
            {"columnId": 4533976019822468,
             "value": "Django DB"
             },
            # Email ME#
            {"columnId": 30376392451972,
             "value": "N/A"
             },
            # CC
            {"columnId": 74356857563012,
             "value": self.cleaned_data['cc_recipients']
             },
            # Priority Urgency
            {"columnId": 8633780001892228,
             "value": self.cleaned_data['priority']
             },
            # Request Date
            {"columnId": 6248973640984452,
             "value": self.instance.request_datetime.strftime("%Y-%m-%d")
             },
            # Due Date
            {"columnId": 4421825833789316,
             "value": self.cleaned_data['required_by'].strftime("%Y-%m-%d")
             },
            # Comments
            {"columnId": 4632932066322308,
             "value": self.cleaned_data['other_instructions']
             },
            # Assigned to
            {"columnId": 129332438951812,
             "value": self.instance.assigned_to.email,
             "displayValue": self.instance.assigned_to.full_name.rstrip()
             },
        ]
        for c in cells_to_add:
            row.cells.append(c)
        action = ss.Sheets.add_rows(3001821196248964, [row])

    def generate_folders(self):
        """
        Initially we want to generate our id and create our folders on W: and copy
        any attached files into the directory. This is flipping sweet.
        Need to move data from uploads/<job_control>/ into W:/Jobs/data_recieved/
        Mkdir in here called request and write the job_description as a txt file
        :return:
        """
        jc = self.instance.job_control
        job_dir = "W:/Jobs/{year}/{job_control}".format(year=jc[1:5], job_control=jc)
        if not os.path.isdir(job_dir):
            os.makedirs(job_dir)

        # check if files need uploading if there is push them to new directory
        mr = settings.MEDIA_ROOT
        up_dir = os.path.join(mr, jc)
        if os.path.isdir(up_dir):
            shutil.move(up_dir, job_dir)

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
        exclude = ['map_requested',
                   'data',
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
            'related_jobs': autocomplete.ModelSelect2Multiple(url='requestjobcontrol-autocomplete'),
            'job_control': forms.HiddenInput(),
            'request_datetime': forms.HiddenInput(),

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
