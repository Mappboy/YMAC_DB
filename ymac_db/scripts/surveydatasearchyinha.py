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

DRIVES = [r'Z:', r'G:', r'Q:', r'K:', ]
UPDATED_DRIVES = [r"Z:\Claim Groups\Yinhawangka\YHW handover\Missing folders (and reports from Z Drive)",
                  r"Z:\Claim Groups\Yinhawangka\YHW handover\Missing reports (from existing folders on Z Drive)",
                  r"Z:\Claim Groups\Yinhawangka\YHW handover\Multiple copies - Duplicates to archive",
                  r"Z:\Claim Groups\Yinhawangka\YHW handover\Unknown - need to figure out"]

CHECK_SURVEYS = [
    "YHW Sites in the Angelo River Area",
    "YHW004(A) Investigation of Area Proposed Development HI Paraburdoo",
    "YHW Proposed Fence Lines & Bores on Rocklea Station HI Paraburdoo",
    "YHW ARCH SITE RS00-01, ROCKLEA STATION, HI",
    "YHW005(A) (367-3) Rocklea",
    "YHW WESTERN PANHANDLE EXPLORATION AREA, ROCKLEA HI",
    "YHW WEST ANGELAS PROJECT AREA",
    "367-6a Rocklea Exploration (E47-16)",
    "YHW WEST ANGELAS DRILLING & MINE INFRA AREAS NEAR NEWMAN",
    "YHW(A)016-1 Rocklea, Rocklea North, and Lagoon Pool Projects",
    "YHW005(A) (367-1) Rocklea Exploration (E47-16)",
    "INN092-3 ROCKLEA PASTROLAL LEASE E47952 and E471153",
    "YHW004(A) West Angelas A,B and E Deposits",
    "IBN132 Juna Downs Railway Prospect",
    "IBN132-1 JUNA DOWNS PASTORAL STATION",
    "INN074 (INN_001)",
    "INN074 Snowy Mountain",
    "INN074-1 Snowy Mountain",
    "INN085-6 Paraburdoo & Eastern Ranges tenements AML7004 & AML70246",
    "YHW MUDLARK WELL AND GURINBIDDY PROJECT",
    "YHW(A)016-1",
    "YHW007",
    "YHW018(B) DE SH2 Rockshelter",
    "YHW WEST ANGELAS MINE AND INFRASTRUCTURE DEVELOPMENT",
    "YHW018-38 Pilbara Iron West Angelas WAC Survey E471050, ML248SA, E471795,E47986, E522044, E47754, E521459, E47798",
    "YHW018-41 West Angelas Deposit B",
    "YHW029 (A)",
    "YHW(A)016 - Dragon E47_1024",
    "YHW(B)010-1",
    "YHW(B)010-1 Dragon E08_2210, E08_2211, E47_2417",
    "YHW004(A) West Angelas Deposits B & E",
    "YHW007A",
    "YHW015B",
    "YHW018_70_ETH_WAC",
    "YHW018-1 West Angelas Angelo River & Indabiddy Drilling",
    "YHW018-10",
    "YHW018-41 West Angelas Deposits B & E",
    "YHW018-56",
    "YHW018_74_ETH_SA_SID - Cancelled",
    "YHW018_89_ARC_SID (WA Arch Trip 8)",
    "YHW018_96_ETH_SA_SID (WA Ethno Trip 4) - Cancelled",
    "YHWB010_2_ARC_ETH_SID (Dragon Energy)",
    "YHWB031_2_ARC_ETH_WPC (NSR)",
    "YHW018_109_ETH_SA_SID - Cancelled",
    "YHW018_119_ARC_SV (GP Site Recording) - Postponed",
    "YHW018",
    "YHW004",
    "YHW004",
    "YHW018-02",
    "YHW018-01",
    "YHW018-03",
    "YHW004A",
    "YHW004A",
    "YHW018-04",
    "YHW018-05",
    "YHW016",
    "YHW018-06",
    "YHW012",
    "YHW018-10",
    "YHW018-11",
    "YHW018-13",
    "YHW018-16",
    "YHW005",
    "YHW018-15",
    "YHW018-C45",
    "YHW018-17",
    "YHW018-20",
    "YHW018-09",
    "YHW018-19",
    "YHW18-18",
    "YHW018-22",
    "120312 APISUR ",
    "YHW010-1",
    "YHW018-24 Group A",
    "YHW018-26",
    "YHW018-25",
    "YHW018-28",
    "YHW018-29",
    "YHW018-30",
    "YHW027",
    "YHW018-32",
    "YHW018-33",
    "YHW004-1",
    "YHW007",
    "YHW018-34",
    "YHW018-35",
    "YHW018-36",
    "YHW018-37",
    "YHW 028",
    "YHW018-39",
    "YHW018-40",
    "YHW PIC MONT",
    "YHW018-42",
    "YHW018-43",
    "YHW DNA",
    "YHW016-1A",
    "YHW032-1A",
    "YHW007-01",
    "YHW007-02",
    "YHW018-44",
    "YHW018-45",
    "YHW018-45",
    "YHW018-46",
    "YHW018-47",
    "YHW005-1",
    "YHW018-48",
    "YHW018-49",
    "YHW018-51",
    "YHW018-52",
    "YHW007-03",
    "YHW018-50",
    "YHW018-53",
    "YHW018-54",
    "YHW018-55",
    "YHW018-57",
    "YHW018-58",
    "YHW018-59",
    "YHW018-60",
    "YHW007-04",
    "YHW010-1B",
    "YHW018-61",
    "YHW018-62",
    "YHW018-62",
    "YHW018-63",
    "YHW018-64",
    "YHW007-05",
    "YHW007-06",
    "YHW018-65",
    "YHW018-66",
    "YHW018-67",
    "YHW007-07",
    "YHW018-68",
    "YHW018-69",
    "YHW018-70",
    "YHW018-70",
    "YHW018-71",
    "YHW005-2",
    "YHW005-2",
    "YHW018-73",
    "YHW018-75",
    "YHW007-08",
    "YHW018-72",
    "YHW018-76",
    "YHW018-78",
    "YHW018-77",
    "YHW018-78",
    "YHW018-79",
    "YHW018-81",
    "YHW007-09",
    "YHW018-80",
    "YHW018-81",
    "YHW018-82",
    "YHW031-1B",
    "YHW005-3",
    "YHW018-80",
    "YHW018-83",
    "YHW005-4",
    "YHW018-84",
    "YHW018-85",
    "YHW005-4",
    "YHW018-86",
    "YHW018-88",
    "YHW007-10",
    "YHW018-87",
    "YHW018-90",
    "YHW018-90",
    "YHW018-92",
    "YHW031-1B",
    "YHW005-3",
    "YHW007-11",
    "YHW018-93",
    "YHW018-94",
    "YHW018-95",
    "YHW005-3",
    "YHW018-81",
    "YHW031-1B",
    "YHW018-97",
    "YHW018-98",
    "YHW018-99",
    "YHW005-5",
    "YHW018-100",
    "YHW018-101",
    "YHW018-102",
    "YHW018-81",
    "YHW031-1B ",
    "YHW007-12",
    "YHW018-103",
    "YHW005-3",
    "YHW018-105",
    "YHW018-106",
    "YHW018-107",
    "YHW18-110",
    "YHW005-6",
    "YHW18-108",
    "YHW018-111",
    "YHW005-7",
    "YHW018-110",
    "YHW018-112",
    "YHW PIC SURVEY",
    "YHW007-13",
    "YHW018-113",
    "YHW007-14",
    "YHW018-104",
    "YHW018-114",
    "YHW018-116",
    "YHW018-115",
    "YHW018-117",
    "YHW018-118",
    "YHW18-118",
    "YHW018-21",
    "YHW018-120",
    "YHW018-121",
    "YHW018-122",
    "YHW018-123",
    "YHW018-124",
    "YHW018-125",
]
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


