import os
import re
import sys
import csv
import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

# Extract folders
get_folder_re = re.compile(r"(?P<folder_path>Z:\\?Claim Groups\\{1,2}(?P<claim_group>\w+)"
                           r"\\Heritage Surveys\\\d{4}\\)"
                           r"(?P<folder>[A-Za-z0-9_\- &\(\),.]+(\\))")

trip_re = re.compile(r"trip[ _\-]?(?P<trip_num>\d)", re.I)
multi_trip_re = re.compile(r"trip[ _\-]?(?P<trip_num_start>\d)-(?P<trip_num_end>\d)", re.I)
matches = []
data_paths = set()
hs_dp = {}
survey_match = re.compile("[A-Z&]{3}\d{3}[-_]?(\d{1,5})?")


def find_survey(survey_string):
    """
    Given a survey string from a path finds a matching Heritage Survey Trip
    :param survey_string:
    :return:
    """
    results = []
    survey_string = survey_string.replace("_", '-')
    survey_qs = HeritageSurvey.objects.filter(survey_id=survey_string)
    if survey_qs:
        results.append(survey_qs)
        return results
    orig_match = HeritageSurvey.objects.filter(original_ymac_id__contains=survey_string)
    if orig_match:
        results.append(orig_match)
    return results


def rscandir(path):
    """
    Recursive directory scanner
    :param path:
    :return:
    """
    for entry in os.scandir(path):
        try:
            yield entry
        except PermissionError:
            continue
        except FileNotFoundError:
            continue
        if entry.is_dir():
            try:
                yield from rscandir(entry.path)
            except PermissionError:
                continue
            except FileNotFoundError:
                continue


def search_docs(qs):
    """
    Checks are query set for any matching folder paths for currently found documentation
    :param qs:
    :return:
    """
    for sc in qs:
        if type(sc) != SurveyDocument:
            filepath = os.path.split(sc.data_path)[0]
        else:
            filepath = sc.filepath
        if filepath not in data_paths and get_folder_re.search(filepath):
            data_paths.add(filepath)
            match = get_folder_re.match(filepath)
            if match:
                print(filepath)
            continue
            matches.append(sc)
            folder = match.groupdict()['folder']
            folder_path = match.groupdict()['folder_path']
            # print(match.groupdict())
            # First check if Survey is only trip.
            for hs in sc.heritagesurvey_set.all():
                if hs not in hs_dp:
                    trip_match = trip_re.search(folder)
                    if trip_match and hs.survey_trip.trip_number == int(trip_match.groupdict()['trip_num']):
                        hs_dp[hs] = folder_path
                        print("Assigning {} to {}".format(hs, folder))
                    else:
                        hs_dp[hs] = folder_path
                        print("Assigning {} to {}".format(hs, folder))
                # We need to match on trips
                elif hs in hs_dp and hs_dp[hs] != folder:
                    trip_match = trip_re.search(folder)
                    if not trip_match and hs.survey_trip.trip_number == 1:
                        hs_dp[hs] = folder
                        print("Reassigning {} to {}".format(hs, folder))
                    elif trip_match and hs.survey_trip.trip_number == int(trip_match.groupdict()['trip_num']):
                        hs_dp[hs] = folder
                        print("Reassigning {} to {}".format(hs, folder))
                    else:
                        print("Differing data paths for {}: {} - {}".format(
                            hs, hs_dp[hs], folder
                        ))
                else:
                    print("Skipping {}".format(hs))


def search_directory():
    """
    Search in the Z drive claims folder.
    Match against current surveys.
    :return:
    """
    matched = set()
    for claim_folder in rscandir(r"Z:\Claim Groups\\"):
        folder_match = get_folder_re.match(claim_folder.path)
        if folder_match:
            full_path = os.path.join(folder_match.groupdict()['folder_path'], folder_match.groupdict()['folder'])
            if full_path in matched:
                continue
            match = survey_match.search(claim_folder.path)
            if match:
                matched.add(full_path)
                # Now check if we are dealing with multiple surveys. If so try trip matching etc
                print(find_survey(match.group()))
                print(full_path)
                # If there is no matching survey found we should write these out to stderr or a file perhaps
        else:
            continue


# for qs in [SurveyDocument.objects.all(), SurveyCleaning.objects.all()]:
#    search_docs(qs)

search_directory()

not_found = ["YHW018-81",
             "YHW018-110",
             "YHW018-109",
             "YHW018-112",
             "YHW018-116"]


def update_dates():
    data_file = r"W:\Utility\SpatialDatabase\cleaned_codes.csv"
    with open(data_file,'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            print(HeritageSurvey.objects.filter(trip_number=row['trip_number'], survey_id=row['primary_svy_name']))


