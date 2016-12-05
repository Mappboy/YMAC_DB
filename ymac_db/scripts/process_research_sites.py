import csv
import re
from collections import Counter
import sys
import os
import django
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.gdal import CoordTransform, SpatialReference

# Date field is date site was recorded go with earliest date provided
sys.path.append(r"C:\Users\cjpoole\Documents\GitHub\YMAC_DB\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

GDA94 = 4283

from ymac_db.models import *

projections = {
    'WGS84': {'LL': 4326, "49": 32749, "50": 32750, "51": 32751, "52": 32752},
    'GDA94': {"LL": 4283, "49": 28349, "50": 28350, 51: 28351, 52: 28352},
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


def get_site(projection, easting, northing, site_buffer=10):
    ct = CoordTransform(SpatialReference(projection), SpatialReference(GDA94))
    buf_point = Point(easting,northing, srid=projection).buffer(site_buffer)
    trans_geom = buf_point.transform(ct, True)
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
    groups = [l.strip() for l in group_string.replace("\n", ";").replace("/", ";").replace(",", ";").split(";")  if l.strip()]
    return set(groups)



def informant_check(informant_string):
    informants = [i.strip(" ") for i in informant_string.replace("\n", ";").replace("\t", ";").replace("&", ";").replace("/", ";").replace(",", ";").split(";") if i.strip()]
    return set(informants)

def clean_site_name(raw_sitename):
    return raw_sitename.replace("\n", " ").strip(" ")
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

with open("X:\Projects\SpatialDatabase\REsearchSites\km_sites.txt", "r") as testfile:
    reader = csv.DictReader(testfile, delimiter='\t')
    replacements = {"art": "rock art",
                    "hist": "historical",
                    "war": "warlu",
                    "wal": "warlu",
                    "myth": "mythological",
                    "cer": "ceremonial",
                    "bir": "birthplace",
                    "death": "death",
                    "bur": "burial",
                    "th": "thalu",
                    "arch": "archaeological",
                    "res": "resource",
                    "camp": "camp",
                    "geo": "ethno-geographical",
                    "meet": "meeting place",
                    "lw": "living water",
                    "law": "law ground",
                    "mas": "massacre site",
                    "nr": "not recorded"}
    for line in reader:
        place_types = site_type_clean(line, "Site Type", replacements, split_type=" ")
        for p in place_types:
            SiteType.objects.get(site_classification=p)
            c[p] += 1

with open("X:\Projects\SpatialDatabase\REsearchSites\gnulli_sites.txt", "r") as testfile:
    reader = csv.DictReader(testfile, delimiter='\t')
    replacements = {
        "camp site": "camp",
        "camping": "camp",
        "foodsource": "food source",
        "fighting place": "fighting area",
        "namaed place": "named place",
        "watersouce": "watersource",
        "water source": "watersource",
        "fishing place": "fishing",
        "geographic feature": "geographical",
        "geographical feature": "geographical",
        "geographical feature???": "geographical",
        "camp ground": "camp",
        "food collection": "food source",
        "archaeological site": "archaeological",
        "archealogical": "archaeological",
        "archaelogical": "archaeological",
        "burial place": "burial",
        "burial site": "burial",
        "historical site": "historical",
        "fishing spot": "fishing",
        "fishing camp": "fishing",
        "boundary marker": "boundary",
        "bounary": "boundary",
        "mythalogical": "mythological",
        "burial ground": "burial",
        "birth place": "birthplace",
        "arc site??": "archaeological",
        "arc site": "archaeological",
        "masacre site": "massacre site",
        "residence?": "residence"
    }
    c = Counter()
    for line in reader:
        site_name = clean_site_name(line["NAME"])
        if not site_name:
            break
        site_types = []
        place_types = site_type_clean(line, "Site Types", replacements, split_type=";", sublines=True)
        for p in place_types:
            try:
                site_types.append(SiteType.objects.get(site_classification=p))
            except:
                print(place_types)
            if not p:
                print(place_types, line)
        groups = [SiteGroup.objects.get_or_create(name=g.strip()) for g in group_check(line["Group"])]
        db_informs = [SiteInformant.objects.get_or_create(name=i.strip(" "))for i in informant_check(line["Informants"])]
        site_number = int(line["MAP SITE ID"]) if line["MAP SITE ID"] else None
        if line["Unnamed Site"]:
            c[site_name] +=1
            site_name = "{} {} {}".format(site_name,"Gnulli", c[site_name])
            site_label = site_name
        print(site_name, site_types, site_number, groups, db_informs)

#     rs, created = ResearchSite.objects.update(
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
