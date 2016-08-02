import os
import re
import sys
import django
import datetime
from django.db.models import Q

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

for sd in SurveyDocument.objects.filter(~Q(filepath='')):
    fp = os.path.normpath(sd.filepath)
    fn = os.path.normpath(sd.filename)
    if os.path.isfile(os.path.join(fp, fn)):
        SurveyDocument.objects.filter(id=sd.id).update(filepath=fp)
    #SurveyDocument.objects.filter(id=hs.id).update(folder_location=os.path.normpath(hs.folder_location))