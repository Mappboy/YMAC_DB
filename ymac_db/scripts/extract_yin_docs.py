import zipfile
import os
import pickle
import re
import sys

import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

# For each document write out if YHW.
for survey_docs in SurveyDocument.objects.filter(surveys__survey_group__group_id="YHW"):
    print(survey_docs)

# Also create spreadsheet of survey details