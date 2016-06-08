from csv import DictReader, DictWriter
from operator import itemgetter, attrgetter
import datetime
import re

# This is sorted on start date which is important for comaprisons made later

MISSINGCODES = r'W:\Utility\SpatialDatabase\pythoninput.csv'
COMPLETECODES = r'W:\Utility\SpatialDatabase\complete_codes.csv'
OUTPUT = r'W:\Utility\SpatialDatabase\cleaned_codes.csv'

OUTPUTHEADER = [
    "trip_number",
    "primary_svy_name",
    "secondary_svy_names",
    "old_survey_code",  # s_code
    "region",  # Region
    "ymac_svy_name",
    "original_svy_name",  # file_ref_no
    "Survey_Type",
    "Survey_method",
    "sh_code",
    "project_name",
    "confirm",
    "start_date",
    "end_date",
    "days",
    "tenements",  # tennement_number
    "comp_code",
    "hd_desc",
    "con_code",
    "con_code2",
    "Name",
    "Name2",
    "con_addr1",
    "con_email",
    "con_name",
    "con2_con_addr1",
    "con2_con_email",
    "con2_con_name",
    "to_Name",
    "to_Num_of_TOs",
    "hn_note",
    "project_status",
    "Data Paths",
    'Cleaning comment'
]
# TODO: Remove extra commas from secondary_svy_names
# TODO: Make sure primary survey names have ints for end values
# TODO: Check in file_ref_no splits if any rows should be added to miss_reader
sec_sur = re.compile(r'\w{6}( |$)')

# Dictionary of code listings where code such as
# YHW001 : [ (endval,sdate,scode,tripnumber) ...]
# where end val is the integer of  YHW001-ENDVAL
code_lookup = {}
# Same but if we find that an endval = 1
# Then we will want to just use endval = 0 and increment tripnumber
found_lookups = {}

