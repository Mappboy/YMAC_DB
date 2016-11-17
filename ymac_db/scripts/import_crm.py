import csv
import re
import sys
import os
from django.db.models import Q
import datetime
import django

# Loading in HSIF and PA
sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *
DATE_CUT_OFF = datetime.datetime(2016, 7, 11)


def get_clean_survey_code(survey_string):
    """
    Fucntion to check if a code is correct formatting or can be turned into a correct forrmating
    :return: A valid and formatted code
    >>> get_survey_code("AMA245-5")
    []
    >>> get_survey_code("Westdeen Holdings Pty Ltd")

    >>> get_survey_code("YHW018_113_Trip2_ETH_SA")
    [<HeritageSurvey: YHW018-113 (Trip 1)- Turee Creek Drilling Program>, <HeritageSurvey: YHW018-113 (Trip 2)- Turee Creek Drilling>]
    """
    survey_match = re.match("[A-Z&]{3}\d{3}[-_]?(\d{1,5})?", survey_string)
    if not survey_match:
        return None
    return survey_match.group().replace("_", '-')



def get_matching_surveys(cleaned_survey_string):
    """
    Returns heritage surveys for matching cleaned survey string
    :param cleaned_survey_string:
    :return:
    """
    return HeritageSurvey.objects.filter(Q(survey_id=cleaned_survey_string))

def get_trip_number(suvey_querset, survey_start_date, survey_end_date):
    """
    Match up queries with survey date
    :param suvey_querset:
    :param survey_date:
    :return:
    """
    pass

def get_claim_group(claim_group, survey_code):
    """
    Returns a valid ymac claim group for SurveyGroup
    :param claim_group:
    :return:
    """
    return SurveyGroup.objects.filter(group_id=survey_code[:3]).first()



def find_survey_folder(survey_code, created_on):
    """
    Attempt to find our matching folder on Z drive
    :param survey_code:
    :param created_on:
    :return:
    """
    pass

def get_methodology(methodologies):
    """
    Lookup and reutrn a queryset of methodologies
    :param methodologies:
    :return:
    """
    pass


if __name__ == "__main__":
    import doctest
    if len(sys.argv) < 2:
        print("Please provide crm filename")
        exit()
    filename = sys.argv[1]
    crm_folder = os.path.normpath(r"X:\Projects\SpatialDatabase\Import CRM")
    crm_file = os.path.join(crm_folder, filename)
    if not os.path.isfile(crm_file):
        print("Could not locate {}".format(crm_file),  file=sys.stderr)
        exit()
    with open(crm_file,"r") as crm_csv:
        reader = csv.DictReader(crm_csv, delimiter='\t')
        for row in reader:
            created_on = datetime.datetime.strptime(row["Created On"], "%d/%m/%y %H:%M %p")
            # All these should be in the database and some are tests so
            if created_on <= DATE_CUT_OFF:
                break
            survey_code = get_clean_survey_code(row['Survey Code'])
            # Just skip bad survey codes
            if survey_code is None:
                print("Bad survey code ", row['Survey Code'])
                continue
            start_date = datetime.datetime.strptime(row["Start Date"], "%d/%m/%y")
            end_date = datetime.datetime.strptime(row["Est End Date"], "%d/%m/%y")
            # Check trip numbers if start_date and end_date don't match then increment trip number or set as trip 1
            if get_matching_surveys(survey_code):
                print(row)
            # check this doing the correct look ups
            #created_by = SiteUser.objects.first(name=row["Created By"]))
            # survey_group = get_claim_group
            # If pa or report file path search for the relevant files

            # folder_location = find_survey_folder(survey_code, created_on)
            # proponent = Proponent.objects.filter(name=row['Proponent']).first()

    doctest.testmod()
