import csv
import re
import sys
import os
from django.db.models import Q
import datetime
import django
import fnmatch

# Loading in HSIF and PA
sys.path.append(r"C:\Users\cjpoole\Documents\GitHub\YMAC_DB\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

DATE_CUT_OFF = datetime.datetime(2016, 7, 11)
# Define our geofile types
GEOFILES = {
    "*.shp": "Shapefile",
    "*.shz": "Zipped Shapefile",
    "*.gdb": "ESRI Geodatabase",
    "*.kml": "Google KML",
    "*.kmz": "Google Zipped KML",
    "*.tab": "MapInfo Tabfile",
    "*.TAB": "MapInfo Tabfile",
    "*.Tab": "MapInfo Tabfile",
    "*.dwg": "Cadfile",
    "*.gpx": "Garmin GPX",
}

GEOFILES_EXT = {
    ".shp": "Shapefile",
    ".shz": "Shapefile",
    ".gdb": "Geodatabase",
    ".kml": "Google KML",
    ".kmz": "Google KML",
    ".tab": "Mapinfo",
    ".TAB": "Mapinfo",
    ".Tab": "Mapinfo",
    ".gpx": "GPX",
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
PA_RE = re.compile("|".join([fnmatch.translate(r"*\2. PA & Data - FINAL PDF VERSION ISSUED TO PROPONENT\*.pdf"),
                             fnmatch.translate(r"*\FINAL PA - PDF - ISSUED TO PROPONENT\*.pdf")]
                            )
                   )


def rscandir(path):
    """
    Recursive scandir function
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


def get_trip_number(suvey_querset, orig_code, survey_start_date, survey_end_date):
    """
    Match up queries with survey date
    TODO: BLank dates in the database
    :param suvey_querset:
    :param survey_date:
    :return:
    """
    trip_number = 1
    match_trip = re.search(r"trip(\b)?(?P<trip_num>(\d))", orig_code, re.I)
    if match_trip:
        return int(match_trip.groupdict()['trip_num'])
    for survey in suvey_querset:
        if survey.date_from == survey_start_date or survey.date_to == survey_end_date or orig_code == survey.original_ymac_id:
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
    if not os.path.isdir(claim_folder):
        return
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


def get_proponent(prop_name):
    """
    Look up proponents etc
    :param prop_name:
    :return:
    """
    prop_names = {
        "Rio Tinto Iron Ore": "Rio Tinto",
        "Rio Tinto Exploration Pty Limited": "Rio Tinto",
        "Rio Tinto Iron Ore Pty Ltd": "Rio Tinto",
        "Metal Sands Ltd": "Metal Sands Pty Ltd",
        "FMG Ltd": "Fortescue Metals Group Ltd",
        "Fortescue Resources Pty Ltd & Ausquest Limited": "Fortescue Metals Group Ltd",
        "Fortescue Metals Group": "Fortescue Metals Group Ltd",
        "Doray Minerals": "Doray Minerals Limited",
        "Department of Agriculture and Food WA": "Department of Agriculture and Food",
        "Department of Parks of Wildlife": "Department of Parks and Wildlife",
        "Hancock Prospecting Pty Ltd & Hamersley Resources Ltd & Wright Prospecting Pty Ltd":
            "Hamersley Resources Ltd; Hancock Prospecting Pty Ltd; Wright Prospecting Pty Ltd",
        "Antipa Minerals": "Antipa Minerals Ltd",
        "Berkut Minerals Ltd": "Berkut Minerals Pty Ltd",
        "BHP Billiton Iron Ore Pty Ltd": "Bhp Billiton Minerals Pty Ltd",
        "Paladin Energy Minerals NL": "Paladin Energy Minerals Nl",
        "Sandfire Exploration Pty Ltd": "Sandfire Resources",
        "SIPA & Ashling Resources & Outtokumpu Zinc Australia": "Sipa Resources Ltd",
        "Platypus Minerals": "Platypus Minerals Ltd",
        "Sandfire Resources NL": "	Sandfire Resources Nl"

    }
    if prop_name in prop_names:
        prop_name = prop_names[prop_name]
    return Proponent.objects.filter(name=prop_name).first()


def check_folder_for_docs(folder_path, found_docs=[]):
    """
    Checks folder for any heritage documents or links existing documents up
    :param folder_path:
    :return:
    """
    if not folder_path or not os.path.isdir(folder_path):
        return
    for direntry in rscandir(folder_path):
        if reportsearch.search(direntry.name):
            if direntry.is_file() and "report" in direntry.name.lower() \
                    and "draft" not in direntry.name.lower() \
                    and "Checklist" not in direntry.path:
                found_docs.append((DocumentType.objects.get(sub_type="Survey Report"), direntry.path))
            elif direntry.is_file() and (("prelim" in direntry.name.lower() and "advice" in direntry.name.lower()) or
                                             PA_RE.match(direntry.path)) \
                    and "draft" not in direntry.name.lower() \
                    and 'edit' not in direntry.path.lower() \
                    and not direntry.name.startswith('~'):
                found_docs.append((DocumentType.objects.get(sub_type="Preliminary Advice"), direntry.path))
            elif direntry.is_file() \
                    and reportsearch.search(direntry.name) \
                    and "hisf" in direntry.path.lower() \
                    and not direntry.name.startswith('~') \
                    and 'edit' not in direntry.path.lower() \
                    and not direntry.name.startswith('~'):
                found_docs.append((DocumentType.objects.get(sub_type="HISF"), direntry.path))
        elif filesearch.search(direntry.name):
            if direntry.is_file():
                found_docs.append((DocumentType.objects.get(
                    sub_type=GEOFILES_EXT[os.path.splitext(direntry.path)[1]]), direntry.path))
    return found_docs


def add_pa_and_reports(pa_path, report_path):
    """
    Add any pa documents or report docs
    :param pa_path:
    :param report_path:
    :return:
    """
    found_files = []
    for path in [pa_path, report_path]:
        if not path or not os.path.isdir(path):
            continue
        for direntry in rscandir(path):
            if reportsearch.search(direntry.name):
                if direntry.is_file() and (("prelim" in direntry.name.lower() and "advice" in direntry.name.lower()) or
                                               PA_RE.match(direntry.path)) \
                        and "draft" not in direntry.name.lower() \
                        and 'edit' not in direntry.path.lower() \
                        and not direntry.name.startswith('~'):
                    found_files.append(("PA", direntry.path))
                elif direntry.is_file() and "report" in direntry.name.lower() and "draft" not in direntry.name.lower():
                    found_files.append(("Report", direntry.path))
    return found_files


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
            # if created_on <= DATE_CUT_OFF:
            #    break
            original_ymac_code = row['Survey Code']
            survey_code = get_clean_survey_code(original_ymac_code)
            # Just skip bad survey codes
            if survey_code is None:
                print("Bad survey code ", row['Survey Code'])
                continue
            start_date = datetime.datetime.strptime(row["Start Date"], "%d/%m/%y")
            end_date = datetime.datetime.strptime(row["Est End Date"], "%d/%m/%y")
            created_on = datetime.datetime.strptime(row["Created On"], "%d/%m/%y %H:%M %p")
            # Check trip numbers if start_date and end_date don't match then increment trip number or set as trip 1
            matching_codes = get_matching_surveys(survey_code)
            trip_number = 1
            if matching_codes:
                trip_number = get_trip_number(matching_codes, original_ymac_code, start_date, end_date)
            # check this doing the correct look ups
            create_user = row["Created By"] if row["Created By"] != 'Geidi VPN' else 'Cameron Poole'
            created_by = SiteUser.objects.filter(user_name=create_user).first()
            survey_group = get_claim_group(row["Claim Group"], survey_code)
            ymac_region = YmacRegion.objects.filter(geom__intersects=survey_group.geom.envelope)
            if len(ymac_region) == 2:
                ymac_region = "Both"
            else:
                ymac_region = ymac_region[0].name
            # If pa or report file path search for the relevant files
            survey_status = SurveyStatus.objects.get(status="Unknown")
            folder_location = find_survey_folder(survey_code, original_ymac_code, created_on, survey_group)
            proponent = get_proponent(row['Proponent'])
            methodologies = get_methodology([row["Survey Methodology"], row["Survey Methodology 2"]])
            project_status = row["Survey Status"]
            survey_type = get_survey_type(row["Survey Type 1"])
            survey_description = row['Survey Area']
            found_douments = add_pa_and_reports(row["PA File Path"], row["PA and Report File Path"])
            documents = check_folder_for_docs(folder_location, found_douments)
            # First we need to create documents
            if not proponent:
                print("Could not locate {} please update db".format(row['Proponent']))
            documents_to_add = []
            if documents:
                for add_doc in documents:
                    doc_type = add_doc[0]
                    doc_path, doc_name = os.path.split(add_doc[1])
                    if "Proponent" in doc_path:
                        status = SurveyStatus.objects.get(status="Proposed")
                    else:
                        status = SurveyStatus.objects.get(status="")
                    doc, doc_created = SurveyDocument.objects.get_or_create(
                        document_type=doc_type,
                        filepath=doc_path,
                        filename=doc_name,
                        file_status=status)
                    documents_to_add.append(doc)
            obj, created = HeritageSurvey.objects.get_or_create(
                survey_id=survey_code,
                trip_number=trip_number)
            obj.created_by = created_by
            obj.date_create = created_on
            obj.date_from = start_date
            obj.date_to = end_date
            obj.survey_group = survey_group
            obj.survey_region = ymac_region
            obj.survey_description = survey_description
            obj.folder_location = folder_location
            obj.proponent = proponent
            obj.project_status = project_status
            obj.data_status = survey_status
            obj.survey_type = survey_type
            obj.original_ymac_id = original_ymac_code
            obj.survey_methodologies.add(*methodologies)
            obj.documents.add(*documents_to_add)
    doctest.testmod()
