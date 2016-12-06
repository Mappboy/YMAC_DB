import csv
import re
from collections import Counter
import sys
import os
import django
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.contrib.gis.gdal import DataSource, OGRGeometry
from itertools import zip_longest

# Date field is date site was recorded go with earliest date provided
sys.path.append(r"C:\Users\cjpoole\Documents\GitHub\YMAC_DB\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

GDA94 = 4283

from ymac_db.models import *


class OutsideWAError(Exception):
    """When geometry doesn't intersect with WA area"""

projections = {
    'WGS84': {'LL': 4326, "49": 32749, "50": 32750, "51": 32751, "52": 32752},
    'GDA94': {"LL": 4283, "49": 28349, "50": 28350, 51: 28351, 52: 28352},
    'GDA 94': {"LL": 4283, "49": 28349, "50": 28350, 51: 28351, 52: 28352},
    "AGD84": {"LL": 4203, "49": 20349, "50": 20350, "51": 20351, "52": 20352},
    "AGD66": {"LL": 4202, "49": 20249, "50": 20250, "51": 20251, "52": 20252}
}


def standardise_names(place_type, replacements):
    rep = dict((re.escape(k), v) for k, v in replacements.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], place_type)


def get_projections(datum, zone):
    datum = datum if datum != "AMG" else "AGD84"
    datum = datum if datum != "MGA" else "GDA94"
    datum = datum if datum != "UTM" else "WGS84"
    zone = zone.lower().replace("k", "")
    return projections[datum][zone]


def get_site(projection, easting, northing, filter_against=None, site_buffer=10):
    ct = CoordTransform(SpatialReference(projection), SpatialReference(GDA94))
    buf_point = Point(easting, northing, srid=projection).buffer(site_buffer)
    trans_geom = buf_point.transform(ct, True)
    if not filter_against.intersects(OGRGeometry(trans_geom.wkt)):
        raise OutsideWAError("The geometry is outside the wa base area")
    return trans_geom


def site_type_clean(row, header, replacements, split_type="\n", sublines=False):
    """
    Clean site_type field
    :param row: Row to clean
    :param header: Header name for site_type
    :return: list of cleaned site names
    """
    raw_place = row[header]
    if sublines:
        raw_place = raw_place.replace("\n", split_type).replace(",", split_type)
    place_types = [standardise_names(p.lower().strip(), replacements) for p in raw_place.split(split_type) if p.strip()]
    return place_types


def group_check(group_string):
    replacements = ["\n", "/", "?", ","]
    for r in replacements:
        group_string = group_string.replace(r,";")
    groups = [l.strip() for l in group_string.split(";") if
              l.strip()]
    return set(groups)


def informant_check(informant_string):
    informants = [i.strip(" ") for i in
                  informant_string.replace("\n", ";").replace("\t", ";").replace("&", ";").replace("/", ";").replace(
                      ",", ";").split(";") if i.strip()]
    return set(informants)


def clean_site_name(raw_sitename):
    return raw_sitename.replace("\n", " ").strip(" ")


def clean_accuracy(raw_accuracy):
    cleaned_fields = []
    if "topo map" in raw_accuracy.lower():
        cleaned_fields.append("approximate")
    else:
        cleaned_fields.append("")
    cleaned_fields.append(raw_accuracy)
    return cleaned_fields


def extract_entities(text):
    import nltk
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text))):
        print(chunk)
            # if hasattr(chunk, 'node'):
            #     print(chunk.node, ' '.join(c[0] for c in chunk.leaves()))



def split_names(raw_string):
    surnames = ["Finlay","Alexander", "Patterson","Dowton", "Daniels", "Wally's", "Lockyer", "Boona's", "Cosmo's", "Hayes", "Boona", "Wally", "Smirke","Sampi", "Bobby", "Evans", "Cox","James", "Parker"]
    replacements = ["\n", ";", ",", "."]
    full_names = []
    for r in replacements:
        raw_string = raw_string.replace(r," ")
    names = raw_string.split(" ")
    if "&" in names and names.index("&") % 2 != 0:
        names[names.index("&")] = names[names.index("&")+2]
    prev_name = ""
    for name in names:
        if name.strip() in surnames:
            full_names.append(prev_name + " " + name
                              )
        else:
            prev_name = name
    return ";".join(full_names)


