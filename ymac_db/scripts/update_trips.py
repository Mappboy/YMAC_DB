import fnmatch
import os
import re
import sys
import pickle
import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

# Extract folders
get_folder_re = re.compile(r"(?P<folder_path>Z:\\?Claim Groups\\(?P<claim_group>\w+)"
                           r"\\Heritage Surveys\\\d{4}\\)"
                           r"(?P<folder>[A-Za-z0-9_\- &\(\),.]+(\\))")

trip_re = re.compile(r"trip[ _\-]?(?P<trip_num>\d)", re.I)
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
        results.append(("S", survey_qs))
        return results
    orig_match = HeritageSurvey.objects.filter(original_ymac_id__contains=survey_string)
    if orig_match:
        results.append(("O", orig_match))
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
    Checks are query set for any matching folder paths
    :param qs:
    :return:
    """
    for sc in qs:
        if sc != SurveyDocument:
            filepath = sc.data_path
        else:
            filepath = sys.path.join(sc.filepath, sc.filename)
        print(filepath)
        continue
        if filepath not in data_paths and get_folder_re.search(filepath):
            data_paths.add(sc.data_path)
            match = get_folder_re.match(filepath)
            matches.append(sc)
            folder = match.groupdict()['folder']
            # print(match.groupdict())
            for hs in sc.heritagesurvey_set.all():
                if hs not in hs_dp:
                    trip_match = trip_re.search(folder)
                    if trip_match and hs.survey_trip.trip_number == int(trip_match.groupdict()['trip_num']):
                        hs_dp[hs] = folder
                        print("Assigning {} to {}".format(hs, folder))
                    else:
                        hs_dp[hs] = folder
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

for qs in [SurveyDocument.objects.all(), SurveyCleaning.objects.all(), SurveyTripCleaning.objects.all()]:
    search_docs(qs)