def check_surveys():
    found = 0
    not_found = []
    for survey in CHECK_SURVEYS:
        survey_qs = HeritageSurveyTrip.objects.filter(survey_id__contains=survey)
        orig_match = HeritageSurveyTrip.objects.filter(original_ymac_id__contains=survey)
        related_code = HeritageSurveyTrip.objects.filter(related_surveys__rel_survey_id__contains=survey)
        proj_name = HeritageSurvey.objects.filter(project_name__contains=survey)
        if survey_qs or orig_match or related_code or proj_name:
            found += 1
        else:
            not_found.append(survey)
            print("Could not find matching survey for %s" % survey)
    print("\n".join(not_found))
    print("Found %d out of %d " % (found, len(CHECK_SURVEYS)))


def print_claim_groups():
    sg = SurveyGroup.objects.all()
    print(sg)
    for g in sg:
        if g.group_name:
            print("(('{gid}', '{gname}'), '{gname}'),".format(gid=g.group_id, gname=g.group_name))
        else:
            print("(({gid}, {gid}), {gid}),".format(gid=g.group_id))


def intial_search():
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
    prelim = 0
    spatial_files_nomatch = 0
    photos_nomatch = 0
    reports_nomatch = 0

    max_dirs = 100
    search_dirs = 0
    # A dictionary of Heritage Survey and list of folders
    survey_directories = {}
    survey_trip_to_sort = {}
    survey_files = {}
    for drive in DRIVES:
        print("Started search drive %s" % drive)
        for dentry in rscandir(drive):
            match = survey_match.search(dentry.path)
            if match:
                surveys = find_survey(match.group())
                geofile = filesearch.search(dentry.name)
                # If we can't find a match this may return survey trips
                matched_hsurvey = filter_survey(surveys, match.group(), dentry)
                # Geo file and match
                if surveys and geofile and dentry.is_file():
                    # try save a SurveyCleaning item get id and then try to add each cleaning join up geofiles
                    # Make sure survey_trip_id is uniq first if not just take the first one
                    # Then save to heritage survey data source
                    _sort_results(matched_hsurvey, 'Spatial File', dentry, survey_directories, survey_trip_to_sort,
                                  survey_files)
                    search_dirs += 1
                    spatial_files += 1
                # Survey found and a directory
                elif surveys and dentry.is_dir():
                    # Other wise just save the root dir
                    print("Found a Survey Directory {}".format(dentry.name))
                    print(matched_hsurvey)
                    _sort_results(matched_hsurvey, 'Directory', dentry, survey_directories, survey_trip_to_sort,
                                  survey_files)
                    survey_dirs += 1
                # Report file and match
                elif surveys and dentry.is_file() and photosearch.search(dentry.name):
                    # Save out as photo to survey
                    _sort_results(matched_hsurvey, 'Photo', dentry, survey_directories, survey_trip_to_sort,
                                  survey_files)
                    photos += 1
                elif surveys and dentry.is_file() \
                        and reportsearch.search(dentry.name) \
                        and "report" in dentry.name.lower() \
                        and "draft" not in dentry.name.lower() \
                        and not dentry.name.startswith('~'):
                    _sort_results(matched_hsurvey, 'Survey Report', dentry, survey_directories, survey_trip_to_sort,
                                  survey_files)
                    reports += 1

                elif geofile:
                    # no survey found but found some spatial files write out to csv
                    PotentialSurvey.objects.create(survey_id=match.group(), data_path=dentry.path,
                                                   path_type='Spatial File')

                    spatial_files_nomatch += 1
                # No matchin survey potential survey with a report
                elif dentry.is_file() and reportsearch.search(dentry.name) \
                        and "report" in dentry.name.lower() and "draft" not in dentry.name.lower():
                    # no survey found but found a report file write to csv for later checking
                    PotentialSurvey.objects.create(survey_id=match.group(), data_path=dentry.path,
                                                   path_type='Survey Report')
                    reports_nomatch += 1
                elif dentry.is_file() and photosearch.search(dentry.name):
                    # no survey found but found a photos found write to csv for later checking
                    PotentialSurvey.objects.create(survey_id=match.group(), data_path=dentry.path, path_type='Photo')
                    photos_nomatch += 1

    for key in survey_files.keys():
        try:
            del survey_directories[key]
        except KeyError:
            continue
    counts = {'Spatial Files': spatial_files,
              'Survey Directories': survey_dirs,
              'Photos': photos,
              'Reports': reports,
              'Spatial Files No Match': spatial_files_nomatch,
              'Photos No Match': photos_nomatch,
              'Reports No Match': reports_nomatch}
    print(counts)
    print(len(survey_directories))
    print(len(survey_files))
    print(len(survey_trip_to_sort))
    t = {'Geofile': 'Spatial File',
         'Report': 'Survey Report',
         'Photo': 'Photo',
         'Directory': 'Directory'}
    with open('directories.pickle', 'r') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        survey_directories = pickle.loads(f, pickle.HIGHEST_PROTOCOL)
    with open('survey_files.pickle', 'r') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        survey_files = pickle.load(f, pickle.HIGHEST_PROTOCOL)
    with open('survey_trip_to_sort.pickle', 'rb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        survey_trip_to_sort = pickle.load(f, encoding="UTF-8")
    # Survey files for each survey write SurveyCleaning object then add to Heritage Survey
    for h_survey, cleaning_files in survey_files.items():
        add_files = []
        if cleaning_file[0] in ('Photo', 'Directory'):
            continue
        for cleaning_file in cleaning_files:
            sc, created = SurveyCleaning.objects.get_or_create(path_type=pt[cleaning_file[0]],
                                                               data_path=cleaning_file[1])
            add_files.append(sc)
        h_survey.data_source.add(*add_files)

    # Do the same thing for our survey directories
    for h_survey, cleaning_files in survey_directories.items():
        add_files = []
        if cleaning_file[0] in ('Photo', 'Directory'):
            continue
        for cleaning_file in cleaning_files:
            sc, created = SurveyCleaning.objects.get_or_create(path_type=pt[cleaning_file[0]],
                                                               data_path=cleaning_file[1])
            add_files.append(sc)
        h_survey.data_source.add(*add_files)

    # For survey trips and other stuff I think writing to our other tables
    for ht_survey, cleaning_files in survey_trip_to_sort.items():
        for cleaning_file in cleaning_files:
            SurveyTripCleaning.objects.create(survey_trip=ht_survey,
                                              path_type=pt[cleaning_file[0]],
                                              data_path=cleaning_file[1])


def prelim_search():
    """
    Searching preliminary advice file in directories where we have found something
    :return:
    """
    prelim = 0

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

    survey_directories = {}
    survey_trip_to_sort = {}
    survey_files = {}
    # Check current objects first
    # Need to figure out what to do for survey trips
    for qs in [SurveyCleaning.objects.all()]:
        for sc in qs:
            if not sc.data_path:
                continue
            _dir = sc.data_path if sc.path_type == "Directory" else os.path.dirname(sc.data_path)
            if "," in _dir:
                _dir = _dir.split(",")[0]
            if not _dir or not os.path.isdir(_dir):
                print("%s is not a directory" % _dir)
                continue
            try:
                for dentry in rscandir(_dir):
                    match = survey_match.search(dentry.path)
                    if match:
                        # If we can't find a match this may return survey trips

                        matched_hsurvey = sc.heritagesurvey_set.all()
                        # Geo file and match
                        if dentry.is_file() \
                                and reportsearch.search(dentry.name) \
                                and "prelim" in dentry.name.lower() \
                                and "draft" not in dentry.name.lower() \
                                and not dentry.name.startswith('~'):
                            _sort_results(matched_hsurvey, 'Prelim Advice', dentry, survey_directories,
                                          survey_trip_to_sort,
                                          survey_files)
                            prelim += 1
                            print(matched_hsurvey, dentry)
            except FileNotFoundError:
                continue
    print("Total found %d" % prelim)
    with open('survey_files_prelim.pickle', 'wb') as f:
        pickle.dump(survey_files, f, pickle.HIGHEST_PROTOCOL)
    add_files = []
    for h_survey, cleaning_files in survey_files.items():
        for cleaning_file in cleaning_files:
            sc, created = SurveyCleaning.objects.get_or_create(path_type=cleaning_file[0],
                                                               data_path=cleaning_file[1])
            add_files.append(sc)
        h_survey.data_source.add(*add_files)


if __name__ == '__main__':
    print("Running Survey analysis")
    prelim_search()
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
