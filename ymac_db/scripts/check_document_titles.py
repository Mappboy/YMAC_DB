import os
import sys

import django
from extract_title import *

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import SurveyDocument

for sd in SurveyDocument.objects.all():
    docpdf = os.path.join(sd.filepath, sd.filename)
    if os.path.exists(docpdf) and os.path.splitext(docpdf)[1] == ".pdf" and sd.document_type.sub_type == 'Survey Report':
        try:
            title = pdf_title(docpdf)
            print("{}".format(title.replace("Microsoft Word -","").strip()))
        except Exception as e:
            print(e.args)
            print("Couldn't handle {}".format(sd))
