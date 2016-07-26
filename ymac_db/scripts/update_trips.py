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
survey_match = re.compile("[A-Z&]{3}\d{3}[-_]?(\d{1,5})?")

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

updates = [
("NJA365-2 (Trip 1)- A1051 Corruna Downs Project - Split Rock Prospect, A1053 Daltons Pit, Road Upgrade - Mount Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA365-2 (Trip 1) A1051 Atlas Corruna Downs_Mt Webber\\"),
("NJA555-10 (Trip 2)- Abydos Mettams, Leightons & Cove Expansion",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-10\\"),
("NJA555-11 (Trip 3)- Mt Webber Road Upgrade and Water Bore. Mt Webber Project - Webber North",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-11 Mt Webber AI053, AI070\\"),
("NJA555-12 (Trip 1)- McPhee Creek",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-12\\"),
("NJA555-13 (Trip 1)- McPhee Creek",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-13\\"),
("NJA555-14 (Trip 1)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-14\\"),
("NJA555-15 (Trip 2)- AI083",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-15\\"),
("NJA555-16 (Trip 1)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-16\\"),
("NJA555-18 (Trip 2)- McPhee Creek",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-18\\"),
("NJA555-19 (Trip 3)- McPhee Creek",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-19\\"),
("NJA555-20 (Trip 1)- McPhee Creek",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-20\\"),
("NJA555-23 (Trip 2)- AI095",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_23_Trip2 & Trip3_ARC_SID\\"),
("NJA555-26 (Trip 2)- Mt Webber Footprint AI098",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_26_Trip2\\"),
("NJA555-28 (Trip 1)- Farrell Well - Miralga Creek",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_28_ARC_ETH_SA\\"),
("NJA555-29 (Trip 1)- Abydos",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-29\\"),
("NJA555-30 (Trip 1)- Abydos",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-30\\"),
("NJA555-31 (Trip 1)- Mount Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_31_ARC_ETH_WPC_SA\\"),
("NJA555-32 (Trip 1)- Abydos Haul Road Shute Drains",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_32_ARC_ETH_WPC\\"),
("NJA555-33 (Trip 1)- Corunna Downs AI115",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_33_ETH_SID\\"),
("NJA555-34 (Trip 1)- Mt Webber -  AI114",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_34_ARC_ETH_S18C\\"),
("NJA555-35 (Trip 1)- Abydos",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_35_ETH_SID_S18C (GANGA MAYA ROCKSHELTER)\\"),
("NJA555-37 (Trip 1)- McPhee Creek AI119",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_37_ETH_WPC\\"),
("NJA555-38 (Trip 2)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_38_ARC_ETH_SID\\"),
("NJA555-38 (Trip 2)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_38_Trip2_ARC_ETH_SID\\"),
("NJA555-39 (Trip 1)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_39_ARC_ETH_SID_SA\\"),
("NJA555-40 (Trip 1)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_40_ARC_ETH_SID_SA\\"),
("NJA555-41 (Trip 1)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_41_ARC_ETH_SID_SA\\"),
("NJA555-42 (Trip 1)- McPhee Creek: Crescent Moon",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_42_ARC_SID\\"),
("NJA555-43 (Trip 1)- McPhee Creek AI096",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_43_ETH_SID\\"),
("NJA555-44 (Trip 1)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_44_ARC_ETH_SA\\"),
("NJA555-45 (Trip 1)- Mt Webber",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_45_ARC_ETH_SA\\"),
("NJA555-46 (Trip 1)- Abydos",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_46_MON\\"),
("NJA555-47 (Trip 1)- Corunna Downs",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_47_ARC_ETH_SA\\"),
("NJA555-48 (Trip 1)- Abydos Ganga Maya",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_48_ARC_S16\\"),
("NJA555-49 (Trip 1)- AI138",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_49_ARC_ETH_SA\\"),
("NJA555-50 (Trip 1)- AI140",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_50_ARC_ETH_SID\\"),
("NJA555-51 (Trip 1)- Mt Webber AI141",r"Z:\Claim Groups\Njamal\Heritage Surveys\2014\NJA555_51_ARC_ETH_SID\\"),
("NJA555-52 (Trip 1)- AI142 - Abydos geotech site visit",r"Z:\Claim Groups\Njamal\Heritage Surveys\2015\NJA555_52_MON\\"),
("NJA555-54 (Trip 1)- Mardu Maya Salvage of Surface Artefacts",r"Z:\Claim Groups\Njamal\Heritage Surveys\2015\NJA555_54_MON\\"),
("NJA555-7 (Trip 1)- Abydos East HR Additional Alignment Requirements",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-7 A1057 AI064 - Atlas Abydos McPhee Creek\\"),
("NJA555-8 (Trip 1)- AI062 Daltons North, AI063 Mt Webber Ibanez Salvage, AI065 Mt Webber Water Bores",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-8 Atlas AI062 Daltons, AI063 Mt Webber Ibanez , AI065Mt Webber\\"),
("NJA555-9 (Trip 1)- Abydos Rockshelter Excavations",r"Z:\Claim Groups\Njamal\Heritage Surveys\2013\NJA555-9 Excavations Abydos AI041\\"),
]

for u in updates:
    trip_num = trip_re.search(u[0]).groupdict()['trip_num']
    survey_id = u[0].split()[0]
    HeritageSurvey.objects.filter(survey_id=survey_id, trip_number=trip_num).update(folder_location=u[1])