import fnmatch
import os
import pickle
import re
import sys

import django

# Loading in HSIF and PA
sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

DRIVES = [r'Z:', r'G:', r'Q:', r'K:', ]

# Define our geofile types
REPORTFILES = {
    "*.doc*": "Word Document",
    "*.pdf": "PDF FILE"
}
reportsearch = re.compile("|".join([fnmatch.translate(ext) for ext in REPORTFILES.keys()]))

survey_match = re.compile("[A-Z&]{3}\d{3}[-_]?(\d{1,5})?")
PA_RE = re.compile("|".join([fnmatch.translate(r"*\2. PA & Data - FINAL PDF VERSION ISSUED TO PROPONENT\*.pdf"),
                             fnmatch.translate(r"*\FINAL PA - PDF - ISSUED TO PROPONENT\*.pdf")]
                            )
                   )

def find_survey(survey_string):
    """
    Given a survey string from a path finds a matching Heritage Survey Trip
    :param survey_string:
    :return:
    """
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


def print_claim_groups():
    sg = SurveyGroup.objects.all()
    print(sg)
    for g in sg:
        if g.group_name:
            print("(('{gid}', '{gname}'), '{gname}'),".format(gid=g.group_id, gname=g.group_name))
        else:
            print("(({gid}, {gid}), {gid}),".format(gid=g.group_id))


def intial_search():
    """
    WTF Does this do
    :return:
    """

    # I think the best bet is to wait till the end of processing before saving.
    # If no file or files for a survey is found then just check if.
    # If we find a directory, we should check to see if it contains a PDF.
    # If it does record that. If not don't worry just save off the directory.

    def _sort_results(results, type_of_results, dir_entry, survey_trips, survey_files):
        for result in results:
            if type(result) == HeritageSurveyTrip:
                if result not in survey_trips:
                    survey_trips[result] = [(type_of_results, dir_entry.path)]
                else:
                    survey_trips[result].append((type_of_results, dir_entry.path))
            # Must be empty or Heritage Survey
            else:
                if result not in survey_files:
                    survey_files[result] = [(type_of_results, dir_entry.path)]
                else:
                    survey_files[result].append((type_of_results, dir_entry.path))

    hsif = 0
    prelim = 0

    max_dirs = 100
    search_dirs = 0
    # A dictionary of Heritage Survey and list of folders
    survey_trip_to_sort = {}
    survey_files = {}
    for drive in DRIVES:
        print("Started search drive %s" % drive)
        for dentry in rscandir(drive):
            match = survey_match.search(dentry.path)
            if match:
                surveys = find_survey(match.group())
                # If we can't find a match this may return survey trips
                matched_hsurvey = filter_survey(surveys, match.group(), dentry)
                # Geo file and match
                # Geo file and match
                if dentry.is_file() \
                    and reportsearch.search(dentry.name) \
                    and (("prelim" in dentry.name.lower() and "advice" in dentry.name.lower()) or
                             PA_RE.match(dentry.path)) \
                    and "draft" not in dentry.name.lower() \
                    and 'edit' not in dentry.path.lower() \
                    and not dentry.name.startswith('~'):
                    _sort_results(matched_hsurvey, 'Prelim Advice', dentry,
                                  survey_trip_to_sort,
                                  survey_files)
                    prelim += 1
                    print(matched_hsurvey, dentry.path)
                elif dentry.is_file() \
                    and reportsearch.search(dentry.name) \
                    and "hisf" in dentry.path.lower() \
                    and not dentry.name.startswith('~') \
                    and 'edit' not in dentry.path.lower() \
                    and not dentry.name.startswith('~'):
                    _sort_results(matched_hsurvey, 'HISF', dentry,
                                  survey_trip_to_sort,
                                  survey_files)
                    hsif += 1
                    print(matched_hsurvey, dentry.path)

    counts = {'Prelims': prelim,
              'HISF': hsif}

    # SAVE HISF As
    print(counts)
    print(len(survey_files))
    print(len(survey_trip_to_sort))
    t = {'Geofile': 'Spatial File',
         'Report': 'Survey Report',
         'Photo': 'Photo',
         'Directory': 'Directory'}
    print("Total found %d" % prelim)
    with open('survey_files_prelim.pickle', 'wb') as f:
        pickle.dump(survey_files, f, pickle.HIGHEST_PROTOCOL)
    with open('survey_trip_to_sort_prelim.pickle', 'wb') as f:
        pickle.dump(survey_trip_to_sort, f, pickle.HIGHEST_PROTOCOL)
    # Pickle the 'data' dictionary using the highest protocol available
    for h_survey, cleaning_files in survey_files.items():
        add_files = []
        for cleaning_file in cleaning_files:
            sc, created = SurveyCleaning.objects.get_or_create(path_type=cleaning_file[0],
                                                               data_path=cleaning_file[1])
            if created:
                add_files.append(sc)
        h_survey.data_source.add(*add_files)
    for ht_survey, cleaning_files in survey_trip_to_sort.items():
        for cleaning_file in cleaning_files:
            sc, created = SurveyTripCleaning.objects.get_or_create(survey_trip=ht_survey,
                                                                   path_type=cleaning_file[0],
                                                                   data_path=cleaning_file[1])

def run_pickles():
    survey_trip_to_sort = {}
    survey_files = {}
    with open('survey_files_prelim.pickle', 'rb') as f:
        survey_files = pickle.load(f, encoding="UTF-8")
    with open('survey_trip_to_sort_prelim.pickle', 'rb') as f:
        survey_trip_to_sort = pickle.load(f, encoding="UTF-8")
    # Pickle the 'data' dictionary using the highest protocol available
    for h_survey, cleaning_files in survey_files.items():
        add_files = []
        for cleaning_file in cleaning_files:
            sc, created = SurveyCleaning.objects.get_or_create(path_type=cleaning_file[0],
                                                               data_path=cleaning_file[1])
            if created:
                add_files.append(sc)
        h_survey.data_source.add(*add_files)
    for ht_survey, cleaning_files in survey_trip_to_sort.items():
        for cleaning_file in cleaning_files:
            try:
                sc, created = SurveyTripCleaning.objects.get_or_create(survey_trip=HeritageSurvey.objects.get(id=ht_survey.survey_trip_id),
                                                                   path_type=cleaning_file[0],
                                                                   data_path=cleaning_file[1])
            except:
                continue

if __name__ == '__main__':
    print("Running Survey analysis")
    #intial_search()
    run_pickles()
    print("Completed Anaylsis")
