import os, sys
from ..models import *
import fnmatch
import time
import csv
import re

DRIVES = ["Z:\Claim Groups\Yinhawangka\Heritage Surveys\\"]


# Define our geofile types

def main():
    with open("Z:\Claim Groups\Yinhawangka\\records.csv", "wb") as csvfile:
        CSVFIELDS = ["Year", "Folders", "Report Found"]
        writer = csv.DictWriter(csvfile, fieldnames=CSVFIELDS, dialect='excel')
        writer.writeheader()
        for drive in DRIVES:
            for root, dirs, files in os.walk(drive, topdown=False):
                if re.search(r'\d{4}', os.path.split(root)[1]):
                    for folders in dirs:
                        writer.writerow(
                            dict(
                                zip(CSVFIELDS, [os.path.split(root)[1],
                                                folders,
                                                "No"])
                            )
                        )


if __name__ == '__main__':
    print "Running Spatial files analysis"
    main()
    print "Completed Anaylsis Check All drives drive for results"
proj_path = "C:/Users/cjpoole/PycharmProjects/ymac_sdb/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ymac_sdb.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Search drives G, Q, H, Z  for directories that match a new survey id or old
# Probably should just use regular expression for each
# re = (surveyid|survey_orig|related_code)
for survey in HeritageSurvey.objects.all():
    primkey, st = survey.pk, survey.survey_trip
