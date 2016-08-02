import csv
import os
import sys
import datetime
import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()
headings = ['id', 'user', 'request_type', 'region', 'Claim', 'Job Description', 'Job Control #', 'Map Size',
            'Supplementary Data', 'Sup File', 'Due Date', 'Request Date', 'Completed Date', 'CC', 'Product Type',
            'Comments', 'Cost centre', 'Proponent', 'Prioity urgency', 'Map', 'Data', 'Analysis', 'Other', 'Draft',
            'Done', 'Assigned To', 'Time (Hours) to Complete', 'Completion Time', 'Predecessors']

from ymac_db.models import *



def get_user(username):
    """
    Try's common lookups on RequestUser
    :param username: 
    :return: 
    """
    user = None
    name_lookups = {
        'Michael Meeghan': 'Michael Meegan',
        'New Person': 'Unknown',
        'MRaj@ymac.org.au': 'Michael Raj',
        'snalder@ymac.org.au': 'Sanna Nalder',
        'Dtaft@ymac.org.au': 'David Taft',
        'jkalpers@ymac.org.au': 'Jose Kalpers',
        'Cath McLeish': 'Catherine McLeish',
        'Catherine Mcleish': 'Catherine McLeish',
        'bashford@ymac.org.au': 'Unknown'
    }
    if len(username.split()) > 1:
        user = RequestUser.objects.filter(name=username)
    if len(username.split()) == 1:
        user = RequestUser.objects.filter(name__icontains=username)
    if username.strip() in name_lookups:
        user = RequestUser.objects.filter(name__icontains=name_lookups[username])
    if not user:
        user = RequestUser.objects.filter(name='Unknown')
    return user[0]

def get_staff(username):
    """
    Try's common lookups on YMAC Staff
    :param username:
    :return:
    """
    staff = None
    name_lookups = {
    }
    if not username:
        return YmacStaff.objects.filter(first_name__icontains='Clive')[0]
    if len(username.split()) > 1:
        staff = YmacStaff.objects.filter(full_name__icontains=username)
    else:
        staff = YmacStaff.objects.filter(first_name__icontains=username)
    return staff[0]
with open('X:\Projects\SpatialDatabase\spatial_requests2load.txt', 'r') as tsv:
    reader = csv.DictReader(tsv, delimiter="\t")
    for row in reader:
        user = get_user(row['user'])
        rt = RequestType.objects.filter(name=row['request_type'])
        if not rt:
            rt = RequestType.objects.filter(name='Uncertain')
        request_type = rt[0]
        claim = row['Claim']
        job_desc = row['Job Description']
        job_control = row['Job Control #']
        map_size = row['Map Size']
        sup_data_text = row['Supplementary Data']
        other_instructions = row["Comments"]
        priority = row["Prioity urgency"]
        map = row['Map']
        data = row['Data']
        analysis = row['Analysis']
        other = row['Other']
        draft = row['Draft']
        done = row['Draft']
        done = row['Done']
        required_by = datetime.datetime.strptime(row['Due Date'], "%d/%m/%y") if row['Due Date'] else None
        try:
            request_datetime = datetime.datetime.strptime(row['Request Date'], "%Y-%m-%d %H:%M:%S") if row['Request Date'] else None
        except ValueError:
            request_datetime = datetime.datetime.strptime(row['Request Date'].split()[0], "%d/%m/%Y")
        completed_datetime = datetime.datetime.strptime(row['Completed Date'], "%Y-%m-%d %H:%M:%S") if row['Completed Date'] else None
        assigned_to = get_staff(row['Assigned To'])
        print(assigned_to)
        #print(user, request_type, claim, job_desc, job_control, map_size, sup_data_text, required_by, request_datetime,
        #      completed_datetime, other_instructions, priority, assigned_to)
        #                                  cc_recipients, product_type, other_instructions,
        #                                  cost_centre, proponent, priority, map, data, analysis,
        #                                  other, draft, done, assigned_to, time_spent, related_jobs)
        # Make sure user is not blank
        # YMACSpatialRequest.objects.create(user, request_type, region, claim, job_desc,
        #                                  job_control, map_size, sup_data_text, sup_data_file,
        #                                  required_by, request_datetime, completed_datetime,
        #                                  cc_recipients, product_type, other_instructions,
        #                                  cost_centre, proponent, priority, map, data, analysis,
        #                                  other, draft, done, assigned_to, time_spent, related_jobs)
        #
