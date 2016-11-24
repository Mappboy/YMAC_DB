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


def find_survey_folder(survey_code, orig_survey, claim_group, date_from):
    """
    Attempt to find our matching folder on Z drive might want to just search for through and see if we can find a matchinging folder
    :param survey_code:
    :param created_on:
    :return:
    """
    folders_search = []
    claim_name = claim_group.group_name
    if not date_from or not survey_code:
        return
    claim_folder = os.path.join(os.path.normpath(r"Z:\Claim Groups"),
                                "{}\\Heritage Surveys\\{}".format(claim_name, date_from.year))
    njamal_dirs = ["Njamal", "Njamal 2", "Njamal 10"]
    check_surveys = []
    if survey_code:
        check_surveys.append(survey_code)
    if orig_survey:
        check_surveys.append(orig_survey)
    if not claim_name == "Njamal":
        for survey in check_surveys:
            folders_search.append(os.path.join(claim_folder, survey))
    else:
        for survey in check_surveys:
            for claim in njamal_dirs:
                folders_search.append(os.path.join(claim_folder, survey))
    if not os.path.isdir(claim_folder):
        print(folders_search)
        print(claim_folder)
        return
    for directory in os.scandir(claim_folder):
        dir_exists = any([directory.path.startswith(check_folder) for check_folder in folders_search])
        if dir_exists:
            return directory.path
    return None


if __name__ == "__main__":
    for survey in HeritageSurvey.objects.filter(folder_location='').filter(survey_group__group_id="YHW"):
        print(find_survey_folder(
            survey.survey_id, survey.original_ymac_id, survey.survey_group, survey.date_from
        )
        )
