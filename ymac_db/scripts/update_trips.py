import os
import re
import sys
import csv
import django
import datetime

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

# Extract folders
get_folder_re = re.compile(r"(?P<folder_path>Z:\\?Claim Groups\\{1,2}(?P<claim_group>\w+)"
                           r"\\Heritage Surveys\\\d{4}\\)"
                           r"(?P<folder>[A-Za-z0-9_\- &\(\),.]+(\\))")

trip_re = re.compile(r"trip[ _\-]?(?P<trip_num>\d)", re.I)
multi_trip_re = re.compile(r"trip(s)?[ _\-]?(?P<trip_num_start>\d)[\-_& ]+(?P<trip_num_end>\d)", re.I)
matches = []
data_paths = set()
hs_dp = {}
survey_match = re.compile("(?P<survey_val>[A-Z&]{3}\d{3})[-_]?(?P<trip_val>\d{1,5})?")

def update_dates():
    """
    This was a fix for the dates that were bad in the database
    :return:
    """
    data_file = r"W:\Utility\SpatialDatabase\cleaned_codes.csv"
    with open(data_file,'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            survey = HeritageSurvey.objects.filter(trip_number=row['trip_number'], survey_id=row['primary_svy_name'])
            if row['start_date']:
                sdate = datetime.datetime.strptime(row['start_date'], "%d/%m/%Y")
                print(sdate)
                survey.update(date_from=sdate)
            if row['end_date']:
                edate = datetime.datetime.strptime(row['end_date'], "%d/%m/%Y")
                print(edate)
                survey.update(date_to=edate)


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
                surveys = find_survey(match.group())
                if len(surveys) == 1:
                    if surveys[0][0].folder_location and surveys[0][0].folder_location != full_path:
                        print("{}\t{}\t{}".format(surveys[0][0], full_path,
                                                                                   surveys[0][0].folder_location))
                    elif surveys[0][0].survey_id.endswith("0"):
                        surveys[0].update(folder_location=full_path.replace("\\\\", "\\"))
                    else:
                        surveys[0].update(folder_location=full_path.replace("\\\\", "\\"))
                elif len(surveys) > 1:
                    m = multi_trip_re.search(full_path)
                    tm = trip_re.search(full_path)
                    if m:
                        for tp in range(int(m.groupdict()['trip_num_start']), int(m.groupdict()['trip_num_end'])+1):
                            for survey in surveys:
                                if survey.trip_number == tp:
                                    if survey.folder_location:
                                        print("{}\t{}\t{}".format(survey, full_path,
                                                                        survey.folder_location))
                                    survey.update(folder_location=full_path.replace("\\\\", "\\"))
                    elif tm:
                        fsurvey = HeritageSurvey.objects.filter(survey_id=match.group,
                                                                trip_number=tm.groupdict()['trip_num'])
                        if fsurvey:
                            if fsurvey.folder_location:
                                print("{}\t{}\t{}".format(fsurvey, full_path,
                                                                                 fsurvey.folder_location))
                            fsurvey.update(folder_location=full_path.replace("\\\\", "\\"))
                        else:
                            # couldn't find survey using trip number try and us comments other wise just write it out
                            print("No survey\t{}\t{}".format(surveys, full_path))
                else:
                    print("No survey\t{}\t{}".format(surveys, full_path))
                    # print out paths that don't we couldn't find surveys for
        else:
            continue


# for qs in [SurveyDocument.objects.all(), SurveyCleaning.objects.all()]:
#    search_docs(qs)

search_directory()

# Need something to update all folders everynow and then.