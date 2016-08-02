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

yinfile = r"Z:\Claim Groups\Yinhawangka\YHW handover\ymac_extract.zip"

with open(yinfile, "wb") as returnfile:
    with ZipFile(returnfile, 'w') as yinzip:
        for sd in SurveyDocument.objects.filter(surveys__survey_group__group_id='YHW'):
            first_survey = sd.surveys.first()
            file2write = os.path.join(sd.filepath, sd.filename)
            if os.path.isfile(file2write):
                yinzip.write(file2write, "{}/{}_Trip{}/{}".format(datetime.datetime.strftime(first_survey.date_from, "%Y"),
                                           first_survey.survey_id,
                                           first_survey.trip_number,
                                           sd.filename))
            else:
                print("Couldn't write %s" % file2write)