def date_parser(raw_dates):
    """
    Function for dealing with crap date keeping
    :param raw_dates:
    :return:
    """
    date_forms = [
        "%d.%m.%Y",
        "%d.%m.%y",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%B %Y"
    ]
    dates_parsed = []
    cleaned_date = None
    for line in raw_dates.split("\n"):
        for d in re.findall(r"(\d+-)?(\d+.\d+.\d+)|(\w+ \w+)|(\d+.\d+.\d+-\d+.\d+.\d+)", line):
            if d[0]:
                raw_start_day = d[0].strip("-")
                raw_end_date = d[1]
                start_date = None
                end_date = None
                for form in date_forms:
                    try:
                        end_date = datetime.datetime.strptime(raw_end_date, form)
                    except:
                        continue
                    if end_date:
                        start_date = datetime.datetime(end_date.year, end_date.month, int(raw_start_day))
                        break
                if not start_date or not end_date:
                    print(d, start_date, end_date)
                    return
                cleaned_date = (start_date, end_date)
            elif d[3]:
                raw_start_date, raw_end_date = d[4].split("-")
                start_date = None
                end_date = None
                for form in date_forms:
                    try:
                        end_date = datetime.datetime.strptime(raw_end_date, form)
                    except:
                        continue
                    if end_date:
                        start_date = datetime.datetime.strptime(raw_start_date, form)
                        break
                if not start_date or not end_date:
                    print(d, start_date, end_date)
                    return
                cleaned_date = (start_date, end_date)
            else:
                d = d[1] if d[1] else d[2]
                for form in date_forms:
                    try:
                        cleaned_date = datetime.datetime.strptime(d, form)
                    except:
                        continue
            if not cleaned_date:
                print(raw_dates)
            dates_parsed.append(cleaned_date)
    return dates_parsed


with open("X:\Projects\SpatialDatabase\REsearchSites\mal_sites.txt", "r") as testfile:
    c = Counter()
    replacements = {"camping": "camp",
                    "foodsource": "food source",
                    "fighting place": "fighting area",
                    "namaed place": "named place",
                    "watersouce": "watersource",
                    "water source": "watersource",
                    "fishing place": "fishing",
                    "geographical feature": "geographical"
                    }
    reader = csv.DictReader(testfile, delimiter='\t')
    for line in reader:
        place_types = site_type_clean(line, "Type of Place", replacements)
        for p in place_types:
            SiteType.objects.get(site_classification=p)
            c[p] += 1

