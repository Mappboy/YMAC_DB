import csv
import os
import sys

import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()
headings = ['id', 'user', 'request_type', 'region', 'Claim', 'Job Description', 'Job Control #', 'Map Size',
            'Supplementary Data', 'Sup File', 'Due Date', 'Request Date', 'Completed Date', 'CC', 'Product Type',
            'Comments', 'Cost centre', 'Proponent', 'Prioity urgency', 'Map', 'Data', 'Analysis', 'Other', 'Draft',
            'Done', 'Assigned To', 'Time (Hours) to Complete', 'Completion Time', 'Predecessors']

from ymac_db.models import *

with open('X:\Projects\SpatialDatabase\spatial_requests2load.txt', 'r') as tsv:
    reader = csv.Reader(tsv, delimiter="\t")
    for row in reader:
        user = RequestUser.objects.filter(name=row['user'])
        # Make sure user is not blank
        # YMACSpatialRequest.objects.create(user, request_type, region, claim, job_desc,
        #                                  job_control, map_size, sup_data_text, sup_data_file,
        #                                  required_by, request_datetime, completed_datetime,
        #                                  cc_recipients, product_type, other_instructions,
        #                                  cost_centre, proponent, priority, map, data, analysis,
        #                                  other, draft, done, assigned_to, time_spent, related_jobs)
        #
