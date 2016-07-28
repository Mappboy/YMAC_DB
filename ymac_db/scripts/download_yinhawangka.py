import os
import re
import sys
import csv
import django
import datetime
from zipfile import ZipFile

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

yinzip = r"Z:\Claim Groups\Yinhawangka\YHW handover\ymac_extract.zip"

with open(yinzip, "wb") as returnfile:
    for sd in SurveyDocument.objects.filter(surveys__survey_group__group_id='YHW'):
        first_survey = sd.surveys.first()
        print(os.path.join(sd.filepath, sd.filename))
        print("{}/{}_Trip{}/{}".format(datetime.datetime.strftime(first_survey.date_from, "%Y"),
                                       first_survey.survey_id,
                                       first_survey.trip_number,
                                       sd.filename))