# with open("X:\Projects\SpatialDatabase\REsearchSites\km_sites.txt", "r") as testfile:
#     reader = csv.DictReader(testfile, delimiter='\t')
#     ds = DataSource(r"V:\NonCustodial\Admin\State Boundaries\WA_Boundary.shp")
#     replacements = {"art": "rock art",
#                     "hist": "historical",
#                     "war": "warlu",
#                     "wal": "warlu",
#                     "myth": "mythological",
#                     "cer": "ceremonial",
#                     "bir": "birthplace",
#                     "death": "death",
#                     "bur": "burial",
#                     "th": "thalu",
#                     "arch": "archaeological",
#                     "res": "resource",
#                     "camp": "camp",
#                     "geo": "ethno-geographical",
#                     "meet": "meeting place",
#                     "lw": "living water",
#                     "law": "law ground",
#                     "mas": "massacre site",
#                     "nr": "not recorded"}
#
#     bad_replacements = {"warlulu":"warlu", "historicalory":"historical"}
#     for line in reader:
#         db_groups = []
#         informants = []
#         site_types = []
#         ab_name = line["Aboriginal site name"]
#         eng_name = line["English site name"]
#         alt_site_name = None
#         if not ab_name and not eng_name:
#             break
#         elif ab_name and not eng_name:
#             site_name = ab_name
#         elif eng_name and not ab_name:
#             site_name = eng_name
#         else:
#             site_name = ab_name
#             alt_site_name = eng_name
#         site_number = int(line["Site No."]) if line["Site No."] else None
#         site_label = line["Label"]
#         ethno_detail = line["Notes"]
#         site_other_coordinates= line["Other sites"]
#         orig_x_val = float(line["Easting (UTM)"]) if line["Easting (UTM)"] else None
#         orig_y_val = float(line["Northing (UTM)"]) if line["Northing (UTM)"] else None
#         buf = 10
#         proj = None
#         if line["Datum"].startswith("MGA50"):
#             datum = "GDA94"
#             zone = "50"
#             proj = get_projections(datum,zone)
#             if orig_y_val and orig_x_val:
#                 geom = get_site(proj,orig_x_val,orig_y_val,ds[0][0].geom,10)
#         place_types = site_type_clean(line, "Site Type", replacements, split_type=" ")
#         for p in place_types:
#             p = p.strip()
#             if p in bad_replacements:
#                 p = bad_replacements[p]
#             try:
#                 site_types.append(SiteType.objects.get(site_classification=p))
#             except:
#                 print("Bad site type")
#             c[p] += 1
#         for g in group_check(line["Group(s)"]):
#             if g == "Robe River Kurrama":
#                 g = "Robe River Kurruma"
#                 #Get from database
#             db_groups.append(SiteGroup.objects.get_or_create(name=g)[0])
#         # rename Robe River Kurrama = Robe River Kurruma
#         [informants.append(SiteInformant.objects.get_or_create(name=i)[0]) for i in informant_check(split_names(line["Informants"]))]
#         cleaned_dates = date_parser(line["Date"]) if line["Date"] else None
#         date_strings = []
#         date_recorded = None
#         if cleaned_dates:
#             date_recorded = cleaned_dates[0]
#             for d in cleaned_dates:
#                 if type(d) == tuple:
#                     date_strings.append(d[0].strftime("%d/%m/%y") + "-" + d[1].strftime("%d/%m/%y"))
#                 else:
#                     date_strings.append(d.strftime("%d/%m/%Y"))
#         raw_field_notes = line["Reference"].replace(",","\n")
#         field_notes = ""
#         for f in zip_longest(date_strings, raw_field_notes.split("\n")):
#             if f[0] and f[1]:
#                 field_notes += " ".join(f) + "\n"
#             elif f[1]:
#                 field_notes += f[1]
#             elif f[0]:
#                 field_notes += f[0]
#         date_created = datetime.datetime.today()
#         created_by = SiteUser.objects.get(user_name="Cameron Poole")
#         claim_group = SurveyGroup.objects.get(group_id="K&M")
#         unnamed_site = False
#         if site_number in [174, 175, 195, 196]:
#             unnamed_site = True
#         rs, created = ResearchSite.objects.get_or_create(
#             site_name=site_name,
#             site_label=site_name,
#             alt_site_name=alt_site_name,
#             site_number=site_number,
#             claim_groups=claim_group,
#             ethno_detail=ethno_detail,
#             unnamed_site=unnamed_site,
#             reference=field_notes.strip(),
#             date_created=date_created,
#             date_recorded=date_recorded,
#             created_by=created_by,
#             orig_x_val=orig_x_val,
#             orig_y_val=orig_y_val,
#             buffer=buf,
#             capture_coord_sys=proj,
#             site_other_coordinates=site_other_coordinates,
#             geom=geom
#         )
#         if db_groups:
#             rs.site_groups.add(*db_groups)
#         if site_types:
#             rs.site_type.add(*site_types)
#         if informants:
#             rs.informants.add(*informants)
#
# # with open("X:\Projects\SpatialDatabase\REsearchSites\gnulli_sites.txt", "r") as testfile:
# #     reader = csv.DictReader(testfile, delimiter='\t')
# #     replacements = {
# #         "camp site": "camp",
# #         "camping": "camp",
# #         "foodsource": "food source",
# #         "fighting place": "fighting area",
# #         "namaed place": "named place",
# #         "watersouce": "watersource",
# #         "water source": "watersource",
# #         "fishing place": "fishing",
# #         "geographic feature": "geographical",
# #         "geographical feature": "geographical",
# #         "geographical feature???": "geographical",
# #         "camp ground": "camp",
# #         "food collection": "food source",
# #         "archaeological site": "archaeological",
# #         "archealogical": "archaeological",
# #         "archaelogical": "archaeological",
# #         "burial place": "burial",
# #         "burial site": "burial",
# #         "historical site": "historical",
# #         "fishing spot": "fishing",
# #         "fishing camp": "fishing",
# #         "boundary marker": "boundary",
# #         "bounary": "boundary",
# #         "mythalogical": "mythological",
# #         "burial ground": "burial",
# #         "birth place": "birthplace",
# #         "arc site??": "archaeological",
# #         "arc site": "archaeological",
# #         "masacre site": "massacre site",
# #         "residence?": "residence"
# #     }
# #     c = Counter()
# #     for line in reader:
# #         site_name = clean_site_name(line["NAME"])
# #         if not site_name:
# #             break
# #         site_types = []
# #         place_types = site_type_clean(line, "Site Types", replacements, split_type=";", sublines=True)
# #         for p in place_types:
# #             site_types.append(SiteType.objects.get(site_classification=p))
# #             if not p:
# #                 print(place_types, line)
# #         if not site_types:
# #             print("No types for ", site_name)
# #             break
# #         groups = [SiteGroup.objects.get_or_create(name=g.strip())[0] for g in group_check(line["Group"])]
# #         db_informs = [SiteInformant.objects.get_or_create(name=i.strip(" "))[0] for i in
# #                       informant_check(line["Informants"])]
# #         site_number = int(line["MAP SITE ID"]) if line["MAP SITE ID"] else None
# #         ethno_detail = line["Claimant Information"]
# #         alt_site_name = line["Other Name"]
# #         unnamed_site = False
# #         if line["Unnamed Site"]:
# #             c[site_name] += 1
# #             site_name = "{} {} {}".format(site_name, "Gnulli", c[site_name])
# #             unnamed_site = True
# #         # TODO Zip up reference Field Notes and date field
# #         #   - Take earliest date from date field as recorded date
# #         cleaned_dates = date_parser(line["Date"]) if line["Date"] else None
# #         date_strings = []
# #         date_recorded = None
# #         if cleaned_dates:
# #             date_recorded = cleaned_dates[0]
# #             for d in cleaned_dates:
# #                 if type(d) == tuple:
# #                     date_strings.append(d[0].strftime("%d/%m/%y") + "-" + d[1].strftime("%d/%m/%y"))
# #                 else:
# #                     date_strings.append(d.strftime("%d/%m/%Y"))
# #         raw_field_notes = line["Reference:  Field Notes"]
# #         field_notes = ""
# #         for f in zip(date_strings, raw_field_notes.split("\n")):
# #             field_notes += " ".join(f) + "\n"
# #         date_created = datetime.datetime.today()
# #         created_by = SiteUser.objects.get(user_name="Cameron Poole")
# #         if line["Easting / Longitude"] and line["Northing / Latitude"]:
# #             orig_x_val = float(line["Easting / Longitude"])
# #             orig_y_val = float(line["Northing / Latitude"])
# #             proj = get_projections(line["GPS Datum"], "50")
# #         else:
# #             orig_x_val = None
# #             orig_y_val = None
# #             proj = None
# #         if orig_x_val and orig_y_val:
# #             buf = 10
# #             geom = get_site(proj, orig_x_val, orig_y_val, buf)
# #         else:
# #             geom = None
# #             buf = 10
# #         coordinate_source = line["Source of Co-ordinates"]
# #         site_comments = line["Alistairs Notes / Internal comments"] + line["Comments"]
# #         coordinate_accuracy, site_location_desc = clean_accuracy(line["Accuracy of Location / Notes"])
# #         claim_group = SurveyGroup.objects.get(group_id="GNU")
# #
# #         rs, created = ResearchSite.objects.get_or_create(
# #             site_name=site_name,
# #             site_label=site_name,
# #             alt_site_name=alt_site_name,
# #             site_number=site_number,
# #             claim_groups=claim_group,
# #             site_comments=site_comments,
# #             ethno_detail=ethno_detail,
# #             unnamed_site=unnamed_site,
# #             reference=field_notes.strip(),
# #             date_created=date_created,
# #             created_by=created_by,
# #             orig_x_val=orig_x_val,
# #             orig_y_val=orig_y_val,
# #             buffer=buf,
# #             coordinate_accuracy=coordinate_accuracy,
# #             capture_coord_sys=proj,
# #             site_location_desc=site_location_desc,
# #             coordinate_source=coordinate_source,
# #             geom=geom
# #         )
# #         print(groups)
# #         if groups:
# #             rs.site_groups.add(*groups)
# #         if site_types:
# #             rs.site_type.add(*site_types)
# #         if db_informs:
# #             rs.informants.add(*db_informs)
#         # print(site_name,  site_number, ethno_detail,geom, coordinate_accuracy,site_location_desc, groups, db_informs, date_recorded, ,date_created,created_by)

