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

# Extract folders
get_folder_re = re.compile(r"(?P<folder_path>Z:\\?Claim Groups\\(?P<claim_group>\w+)"
                           r"\\Heritage Surveys\\\d{4}\\)"
                           r"(?P<folder>[A-Za-z0-9_\- &\(\),.]+(\\))")

trip_re = re.compile(r"trip[ _\-]?(?P<trip_num>\d)", re.I)
matches = []
data_paths = set()
hs_dp = {}
for sc in SurveyCleaning.objects.all():
    if sc.data_path and sc.data_path not in data_paths and get_folder_re.search(sc.data_path):
        data_paths.add(sc.data_path)
        match = get_folder_re.match(sc.data_path)
        matches.append(sc)
        folder = match.groupdict()['folder']
        # print(match.groupdict())
        for hs in sc.heritagesurvey_set.all():
            if hs not in hs_dp:
                trip_match = trip_re.search(folder)
                if trip_match and hs.survey_trip.trip_number == int(trip_match.groupdict()['trip_num']):
                    hs_dp[hs] = folder
                    print("Assigning {} to {}".format(hs, folder))
                else:
                    hs_dp[hs] = folder
                    print("Assigning {} to {}".format(hs, folder))
            # We need to match on trips
            elif hs in hs_dp and hs_dp[hs] != folder:
                trip_match = trip_re.search(folder)
                if not trip_match and hs.survey_trip.trip_number == 1:
                    hs_dp[hs] = folder
                    print("Reassigning {} to {}".format(hs, folder))
                elif trip_match and hs.survey_trip.trip_number == int(trip_match.groupdict()['trip_num']):
                    hs_dp[hs] = folder
                    print("Reassigning {} to {}".format(hs, folder))
                else:
                    print("Differing data paths for {}: {} - {}".format(
                        hs, hs_dp[hs], folder
                    ))
            else:
                print("Skipping {}".format(hs))
