from surveydatasearch import *

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'
from django.conf import settings

django.setup()

# fp = 'Z:Archive & Sort\\KMAC\\Unsorted Files\\Claims\\Final Reports\\K&M048 WPIOP - Final Reports - Archaeology\\\\'
fp = r"Z:Archive & Sort\KMAC\Unsorted Files\Finance\\"
for dentry in os.scandir(fp):
    match = survey_match.search(dentry.path)
    if match:
        surveys = find_survey(match.group())
        if surveys and dentry.is_file() \
                and reportsearch.search(dentry.name) \
                and "report" in dentry.name.lower() \
                and "draft" not in dentry.name.lower() \
                and not dentry.name.startswith('~'):
            print("Possible report {}".format(dentry.path))
        print(surveys)
        found_survey = filter_survey(surveys, match.group(), dentry)
        print(found_survey)
