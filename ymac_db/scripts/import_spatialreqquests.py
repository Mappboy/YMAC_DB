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


HEADER = ["Subject",
"Body",
"From: (Name)",
"From: (Address)",
"From: (Type)",
"To: (Name)",
"To: (Address)",
"To: (Type)",
"CC: (Name)",
"CC: (Address)",
"CC: (Type)",
"BCC: (Name)",
"BCC: (Address)",
"BCC: (Type)",
"Billing Information",
"Categories",
"Importance",
"Mileage",
"Sensitivity"]

process_emails_dir = "C:\Deleteme\process requests"
rqt = re.compile(r"Request Type\*?: (?P<request_type>(.*))", re.I)
reg = re.compile(r"Region\*?: (?P<region>(.*))", re.I)
cost_c = re.compile(r"Cost Centre\*?: (?P<cost_centre>(.*))", re.I)
claims = re.compile(r"Claims (if known): (?P<claim>(.*))", re.I)
deliv = re.compile(r"Delivery and/or Product Instructions\*?: (?P<delivery>(.*))",re.I)
job_re = re.compile(r"(?P<job_id>(J20\d+-\d+|(\d+)))")
m_sizes = re.compile(r"If a map please indicate size if known:(?P<map_size>(.*))", re.I)

job_dict = {}

def clean_delivery(deliv_type):
    options = [ "Digital only", "Digital and Hard Copy", "Other" ]
    for o in options:
        if o in deliv_type:
            return deliv_type[:len(o)]


def process_email(email_to_read):
    with open(os.path.join(process_emails_dir, email_to_read),'r') as open_email:
        reader = csv.DictReader(open_email, fieldnames=HEADER)
        for row in reader:
            job_id = job_re.search(row["Subject"])
            req = rqt.search(row["Body"])
            region = reg.search(row["Body"])
            cost_centre = cost_c.search(row["Body"])
            delivery = deliv.search(row["Body"])
            claim = claims.search(row["Body"])
            map_size = m_sizes.search(row["Body"])
            if not region or not job_id:
                continue
            jid = job_id.groupdict()['job_id']
            clean_deliv = clean_delivery(delivery.groupdict()['delivery'])
            clean_region = region.groupdict()['region'] if len(region.groupdict()['region']) <= len("Pilbara") else region.groupdict()['region'][:len("Pilbara")]
            clean_cost = "DPMC" if cost_centre.groupdict()['cost_centre'].startswith("DPMC") else cost_centre.groupdict()['cost_centre']
            if map_size:
                clean_map = map_size.groupdict()["map_size"] if map_size.groupdict()["map_size"].startswith("A") else None
            else:
                clean_map = None
            job_dict[jid] = [clean_region,
                             clean_cost,
                             clean_deliv,
                             clean_map]

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


def date_clean(date_to_clean):
    if not date_to_clean:
        return None
    formats = ["%d/%m/%Y","%Y-%m-%d %H:%M:%S"]
    cleaned_date = None
    for f in formats:
        try:
            cleaned_date = datetime.datetime.strptime(date_to_clean, f).strftime("%Y-%m-%d")
            break
        except ValueError:
            continue
    if not cleaned_date:
        return datetime.datetime.strptime(date_to_clean.split()[0], formats[0]).strftime("%Y-%m-%d")
    return cleaned_date

def main():
    # Set up job_dict
    # NOTE: This will remove all existing jobs be very very careful
    YMACSpatialRequest.objects.all().delete()
    for email_to_process in os.listdir(process_emails_dir):
        process_email(email_to_process)
    with open('X:\Projects\SpatialDatabase\spatial_requests_update.txt', 'r') as tsv:
        reader = csv.DictReader(tsv, delimiter="\t")
        for row in reader:
            user = get_user(row['Requested By'])
            rt = RequestType.objects.filter(name=row['Task Name'])
            if not rt:
                rt = RequestType.objects.filter(name='Uncertain')
            request_type = rt[0]
            claim = None
            job_desc = row['Job Description']
            job_control = row['Job Control #'][:len("JYYYY-CNO")]
            map_size = row['Map Size'].replace("Please select map size if applicable","").replace("Other (Please describe in Other Instructions","Other")
            sup_data_text = row['Supplementary Data']
            other_instructions = row["Comments"]
            priority = row["Prioity urgency"]
            _map = row['Map']
            data = row['Data']
            analysis = row['Analysis']
            other = row['Other']
            draft = row['Draft']
            done = row['Done']
            email_me_no = row['EmailMe #']
            cc_recipients = row['CC']
            required_by = date_clean(row['Due Date'])
            request_datetime = date_clean(row['Request Date'])
            completed_datetime = date_clean(row['Completed Date'])
            assigned_to = get_staff(row['Assigned To'])
            time_spent = row['Time (Hours) to Complete'] if row['Time (Hours) to Complete'] else 0.0
            region, cost_centres, delivery = [None] * 3
            if job_control in job_dict:
                region, cost_centres, delivery,clean_map = job_dict[job_control]
            if email_me_no in job_dict:
                region, cost_centres, delivery, clean_map = job_dict[email_me_no]
            if map_size:
                clean_map = map_size
            print(job_control, email_me_no, clean_map, required_by, request_datetime, completed_datetime, region, cost_centres, delivery)

            #print(user, request_type, claim, job_desc, job_control, map_size, sup_data_text, required_by, request_datetime,
            #      completed_datetime, other_instructions, priority, assigned_to, region, cost_centres, delivery)
            #                                  cc_recipients, product_type, other_instructions,
            #                                  cost_centre, proponent, priority, map, data, analysis,
            #                                  other, draft, done, assigned_to, time_spent, related_jobs)
            # Make sure user is not blank
            yr = YMACSpatialRequest.objects.update_or_create(user=user, request_type=request_type, region=region,
                                                  job_desc=job_desc,
                                                  job_control=job_control, map_size=clean_map, sup_data_text=sup_data_text,
                                                  required_by=required_by, request_datetime=request_datetime,
                                                  completed_datetime=completed_datetime, product_type=delivery, other_instructions=other_instructions,
                                                  cost_centre=cost_centres, proponent=None, priority=priority, map_requested=_map, data=data, analysis=analysis,
                                                  other=other, draft=draft, done=done, assigned_to=assigned_to, time_spent=time_spent)


if __name__ == '__main__':
    main()
