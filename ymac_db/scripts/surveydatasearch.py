import os
import re
import fnmatch
import sys, os
import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'
from django.conf import settings

django.setup()

from ymac_db.models import *

DRIVES = [r'K:', r'Z:', r'Q:', r'G:']
# Define our geofile types
GEOFILES = {"*.shp": "Shapefile",
            "*.shz": "Zipped Shapefile",
            "*.gdb": "ESRI Geodatabase",
            "*.kml": "Google KML",
            "*.kmz": "Google Zipped KML",
            "*.tab": "MapInfo Tabfile",
            "*.dwg": "Cadfile",
            "*.gpx": "Garmin GPX",
            }

REPORTFILES = {
    "*.doc*": "Word Document",
    "*.pdf": "PDF FILE"
}

PHOTOS = {
    "*.jpg": "JPEG",
}
filesearch = re.compile("|".join([fnmatch.translate(ext) for ext in GEOFILES.keys()]))
reportsearch = re.compile("|".join([fnmatch.translate(ext) for ext in REPORTFILES.keys()]))
photosearch = fnmatch.translate("*.jpg")
survey_match = re.compile("[A-Z&]{3}\d{3}[-_]?(\d{1,5})?")


# Define our geofile types


def find_survey(survey_string):
    results = []
    survey_qs = HeritageSurveyTrip.objects.filter(survey_id=survey_string)
    if survey_qs:
        results.append(("S", survey_qs))
        return results
    orig_match = HeritageSurveyTrip.objects.filter(original_ymac_id__contains=survey_string)
    if orig_match:
        results.append(("O", orig_match))
    related_code = HeritageSurveyTrip.objects.filter(related_surveys__rel_survey_id=survey_string)
    if related_code:
        results.append(("R", related_code))
    return results


def rscandir(path):
    for entry in os.scandir(path):
        yield entry
        if entry.is_dir():
            yield from rscandir(entry.path)


def filter_survey(survey_results, match_string, dir_entry):
    """
    Trying to match up the correct file to the correct survey
    :param survey_results:
    :param match_string:
    :param dir_entry:
    :return:
    """
    survey_type = 0
    survey_objs = 1
    result = None
    # Actually our zeroeth bet is just check if first tuple is 'O' and zero length
    # IF so return it.
    if len(survey_results[survey_type][survey_objs]) == 1:
        result = survey_results[survey_type][survey_objs]
    # First bet is to try a reverse match on those survey_ids [prop-id]-[tripnum]
    # on our dir entry, if this is good then we can return and forget it
    for surveys in survey_results:
        matched_vals = [match_survey for match_survey in survey_results[survey_objs]
                        if re.search(re.compile(match_survey.survey_id), dir_entry.path)]
        if matched_vals:
            result = matched_vals[1]
            break

    # Next step if it is a 6 character string chances are it might belong to the 0 group
    if len(match_string) == 6:
        # Chances are this is a survey id that should end in 0
        # pull in survey_ids and check if any endwith 0
        # First test the dir_entry.name for a string match
        # Because this might have been neglected in the search path
        for survey_list in survey_results:
            if any(map(lambda x: x.survey_id.endswith('0'), survey_list[1])):
                result = filter(lambda x: x.survey_id.endswith('0'), survey_list[1])

    return result


def main():
    # I think the best bet is to wait till the end of processing before saving.
    # If no file or files for a survey is found then just check if.
    # If we find a directory, we should check to see if it contains a PDF.
    # If it does record that. If not don't worry just save off the directory.

    max_dirs = 1000
    search_dirs = 0
    # A dictionary of Heritage Survey and list of folders
    survey_directories = {}

    survey_files = {}
    for drive in DRIVES:
        print("Started search drive %s" % drive)
        for dentry in rscandir(drive):
            match = survey_match.search(dentry.path)
            if match:
                surveys = find_survey(match.group())
                geofile = filesearch.search(dentry.name)
                # Geo file and match
                if surveys and geofile and dentry.is_file():
                    # try save a SurveyCleaning item get id and then try to add each cleaning join up geofiles
                    # Make sure survey_trip_id is uniq first if not just take the first one
                    # Then save to heritage survey data source
                    print(surveys)
                    print("Found a Survey Geofile {}".format(dentry.name))
                # Survey found and a directory
                elif surveys and dentry.is_dir():
                    # Other wise just save the root dir
                    # print("Found a Survey Directory {}".format(dentry.name))
                    continue
                # Report file and match
                elif surveys and dentry.is_file() and photosearch(dentry.name):
                    # Save out as photo to survey
                    continue
                elif surveys and dentry.is_file() and reportsearch.search(dentry.name) \
                        and "report" in dentry.name.lower() and "draft" not in dentry.name.lower():
                    print("Possible report {}".format(dentry.path))
                    print(surveys)
                elif geofile:
                    print("Found potential spatial file no matching survey {}".format(dentry.name))
                    # no survey found but found some spatial files write out to csv
                    continue
                # No matchin survey potential survey with a report
                elif dentry.is_file() and reportsearch.search(dentry.name) \
                        and "report" in dentry.name.lower() and "draft" not in dentry.name.lower():
                    # no survey found but found a report file write to csv for later checking
                    continue
                elif dentry.is_file() and photosearch.search(dentry.name):
                    # no survey found but found a photos found write to csv for later checking
                    continue
            if dentry.is_dir():
                search_dirs += 1
            if search_dirs > max_dirs:
                break
        if search_dirs > max_dirs:
            break


if __name__ == '__main__':
    print("Running Spatial files analysis")
    main()
    print("Completed Anaylsis Check All drives drive for results")

# Search drives G, Q, H, Z  for directories that match a new survey id or old
# Probably should just use regular expression for each
# re = (surveyid|survey_orig|related_code)

# HeritageSurvey.objects.all():