with open(MISSINGCODES, 'r') as csv_missing_codes_file, \
        open(COMPLETECODES, 'r') as csv_codes_file, open(OUTPUT, 'wb') as output:
    miss_reader = DictReader(csv_missing_codes_file)
    codes_reader = DictReader(csv_codes_file)
    csv_out = DictWriter(output, fieldnames=OUTPUTHEADER, dialect='excel', lineterminator='\r\n', )
    csv_out.writeheader()
    # Skip headers

    # Read in codes reader
    # WE should be writing these rows as we go along too
    for row in codes_reader:
        svyname = row["primary_svy_name"]
        claim_key = row["primary_svy_name"].split("-")[0]
        endval = int(row["primary_svy_name"].split("-")[1])
        sdate, scode, tripnumber = row["start_date"], row["s_code"], row["trip_number"]
        secondary_keys = [sec_key for sec_key in row["secondary_svy_names"].split(",") if sec_key]
        if claim_key not in code_lookup:
            code_lookup[claim_key] = [(endval, sdate, scode, tripnumber)]
        else:
            code_lookup[claim_key].append((endval, sdate, scode, tripnumber))
            code_lookup[claim_key].sort(key=itemgetter(0))
        if secondary_keys:
            for secondary in secondary_keys:
                sec_key = secondary.split("-")[0]
                sec_end = int(secondary.split("-")[1])
                if sec_key not in code_lookup:
                    code_lookup[sec_key] = [(sec_end, sdate, scode, tripnumber)]
                else:
                    code_lookup[sec_key].append((sec_end, sdate, scode, tripnumber))
                    code_lookup[sec_key].sort(key=itemgetter(0))
        row['old_survey_code'] = row['s_code']
        row['region'] = row['Region']
        row['original_svy_name'] = row['file_ref_no']
        row['tenements'] = row['tennement_number']
        row['primary_svy_name'] = "{}-{}".format(claim_key, endval)
        delfields = ['tennement_number',
                     '_matched_records',
                     'sps_code',
                     'file_ref_no',
                     'Region',
                     'exact__.startIndex',
                     'exact__.match',
                     's_code']
        for field in delfields:
            del row[field]
        csv_out.writerow(row)

    for row in miss_reader:
        claim_key = row["primary_svy_name"].split("-")[0]
        sdate, scode, tripnumber = row["start_date"], row["s_code"], row["trip_number"]
        secondary_keys = [sec_key for sec_key in row["secondary_svy_names"].split(",") if sec_key]
        if claim_key not in code_lookup:
            endval = 1
            code_lookup[claim_key] = [(endval, sdate, scode, tripnumber)]
        else:
            cmpend, cmpdate, cmpcode, comptrip = code_lookup[claim_key][0]
            if cmpdate:
                cmpdate = datetime.datetime.strptime(cmpdate, "%d/%m/%Y")
            if sdate:
                sdate = datetime.datetime.strptime(sdate, "%d/%m/%Y")
            # Just use zero and add to our found_lookup
            if cmpend > 1 and scode < cmpcode:
                endval = cmpend - 1
                if type(sdate) == datetime.datetime:
                    sdate = sdate.strftime("%d/%m/%Y")
                code_lookup[claim_key].append((endval, sdate, scode, tripnumber))
            elif cmpend > 1 and cmpdate and sdate and (sdate < cmpdate):
                endval = cmpend - 1
                if type(sdate) == datetime.datetime:
                    sdate = sdate.strftime("%d/%m/%Y")
                code_lookup[claim_key].append((endval, sdate, scode, tripnumber))
            elif cmpend == 1 and claim_key not in found_lookups:
                endval = 0
                if type(sdate) == datetime.datetime:
                    sdate = sdate.strftime("%d/%m/%Y")
                found_lookups[claim_key] = [(endval, sdate, scode, tripnumber)]
            elif cmpend == 1 and claim_key in found_lookups:
                endval = 0
                lasttrip = sorted(set(found_lookups[claim_key]), key=itemgetter(3))[-1]
                if lasttrip[2] < scode:
                    tripnumber = int(lasttrip[3]) + 1
                if type(sdate) == datetime.datetime:
                    sdate = sdate.strftime("%d/%m/%Y")
                found_lookups[claim_key].append((endval, sdate, scode, tripnumber))
            else:
                if claim_key not in found_lookups:
                    endval = 0
                    if type(sdate) == datetime.datetime:
                        sdate = sdate.strftime("%d/%m/%Y")
                    found_lookups[claim_key] = [(endval, sdate, scode, tripnumber)]
                else:
                    endval = 0
                    lasttrip = sorted(set(found_lookups[claim_key]), key=itemgetter(3))[-1]
                    if lasttrip[2] < scode:
                        tripnumber = int(lasttrip[3]) + 1
                    if type(sdate) == datetime.datetime:
                        sdate = sdate.strftime("%d/%m/%Y")
                    found_lookups[claim_key].append((endval, sdate, scode, tripnumber))
        row['primary_svy_name'] = "{}-{}".format(claim_key, endval)
        row['trip_number'] = tripnumber
        # Should just be able to write correct value out here
        cleaned_keys = []
        if secondary_keys:
            for sec_key in secondary_keys:
                if sec_key not in code_lookup:
                    sec_end = 1
                else:
                    sec_end = 0
                cleaned_keys.append("{}-{}".format(sec_key, sec_end))
            row['secondary_svy_names'] = ",".join(cleaned_keys)
        row['old_survey_code'] = row['s_code']
        row['region'] = row['Region']
        row['original_svy_name'] = row['file_ref_no']
        row['tenements'] = row['tennement_number']
        delfields = ['tennement_number',
                     '_matched_records',
                     'sps_code',
                     'file_ref_no',
                     'Region',
                     'exact__.startIndex',
                     'exact__.match',
                     's_code']
        for field in delfields:
            del row[field]
        csv_out.writerow(row)
