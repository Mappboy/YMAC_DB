import fnmatch
import os
import sys

import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

DRIVES = [r'Z:\Claim Groups\Yinhawangka\Heritage Surveys\\']
# Define our geofile types
GEOFILES = {"*.shp": "Shapefile",
            "*.shz": "Shapefile",
            "*.E00": "Shapefile",
            "*.gdb": "Geodatabase",
            "*.kml": "Google KML",
            "*.kmz": "Google KML",
            "*.tab": "MapInfo",
            "*.TAB": "MapInfo",
            "*.gpx": "GPX",
            "*.zip": "Zipped",
            }

GEO_EXT = {".shp": "Shapefile",
            ".shz": "Shapefile",
            ".E00": "Shapefile",
            ".gdb": "Geodatabase",
            ".kml": "Google KML",
            ".kmz": "Google KML",
            ".tab": "Mapinfo",
            ".TAB": "Mapinfo",
            ".zip": "Zipped",
            }

filesearch = re.compile("|".join([fnmatch.translate(ext) for ext in GEOFILES.keys()]))
survey_match = re.compile("[A-Z&]{3}\d{3}[-_]?(\d{1,5})?")


# Define our geofile types

def find_empty_dirs(path):
    count = []
    for direntry in rscandir(path):
        if direntry.is_dir() and not os.listdir(direntry.path):
            count.append(direntry)
    return count

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

def folder_search(base_path, search_path):
    """
    Returns a list of paths to search that are longer than the base path
    :param base_path:
    :param search_path:
    :return:
    """
    found_paths = []
    while not os.path.samefile(search_path, base_path) and search_path:
        search_path = os.path.split(search_path)[0]
        found_paths.append(search_path)
    return found_paths[:-2]


def main():
    # I think the best bet is to wait till the end of processing before saving.
    # If no file or files for a survey is found then just check if.
    # If we find a directory, we should check to see if it contains a PDF.
    # If it does record that. If not don't worry just save off the directory.


    spatial_files = 0

    claim_drive = os.path.normpath(DRIVES[0])
    total_files = 0
    all_geo_files = 0
    new_geofiles  = 0
    geofiles_survey = 0
    geofiles_no_survey = 0

    for direntry in rscandir(claim_drive):
        total_files +=1
        # Make sure it isn't already in our survey documents
        hs = None
        if filesearch.search(direntry.path) and not SurveyDocument.objects.filter(filename=direntry.name):
            all_geo_files +=1
            new_geofiles +=1
            ext = GEO_EXT[os.path.splitext(direntry.name)[1]]
            doc_type = DocumentType.objects.filter(sub_type=ext).first()
            if not doc_type:
                print(direntry.path, ext)
            assert doc_type
            for check_docs in folder_search(claim_drive, direntry.path):
                hs = HeritageSurvey.objects.filter(folder_location=check_docs).first()
                if hs:
                    break
            filepath, filename = os.path.split(direntry.path)
            if hs:
                geofiles_survey+=1
                sd, created = SurveyDocument.objects.get_or_create(document_type=doc_type, filepath=filepath, filename=filename)
                hs.documents.add(sd)
            else:
                geofiles_no_survey += 1
                sd, created = SurveyDocument.objects.get_or_create(document_type=doc_type, filepath=filepath, filename=filename)
        elif filesearch.search(direntry.path):
            all_geo_files+=1
    print("All Files {}\n Geofiles {} \nNew Geofiles {} \n "
            "Files with Survey {}\n Files no Survey {} \n ".format(total_files, all_geo_files, new_geofiles, geofiles_survey, geofiles_no_survey))

if __name__ == '__main__':
    print("Running Survey analysis")
    main()
    print("Completed Anaylsis")
