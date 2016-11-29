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

# WE actually want to make sure that and documents whose surveys are different are joined up.
# If however the survey id is the same and document id is different then delete it
for row in SurveyDocument.objects.all():
    matched = SurveyDocument.objects.filter(Q(filepath=row.filepath)& Q(filename=row.filename))
    if matched.count() > 1:
        for sd in matched:
            if [d.id for d in sd.surveys.all()] != [ d.id for d in row.surveys.all()] and sd.id != row.id:
                print(sd,row)
                #SurveyDocument.objects.filter(id=row.id).delete()
