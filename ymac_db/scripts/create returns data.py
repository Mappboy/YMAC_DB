import os
import re
import sys

import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import SurveyDocument, HeritageSurvey, YACReturn

YAC_RETURNS_FOLDER = r"Z:\Claim Groups\Yinhawangka\YHW handover\Yinhawnagka Return of Information 1"
survey_re = re.compile(r"(?P<year>\d{4})\\(?P<survey_id>\w{3}\d{3}-\d{1,3})_Trip(?P<tripnum>\d{1,2})\\(?P<file>(.*))")

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

def newReports():
    for yr in YACReturn.objects.filter(report=False):
        if yr.survey.first().documents.all():
            # Run original download yinhawangka
            print(yr.survey.first())


def createYACReturns():
    fails = 0
    suc = 0
    for entry in rscandir(YAC_RETURNS_FOLDER):
        match = survey_re.search(entry.path)
        if match:
            mdict = match.groupdict()
            doc = SurveyDocument.objects.filter(filename=mdict["file"]).first()
            survey_doc = HeritageSurvey.objects.filter(survey_id=mdict["survey_id"], trip_number=mdict["tripnum"]).first()
            if not doc and not survey_doc:
                # USE survey fallback and check for PA_FINAL in name
                print("Couldn't find {file}".format(file=mdict["file"]))
                fails+=1
                continue
            suc +=1
            if doc:
                survey = doc.surveys.first()
                pa = doc.document_type.sub_type == 'Preliminary Advice'
                report = doc.document_type.sub_type == 'Survey Report'
            else:
                survey = survey_doc
                pa = 'PA_FINAL' in mdict["file"]
                report = 'PA_FINAL' not in mdict["file"]
            print(survey, pa, report, mdict["file"])
            update_values = {}
            if pa:
                update_values["pa"] = pa
            if report:
                update_values["report"] = report
            YACReturn.objects.update_or_create(survey=survey, defaults=update_values)
    print("{} failed items {} succeeded items".format(fails, suc))

def main():
    newReports


if __name__ == '__main__':
    main()
