import os
import sys
from zipfile import ZipFile

import django
from django.db.models import Q

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *

yinfile = r"Z:\Claim Groups\Yinhawangka\YHW handover\ymac_extract.zip"
newfile = r"Z:\Claim Groups\Yinhawangka\YHW handover\ymac_extract_update.zip"


def get_docs(yac_filter, doc_filters):
    for hs in HeritageSurvey.objects.filter(
            pk__in=[yc.survey.id for yc in YACReturn.objects.filter(Q(report=False) | Q(pa=False))]):
        docs = hs.documents.filter(
            Q(document_type__sub_type='Survey Report') | Q(document_type__sub_type='Preliminary Advice'))


def write_out_docs(docs, hs):
    for doc in docs:
        print(doc.filepath, doc.filename)
        print("{}/{}_Trip{}/{}".format(datetime.datetime.strftime(hs.date_from, "%Y"),
                                       hs.survey_id,
                                       hs.trip_number,
                                       doc.filename))


def read_written_files():
    found_files = {}
    with open(yinfile, "rb") as returnfile:
        with ZipFile(returnfile, 'r') as yinzip:
            for f in yinzip.namelist():
                year, survey, file = f.split("/")
                if survey in found_files:
                    found_files[survey].append(file)
                else:
                    found_files[survey] = [file]
    return found_files


def write_yin_zip_all():
    """
    Write everything in our documents table that are YHW OUT
    :return:
    """
    with open(yinfile, "wb") as returnfile:
        with ZipFile(returnfile, 'w') as yinzip:
            for sd in SurveyDocument.objects.filter(surveys__survey_group__group_id='YHW'):
                first_survey = sd.surveys.first()
                file2write = os.path.join(sd.filepath, sd.filename)
                if os.path.isfile(file2write):
                    yinzip.write(file2write,
                                 "{}/{}_Trip{}/{}".format(datetime.datetime.strftime(first_survey.date_from, "%Y"),
                                                          first_survey.survey_id,
                                                          first_survey.trip_number,
                                                          sd.filename))
                else:
                    print("Couldn't write %s" % file2write)


def write_yin_zip_update(already_zipped):
    """
    Write everything in our documents table that are YHW OUT
    :return:
    """
    with open(newfile, "wb") as returnfile:
        with ZipFile(returnfile, 'w') as yinzip:
            for sd in SurveyDocument.objects.filter(surveys__survey_group__group_id='YHW'):
                first_survey = sd.surveys.first()
                file2write = os.path.join(sd.filepath, sd.filename)
                survey_key = "{}_Trip{}".format(first_survey.survey_id,
                                                first_survey.trip_number)
                if os.path.isfile(file2write):
                    if survey_key not in already_zipped or sd.filename not in already_zipped[survey_key]:
                        yinzip.write(file2write, "{}/{}_Trip{}/{}".format(datetime.datetime.strftime(
                            first_survey.date_from, "%Y"),
                            first_survey.survey_id,
                            first_survey.trip_number,
                            sd.filename))
                        if sd.document_type.sub_type == "Survey Report":
                            YACReturn.objects.filter(survey=first_survey).update(report=True)
                        else:
                            YACReturn.objects.filter(survey=first_survey).update(pa=True)
                else:
                    print("File doesn't exist %s" % file2write)


def main():
    write_yin_zip_update(read_written_files())
    print("Finished you dilly")


if __name__ == '__main__':
    main()
