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

DRIVES = [r'Z:', r'G:', r'Q:', r'K:']
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
photosearch = re.compile(fnmatch.translate("*.jpg"))
survey_match = re.compile("[A-Z&]{3}\d{3}[-_]?(\d{1,5})?")


# Define our geofile types


def find_survey(survey_string):
    results = []
    survey_string = survey_string.replace("_", '-')
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


def filter_survey(survey_results, match_string, dir_entry):
    """
    Trying to match up the correct file to the correct survey and Return a Heritage Survey record for it.
    :param survey_results:
    :param match_string:
    :param dir_entry:
    :return: A list of surveys or survey trips
    """
    survey_type = 0
    survey_objs = 1
    # Actually our zeroeth bet is just check if first tuple is 'O' and zero length
    # IF so return it.
    if survey_results and len(survey_results[survey_type][survey_objs]) == 1:
        return [survey_results[survey_type][survey_objs][0].heritagesurvey_set.all()[0]]

    # If heritage survey survey ids match for each trip then just return that survey
    her_surveys = set()
    for surveys in survey_results:
        for survey in surveys[survey_objs]:
            her_surveys.add(survey.survey_id)
    if len(her_surveys) == 1:
        return [survey.heritagesurvey_set.all()[0] for surveys in survey_results for survey in surveys[survey_objs]]

    # Another bet is to try a reverse match on those survey_ids [prop-id]-[tripnum]
    # on our dir entry, if this is good then we can return and forget it
    # Bit of a mess but it will do
    sub_match_surveys = set()
    sub_match = []
    for surveys in survey_results:
        for match_survey in surveys[survey_objs]:
            sub_str = re.split('[A-Z]', match_survey.survey_id)[-1].replace('-', '[-_]') + "[-_ ]"
            re_sub = re.compile(sub_str)
            if re_sub.search(dir_entry.path):
                sub_match.append(match_survey)
    if sub_match:
        for survey in sub_match:
            sub_match_surveys.add(survey.heritagesurvey_set.all()[0])
        return list(sub_match)

    # Next step if it is a 6 character string chances are it might belong to the 0 group
    zero_match_surveys = set()
    if survey_results and len(match_string) == 6:
        # Chances are this is a survey id that should end in 0
        # pull in survey_ids and check if any endwith 0
        # First test the dir_entry.name for a string match
        # Because this might have been neglected in the search path

        for survey_list in survey_results:
            if any(map(lambda x: x.survey_id.endswith('-0'), survey_list[survey_objs])):
                for survey in filter(lambda x: x.survey_id.endswith('-0'), survey_list[survey_objs]):
                    zero_match_surveys.add(survey.heritagesurvey_set.all()[0])
        if zero_match_surveys:
            return list(zero_match_surveys)
    if survey_results and survey_results[0][survey_type] == 'S':
        return list(survey_results[0][survey_objs])
    else:
        return [survey for surveys in survey_results for survey in surveys[survey_objs]]


