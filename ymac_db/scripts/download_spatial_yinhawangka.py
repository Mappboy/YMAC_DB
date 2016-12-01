import os
import sys
from zipfile import ZipFile

import django
from django.db.models import Q

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

yinfile = r"C:\Temp\ymac_saptial_extract.zip"

# Define our geofile types
geofiles = {".shp": "Shapefile",
            ".shz": "Zipped Shapefile",
            ".gdb": "ESRI Geodatabase",
            ".kml": "Google KML",
            ".kmz": "Google Zipped KML",
            ".tab": "MapInfo Tabfile",
            ".TAB": "MapInfo Tabfile",
            ".Tab": "MapInfo Tabfile",
            ".dwg": "Cadfile",
            ".gpx": "Garmin GPX",
            }

extra_files = {
    '.shp': [".ext", ".prj", ".cpg", ".shx", ".dbf", ".sbn"],
    ".TAB": [".DAT", ".MAP", ".ID", ".IND"],
}


def write_out_docs(docs, hs):
    for doc in docs:
        print(doc.filepath, doc.filename)
        print("{}/{}_Trip{}/{}".format(datetime.datetime.strftime(hs.date_from, "%Y"),
                                       hs.survey_id,
                                       hs.trip_number,
                                       doc.filename))


def update_documents():
    for survey in HeritageSurvey.objects.filter(survey_group__group_id='YHW', folder_location__isnull=False):
        if survey.folder_location and survey.survey_id != 'YHW007-9':
            for direntry in rscandir(survey.folder_location):
                filepath, filename = os.path.split(direntry.path)
                check = SurveyDocument.objects.filter(filepath=filepath, filename=filename)
                if direntry.is_file and os.path.splitext(direntry.name)[1] in geofiles.keys() and not check:
                    print(direntry.path)


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


def write_yin_zip_all():
    """
    Write everything in our documents table that are YHW OUT
    :return:
    """
    with open(yinfile, "wb") as returnfile:
        with ZipFile(returnfile, 'w') as yinzip:
            for sd in SurveyDocument.objects.filter(surveys__survey_group__group_id='YHW').filter(Q(document_type__document_type='Spatial')|Q(document_type__sub_type='Zipped')
                    ):
                surveys = sd.surveys.all()
                file2write = os.path.join(sd.filepath, sd.filename)
                for s in surveys:
                    folder_date = datetime.datetime.strftime(s.date_from, "%Y") if s.date_from else "unknown"
                    if os.path.isfile(file2write):
                        # find extra files for TAB or SHP files
                        file_prefix, file_ext = os.path.splitext(file2write)
                        if file_ext in extra_files:
                            for file_suffix in extra_files[file_ext]:
                                fpath = file_prefix + file_suffix
                                fname = os.path.split(file_prefix)[1] + file_suffix
                                if os.path.isfile(fpath):
                                    yinzip.write(fpath,
                                                 "{}/{}_Trip{}/{}/{}".format(folder_date,
                                                                             s.survey_id,
                                                                             s.trip_number,
                                                                             sd.file_status,
                                                                             fname))
                        yinzip.write(file2write,
                                         "{}/{}_Trip{}/{}/{}".format(folder_date,
                                                                     s.survey_id,
                                                                     s.trip_number,
                                                                     sd.file_status,
                                                                     sd.filename))

                    # deal with geodatabases
                    elif os.path.isdir(file2write):
                        for geop in rscandir(file2write):
                            yinzip.write(geop.path,
                                         "{}/{}_Trip{}/{}/{}/{}".format(folder_date,
                                                                        s.survey_id,
                                                                        s.trip_number,
                                                                        sd.file_status,
                                                                        sd.filename,
                                                                        geop.name))
                    else:
                        print("Couldn't write %s" % file2write)


def main():
    # update_documents()
    write_yin_zip_all()
    print("Finished you dilly")


if __name__ == '__main__':
    main()
