import csv
import re
import sys
import os
from django.db.models import Q
import datetime
import django
import fnmatch

# Loading in HSIF and PA
sys.path.append(r"C:\Users\cjpoole\Documents\GitHub\YMAC_DB\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

for row in SurveyDocument.objects.all():
    matched = SurveyDocument.objects.filter(Q(filepath=row.filepath)&Q(filename=row.filename))
    if matched.count() > 1:
        for sd in matched:
            print(row.surveys.all())
            if sd.surveys.all() == row.surveys.all():
                print(matched)