def main():
    # I think the best bet is to wait till the end of processing before saving.
    # If no file or files for a survey is found then just check if.
    # If we find a directory, we should check to see if it contains a PDF.
    # If it does record that. If not don't worry just save off the directory.

    def _sort_results(results, type_of_results, dir_entry, survey_dirs, survey_trips, survey_files):
        for result in results:
            if type(result) == HeritageSurveyTrip:
                if result not in survey_trips:
                    survey_trips[result] = [(type_of_results, dir_entry.path)]
                else:
                    survey_trips[result].append((type_of_results, dir_entry.path))
            # Must be empty or Heritage Survey
            else:
                if type_of_results == 'Directory':
                    if result not in survey_dirs:
                        survey_dirs[result] = [dir_entry.path]
                    else:
                        try:
                            if os.path.commonpath(survey_dirs[result] + [dir_entry.path]) not in survey_dirs[result]:
                                survey_dirs[result].append(dir_entry.path)
                        except ValueError:
                            survey_dirs[result].append(dir_entry.path)
                            # Skip it no point adding sub folders

                else:
                    if result not in survey_files:
                        survey_files[result] = [(type_of_results, dir_entry.path)]
                    else:
                        survey_files[result].append((type_of_results, dir_entry.path))

    spatial_files = 0
    survey_dirs = 0
    photos = 0
    reports = 0
    spatial_files_nomatch = 0
    photos_nomatch = 0
    reports_nomatch = 0

    max_dirs = 100
    search_dirs = 0
    # A dictionary of Heritage Survey and list of folders
    survey_directories = {}
    survey_trip_to_sort = {}
    survey_files = {}
    # for drive in DRIVES:
    #    print("Started search drive %s" % drive)
    #    for dentry in rscandir(drive):
    #        match = survey_match.search(dentry.path)
    #        if match:
    #            surveys = find_survey(match.group())
    #            geofile = filesearch.search(dentry.name)
    #            # If we can't find a match this may return survey trips
    #            matched_hsurvey = filter_survey(surveys, match.group(), dentry)
    #            # Geo file and match
    #            if surveys and geofile and dentry.is_file():
    #                # try save a SurveyCleaning item get id and then try to add each cleaning join up geofiles
    #                # Make sure survey_trip_id is uniq first if not just take the first one
    #                # Then save to heritage survey data source
    #                _sort_results(matched_hsurvey, 'Spatial File', dentry, survey_directories, survey_trip_to_sort,
    #                              survey_files)
    #                search_dirs += 1
    #                spatial_files += 1
    #            # Survey found and a directory
    #            elif surveys and dentry.is_dir():
    #                # Other wise just save the root dir
    #                print("Found a Survey Directory {}".format(dentry.name))
    #                print(matched_hsurvey)
    #                _sort_results(matched_hsurvey, 'Directory', dentry, survey_directories, survey_trip_to_sort,
    #                              survey_files)
    #                survey_dirs += 1
    #            # Report file and match
    #            elif surveys and dentry.is_file() and photosearch.search(dentry.name):
    #                # Save out as photo to survey
    #                _sort_results(matched_hsurvey, 'Photo', dentry, survey_directories, survey_trip_to_sort,
    #                              survey_files)
    #                photos += 1
    #            elif surveys and dentry.is_file() \
    #                    and reportsearch.search(dentry.name) \
    #                    and "report" in dentry.name.lower() \
    #                    and "draft" not in dentry.name.lower() \
    #                    and not dentry.name.startswith('~'):
    #                _sort_results(matched_hsurvey, 'Survey Report', dentry, survey_directories, survey_trip_to_sort,
    #                              survey_files)
    #                reports += 1
    #            elif geofile:
    #                # no survey found but found some spatial files write out to csv
    #                PotentialSurvey.objects.create(survey_id=match.group(), data_path=dentry.path, path_type='Spatial File')
    #
    #                spatial_files_nomatch += 1
    #            # No matchin survey potential survey with a report
    #            elif dentry.is_file() and reportsearch.search(dentry.name) \
    #                    and "report" in dentry.name.lower() and "draft" not in dentry.name.lower():
    #                # no survey found but found a report file write to csv for later checking
    #                PotentialSurvey.objects.create(survey_id=match.group(), data_path=dentry.path, path_type='Survey Report')
    #                reports_nomatch += 1
    #            elif dentry.is_file() and photosearch.search(dentry.name):
    #                # no survey found but found a photos found write to csv for later checking
    #                PotentialSurvey.objects.create(survey_id=match.group(), data_path=dentry.path, path_type='Photo')
    #                photos_nomatch += 1
    #
    # for key in survey_files.keys():
    #    try:
    #        del survey_directories[key]
    #    except KeyError:
    #        continue
    # counts = {'Spatial Files': spatial_files,
    #          'Survey Directories': survey_dirs,
    #          'Photos': photos,
    #          'Reports': reports,
    #          'Spatial Files No Match': spatial_files_nomatch,
    #          'Photos No Match': photos_nomatch,
    #          'Reports No Match': reports_nomatch}
    # print(counts)
    # print(len(survey_directories))
    # print(len(survey_files))
    # print(len(survey_trip_to_sort))
    pt = {'Geofile': 'Spatial File',
          'Report': 'Survey Report',
          'Photo': 'Photo',
          'Directory': 'Directory'}
    # with open('directories.pickle', 'r') as f:
    #    # Pickle the 'data' dictionary using the highest protocol available.
    #    survey_directories = pickle.loads(f, pickle.HIGHEST_PROTOCOL)
    # with open('survey_files.pickle', 'r') as f:
    #    # Pickle the 'data' dictionary using the highest protocol available.
    #    survey_files = pickle.load(f, pickle.HIGHEST_PROTOCOL)
    with open('survey_trip_to_sort.pickle', 'rb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        survey_trip_to_sort = pickle.load(f, encoding="UTF-8")
        # Survey files for each survey write SurveyCleaning object then add to Heritage Survey
        # for h_survey, cleaning_files in survey_files.items():
        #    add_files = []
        #    if cleaning_file[0] in ('Photo', 'Directory'):
        #        continue
        #    for cleaning_file in cleaning_files:
        #        sc, created = SurveyCleaning.objects.get_or_create(path_type=pt[cleaning_file[0]], data_path=cleaning_file[1])
        #        add_files.append(sc)
        #    h_survey.data_source.add(*add_files)
    #
    ## Do the same thing for our survey directories
    # for h_survey, cleaning_files in survey_directories.items():
    #    add_files = []
    #    if cleaning_file[0] in ('Photo', 'Directory'):
    #        continue
    #    for cleaning_file in cleaning_files:
    #        sc, created = SurveyCleaning.objects.get_or_create(path_type=pt[cleaning_file[0]], data_path=cleaning_file[1])
    #        add_files.append(sc)
    #    h_survey.data_source.add(*add_files)

    # For survey trips and other stuff I think writing to our other tables
    for ht_survey, cleaning_files in survey_trip_to_sort.items():
        for cleaning_file in cleaning_files:
            stc, created = SurveyTripCleaning.objects.get_or_create(survey_trip=ht_survey,
                                                                    path_type=pt[cleaning_file[0]],
                                                                    data_path=cleaning_file[1])


if __name__ == '__main__':
    print("Running Survey analysis")
    main()
    print("Completed Anaylsis")

# Search drives G, Q, H, Z  for directories that match a new survey id or old
# Probably should just use regular expression for each
# re = (surveyid|survey_orig|related_code)
# Original NUMBERS
# {'Reports': 6450,
# 'Photos No Match': 24552,
# 'Photos': 5426,
# 'Survey Directories': 38962,
# 'Reports No Match': 6326,
# 'Spatial Files No Match': 1574,
# 'Spatial Files': 3470}
# Survey Directories with no spatial files 319
# Matched up surveys 940
# Survey Trips with Unclear survey match 1056
# HeritageSurvey.objects.all():
