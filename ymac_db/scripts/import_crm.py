import csv
import re
import sys
import os
from django.db.models import Q
import datetime
import django

# Loading in HSIF and PA
sys.path.append(r"C:\Users\cjpoole\Documents\GitHub\YMAC_DB\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

DATE_CUT_OFF = datetime.datetime(2016, 7, 11)


def get_clean_survey_code(survey_string):
    """
    Fucntion to check if a code is correct formatting or can be turned into a correct forrmating
    :return: A valid and formatted code
    >>> get_clean_survey_code("Westdeen Holdings Pty Ltd")

    >>> get_clean_survey_code("YHW018_113")
    'YHW018-113'
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
    >>> get_matching_surveys("AMA245-5")
    <QuerySet []>
    >>> get_matching_surveys("YHW018-113")
    <QuerySet [<HeritageSurvey: YHW018-113 (Trip 2)- Turee Creek Drilling>, <HeritageSurvey: YHW018-113 (Trip 1)- Turee Creek Drilling Program>]>
    """
    return HeritageSurvey.objects.filter(Q(survey_id=cleaned_survey_string))


def get_trip_number(suvey_querset, survey_start_date, survey_end_date):
    """
    Match up queries with survey date
    :param suvey_querset:
    :param survey_date:
    :return:
    """
    trip_number = 1
    for survey in suvey_querset:
        if survey.date_from == survey_start_date or survey.date_to == survey_end_date:
            return survey.trip_number
        if survey.trip_number > trip_number:
            trip_number = survey.trip_number
    return trip_number + 1


def get_claim_group(claim_group, survey_code):
    """
    Returns a valid ymac claim group for SurveyGroup
    :param claim_group:
    :return:
    >>> get_claim_group("Yinhawangka (For Heritage)", 'YHW018-132')
    <SurveyGroup: Yinhawangka>
    """
    return SurveyGroup.objects.filter(group_id=survey_code[:3]).first()


def find_survey_folder(survey_code, orig_survey, created_on, claim_group):
    """
    Attempt to find our matching folder on Z drive
    :param survey_code:
    :param created_on:
    :return:
    """
    folders_search = []
    claim_name = claim_group.group_name
    claim_folder = os.path.join(os.path.normpath(r"Z:\Claim Groups"),
                                "{}\\Heritage Surveys\\{}".format(claim_name, created_on.year))
    njamal_dirs = ["Njamal", "Njamal 2", "Njamal 10"]
    if not claim_name == "Njamal":
        for survey in [survey_code, orig_survey]:
            folders_search.append(os.path.join(claim_folder, survey))
    else:
        for survey in [survey_code, orig_survey]:
            for claim in njamal_dirs:
                folders_search.append(os.path.join(claim_folder, survey))
    for directory in os.scandir(claim_folder):
        dir_exists = any([directory.path.startswith(check_folder) for check_folder in folders_search])
        if dir_exists:
            return directory.path
    return None


def get_methodology(methodologies):
    """
    Lookup and return a queryset of methodologies
    :param methodologies:
    :return:
    """
    methods = {'WPC': 'Work Program Clearance',
               'WAC': 'Work Area Clearance',
               'SID': 'Site ID',
               'SA': 'Site Avoidance',
               'S18C': 'Section 18',
               'S16': 'Section 16',
               'MON': 'Monitoring',
               'REC': 'Reconnaissance',
               }
    return [SurveyMethodology.objects.get(survey_meth=methods[meth]) for meth in methodologies if meth]


def get_survey_type(raw_type):
    """
    Return cleaned survey type
    :param raw_type:
    :return:
    """
    survey_types = {
        'ETH/ARC': 'AE1',
        'ARC': 'A1',
        'MON': 'M',
        'ETH': 'E1',
    }
    return SurveyType.objects.get(type_id=survey_types[raw_type])


def check_folder_for_docs(folder_path):
    """
    Checks folder for any heritage documents or links existing documents up
    :param folder_path:
    :return:
    """


if __name__ == "__main__":
    import doctest

    if len(sys.argv) < 2:
        print("Please provide crm filename")
        exit()
    filename = sys.argv[1]
    crm_folder = os.path.normpath(r"X:\Projects\SpatialDatabase\Import CRM")
    crm_file = os.path.join(crm_folder, filename)
    if not os.path.isfile(crm_file):
        print("Could not locate {}".format(crm_file), file=sys.stderr)
        exit()
    with open(crm_file, "r") as crm_csv:
        reader = csv.DictReader(crm_csv, delimiter='\t')
        for row in reader:
            created_on = datetime.datetime.strptime(row["Created On"], "%d/%m/%y %H:%M %p")
            # All these should be in the database and some are tests so
            if created_on <= DATE_CUT_OFF:
                break
            original_ymac_code = row['Survey Code']
            survey_code = get_clean_survey_code(original_ymac_code)
            # Just skip bad survey codes
            if survey_code is None:
                print("Bad survey code ", row['Survey Code'])
                continue
            start_date = datetime.datetime.strptime(row["Start Date"], "%d/%m/%y")
            end_date = datetime.datetime.strptime(row["Est End Date"], "%d/%m/%y")
            # Check trip numbers if start_date and end_date don't match then increment trip number or set as trip 1
            matching_codes = get_matching_surveys(survey_code)
            trip_number = 1
            if matching_codes:
                trip_number = get_trip_number(matching_codes, start_date, end_date)
            # check this doing the correct look ups
            created_by = SiteUser.objects.filter(user_name=row["Created By"]).first()
            survey_group = get_claim_group(row["Claim Group"], survey_code)
            # If pa or report file path search for the relevant files

            folder_location = find_survey_folder(survey_code, original_ymac_code, created_on, survey_group)
            proponent = Proponent.objects.filter(name=row['Proponent']).first()
            methodologies = get_methodology([row["Survey Methodology"], row["Survey Methodology 2"]])
            survey_status = row["Survey Status"]
            survey_type = get_survey_type(row["Survey Type 1"])
            obj, created = HeritageSurvey.objects.update_or_create(
                survey_code,
                trip_number,
                created_by,
                survey_group,
                folder_location,
                proponent,
                methodologies,
                survey_status,
                survey_type,
                original_ymac_code)
    doctest.testmod()