# rs, created = ResearchSite.objects.update(
#         site_name=site_name,
#         site_label=site_name,
#         alt_site_name=alt_site_name,
#         orig_x_val=orig_x_val,
#         orig_y_val=orig_y_val,
#         buffer=buf,
#         capture_coord_sys=proj,
#         created_by=created_by,
#         date_created=date_created,
#         geom=geom
#     )
# except:
# map across  projection details
# create informants and site type
# with open("X:\Projects\SpatialDatabase\REsearchSites\pkkp_sites.txt", "r") as testfile:
#     reader = csv.DictReader(testfile, delimiter='\t')
#     pkkp_site_replacement = {
#         "hist": "historical",
#         "thalu": "thalu",
#         "bur": "burial",
#         "birth": "birthplace",
#         "brith": "birthplace",
#         "yinta": "living water",
#         "yinda": "living water",
#         "art": "rock art",
#         "warlu": "warlu",
#         "rh": "rock hole",
#         "myth": "mythological",
#         "arch": "archaeological",
#         "geo": "ethno-geographical",
#         "law": "law ground",
#         "mass": "massacre site",
#         "camp": "camp",
#         "bound": "boundary",
#         "ethno": "ethnographic",
#         "obj": "cultural objects",
#     }
#     all_informants = set()
#     lines = 0
#     for line in reader:
#         if line["RTIO Fieldsite [Spatial]"] or line["FMG ID [Spatial]"] or line["Survey Code"] or line[
#             "Layer Name"] == "PKKP_RRA" or not (any((line["Aboriginal site name"], line["English site name"]))):
#             continue
#         site_cols = ["Site Type 1", "Site Type 2", "Site Type 3"]
#         db_site_types = []
#         alt_site_name = None
#         if line["Aboriginal site name"] and line["English site name"]:
#             site_name = line["Aboriginal site name"]
#             alt_site_name = line["English site name"]
#         elif line["Aboriginal site name"] and not line["English site name"]:
#             site_name = line["Aboriginal site name"]
#         elif line["English site name"] and not line["Aboriginal site name"]:
#             site_name = line["English site name"]
#         else:
#             break
#         for sc in site_cols:
#             place_types = site_type_clean(line, sc, pkkp_site_replacement, split_type=";", sublines=False)
#             for p in place_types:
#                 try:
#                     db_site_types.append(SiteType.objects.get(site_classification=p))
#                 except:
#                     print("Bad ", p)
#                 if not p:
#                     print(place_types, line)
#                 c[p] += 1
#         informants = line["Informants"].replace("\n", ";").replace("/", ";").replace(",", ";").split(";")
#         db_informs = [SiteInformant.objects.get_or_create(name=i.strip(" "))[0] for i in informants if i]
#         buf = int(line["Required Buffer"].rstrip(" ").replace("m", "")) if line["Required Buffer"] else 10
#         if line["Easting "] and line["Northing "]:
#             orig_x_val = float(line["Easting "])
#             orig_y_val = float(line["Northing "])
#             proj = get_projections(line["Datum"], line["Map"])
#         else:
#             orig_x_val = None
#             orig_y_val = None
#             proj = None
#         if orig_x_val and orig_y_val:
#             geom = get_site(proj, orig_x_val, orig_y_val, buf)
#         else:
#             geom = None
#             buf = 10
#         site_comments = line["Notes 1"]
#         other_cords = line["Other Coordinates Recorded"]
#         date_created = datetime.datetime.today()
#         created_by = SiteUser.objects.get(user_name="Cameron Poole")
#         if line["Group(s)"]:
#             groups = [SiteGroup.objects.get(name=l.strip()) for l in line["Group(s)"].split("/") if l.strip() ]
#             rs = ResearchSite.objects.get(
#                                                     site_name=site_name,
#                                                     )
#             rs.site_groups.add(*groups)
#         #rs.site_type.add(*db_site_types)
#         #rs.informants.add(*db_informs)
#     print(c)
