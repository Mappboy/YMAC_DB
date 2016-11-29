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

extra_files = {
    '.shp': [".ext", ".prj", ".cpg", ".shx", ".dbf", ".sbn"],
    ".tab": [".DAT", ".dat", ".map", ".MAP", ".id", ".id"],
    ".TAB": [".DAT", ".dat", ".map", ".MAP", ".id", ".id"],
}


def write_out_docs(docs, hs):
    for doc in docs:
        print(doc.filepath, doc.filename)
        print("{}/{}_Trip{}/{}".format(datetime.datetime.strftime(hs.date_from, "%Y"),
                                       hs.survey_id,
                                       hs.trip_number,
                                       doc.filename))

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
            for sd in SurveyDocument.objects.filter(surveys__survey_group__group_id='YHW').filter(document_type__document_type='Spatial'):
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
                                             "{}/{}_Trip{}/{}".format(folder_date,
                                                                      s.survey_id,
                                                                      s.trip_number,
                                                                      fname))
                        else:
                            yinzip.write(file2write,
                                     "{}/{}_Trip{}/{}".format(folder_date,
                                                              s.survey_id,
                                                              s.trip_number,
                                                              sd.filename))
                    # deal with geodatabases
                    elif os.path.isdir(file2write):
                        for geop in rscandir(file2write):
                            yinzip.write(geop.path,
                                         "{}/{}_Trip{}/{}/{}".format(folder_date,
                                                                  s.survey_id,
                                                                  s.trip_number,
                                                                  sd.filename,
                                                                     geop.name))
                    else:
                        print("Couldn't write %s" % file2write)




def main():
    write_yin_zip_all()
    print("Finished you dilly")


if __name__ == '__main__':
    main()
