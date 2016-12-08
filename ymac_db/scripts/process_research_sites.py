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
    'GDA94': {"LL": 4283, "49": 28349, "50": 28350, '51': 28351, '52': 28352},
    'GDA 94': {"LL": 4283, "49": 28349, "50": 28350, '51': 28351, '52': 28352},
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


class SiteGeomCheck(object):
    def __init__(self, datasource, error_msg):
        self.datasource = DataSource(datasource)
        self.error_msg = error_msg
        self.geom = self.get_geom()

    def get_geom(self):
        if not self.datasource.layer_count == 1:
            raise Exception("More than one layer in filter check")
        return self.datasource[0][0].geom

    def intersects(self, geom_test):
        if type(geom_test) == django.contrib.gis.geos.polygon.Polygon:
            geom_test = OGRGeometry(geom_test.wkt)
        if type(geom_test) == django.contrib.gis.gdal.geometries.Polygon:
            if self.geom.intersects(geom_test):
                return True
            else:
                return False
        raise Exception("Bad geometry ... I think " + str(type(geom_test)))


def get_site(projection, easting, northing, filters=(), site_buffer=10):
    ct = CoordTransform(SpatialReference(projection), SpatialReference(GDA94))
    buf_point = Point(easting, northing, srid=projection).buffer(site_buffer)
    trans_geom = buf_point.transform(ct, True)
    if filters:
        for f in filters:
            if not f.intersects(trans_geom):
                raise OutsideWAError(f.error_msg)
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
        group_string = group_string.replace(r, ";")
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
    surnames = ["Finlay", "Alexander", "Patterson", "Dowton", "Daniels", "Wally's", "Lockyer", "Boona's", "Cosmo's",
                "Hayes", "Boona", "Wally", "Smirke", "Sampi", "Bobby", "Evans", "Cox", "James", "Parker"]
    replacements = ["\n", ";", ",", "."]
    full_names = []
    for r in replacements:
        raw_string = raw_string.replace(r, " ")
    names = raw_string.split(" ")
    if "&" in names and names.index("&") % 2 != 0:
        names[names.index("&")] = names[names.index("&") + 2]
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


class SiteRegister(object):
    def __init__(self, filesource, mappings, replacements, filters):
        self.filesource = filesource
        self.filters = filters
        self.replacements = replacements
        self.mappings = mappings

    def perform_checks(self):
        """
        Function to check file for things like bad informants or site_types
        :return:
        """
        pass

# Ngarlawangka
# replacements = {"art": "rock art",
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
#                     "nr": "not recorded",
#                     "mod tree": "modified"
#                      "claypan": geographic,
# }
# Change NLW groups To Ngarlawanka JUR/ To Jurrru YINH to Yin
# EAsting and northing strip mNE*
# Lookup and join DAA sites from Notes1 and

# with open(r"X:\Projects\SpatialDatabase\REsearchSites\naag_sites.txt", "r") as testfile:
#     site_names = []
#     claim_check = SiteGeomCheck(r"V:\Custodial\NativeTitle\Claims\Naaguja\Naaguja_ClaimArea.shp",
#                                 "Outside Claim Area")
#     wa_check = SiteGeomCheck(r"V:\NonCustodial\Admin\State Boundaries\WA_Boundary.shp", "Outside Claim WA")
#     filters = [claim_check, wa_check]
#     c = Counter()
#     reader = csv.DictReader(testfile, delimiter='\t')
#     for index, line in enumerate(reader):
#         db_informants = []
#         site_types = []
#         place_types = line["site_type"].split(",")
#         for p in place_types:
#             p = p.strip()
#             if p:
#                 site_types.append(SiteType.objects.get(site_classification=p))
#                 c[p] += 1
#         site_name = line["Name"]
#         alt_site_name = line[" Other Name"]
#         site_location_desc = line[" Type of Place "]
#         ethno_detail = line["Claimant Comments"]
#         informants = line["Claimants"]
#         informant_checked = informant_check(informants)
#         if informants:
#             [db_informants.append(SiteInformant.objects.get_or_create(name=inf)[0]) for inf in set(informant_checked) if inf]
#         date_string = line["Date"]
#         references = line["Reference:  Field Notes"]
#         orig_x_val = float(line["Easting"]) if line["Easting"] else None
#         orig_y_val = float(line["Northing"]) if line["Northing"] else None
#         buf = 10
#         proj = None
#         geom = None
#         if orig_y_val and orig_x_val:
#            datum = "GDA94"
#            zone = line["Zone"]
#            proj = get_projections(datum, zone)
#            try:
#                geom = get_site(proj, orig_x_val, orig_y_val, filters, 10)
#            except OutsideWAError as e:
#                # print(e.args)
#                # print(index, orig_x_val, orig_y_val, proj)
#                geom = get_site(proj, orig_x_val, orig_y_val)
#         claim_group = SurveyGroup.objects.get(group_id="NAA")
#         dates_found = re.findall(r"\d{1,2}\.\d{1,2}\.\d{2,4}", date_string)
#         cleaned_dates = date_parser(date_string) if date_string else None
#         date_strings = []
#         date_recorded = None
#         if cleaned_dates:
#             date_recorded = cleaned_dates[0]
#             for d in cleaned_dates:
#                 date_strings.append(d.strftime("%d/%m/%Y"))
#         raw_field_notes = references.replace(",", "\n")
#         field_notes = ""
#         # print(raw_field_notes, date_strings)
#         for f in zip_longest(date_strings, raw_field_notes.split("\n")):
#             if f[0] and f[1]:
#                 field_notes += " ".join(f) + "\n"
#             elif f[1]:
#                 field_notes += f[1]
#             elif f[0]:
#                 field_notes += f[0]
#         print(index, field_notes)
#         date_created = datetime.datetime.today()
#         created_by = SiteUser.objects.get(user_name="Cameron Poole")
#         rs, created = ResearchSite.objects.get_or_create(
#             site_name=site_name,
#             alt_site_name=alt_site_name,
#             site_label=site_name,
#             claim_groups=claim_group,
#             ethno_detail=ethno_detail,
#             site_location_desc=site_location_desc,
#             reference=raw_field_notes,
#             date_created=date_created,
#             date_recorded=date_recorded,
#             created_by=created_by,
#             orig_x_val=orig_x_val,
#             orig_y_val=orig_y_val,
#             buffer=buf,
#             capture_coord_sys=proj,
#             geom=geom
#         )
#         if site_types:
#             rs.site_type.add(*site_types)
#         if db_informants:
#             rs.informants.add(*db_informants)


# with open(r"X:\Projects\SpatialDatabase\REsearchSites\palkyu_sites.txt", "r") as testfile:  # # Clean up objects
#     ResearchSite.objects.filter(claim_groups__group_id="PAL").delete()
#     # NOTE: Nuukangunya 1 is missing, Warrapa is missing
#     inform_options = [
#         'Amy French',
#         'Brian Tucker',
#         'Bonny Tucker',
#         'Charlie Coppin',
#         'Cheryl Yuline',
#         'Colin Crusoe',
#         'David Milroy',
#         'David Stock',
#         'Florrie Sam',
#         'Fred Stream',
#         'Gordon Yuline',
#         'Johnson Taylor',
#         'Joseph Taylor',
#         'Kevin Stream',
#         'Lily Long',
#         'Phyllis French',
#         'Reggie Malana',
#         'Susie Stream',
#         'Suzie Yuline',
#         'Terry Jaffrey',
#         'Tommy Stream',
#         'Walter Stream',
#     ]
#
#     site_groups = {
#         'Blue Bar Pool': 'Bulamu',
#         'Cajuput Spring': 'Julimangu / Kalurru',
#         'Jatarrkanha': 'Julimangu / Kalurru',
#         'Jirrpayinya': 'Julimangu / Kalurru',
#         'Jitangamuna ': 'Julimangu / Kalurru',
#         'Jumpaku': 'Kaparrkurra',
#         'Jurakunya': 'Julimangu / Kalurru',
#         'Kaamalanha': 'Julimangu / Kalurru',
#         'Kalampanguninha 1': 'Julimangu / Kalurru',
#         'Kalampanguninha 2': 'Julimangu / Kalurru',
#         'Kalona': 'Julimangu / Kalurru',
#         'Kaparrkurra': 'Kaparrkurra',
#         'Kaparrkurra Law Ground 1': 'Kaparrkurra',
#         'Kaparrkurra Law Ground 2': 'Kaparrkurra',
#         'Kaparrkurra Rock Quarry': 'Kaparrkurra',
#         'Kuluminya': 'Kaparrkurra',
#         'Kunayinya': 'Julimangu / Kalurru',
#         'Kuntanpoona': 'Julimangu / Kalurru',
#         'Malganyjarra': 'Julimangu / Kalurru',
#         'Mantingunha': 'Julimangu / Kalurru',
#         'Mantingunha Law Ground 1': 'Julimangu / Kalurru',
#         'Mantingunha Law Ground 2': 'Julimangu / Kalurru',
#         'Minturrina': 'Julimangu / Kalurru',
#         'Minyminypa': 'Julimangu / Kalurru',
#         'Nullagine Engravings': 'Julimangu / Kalurru',
#         'Nullagine Graves': 'Julimangu / Kalurru',
#         'Nullagine rockhole': 'Julimangu / Kalurru',
#         'Panga': 'Julimangu / Kalurru',
#     }
#     for k, v in list(site_groups.items()):
#         site_groups[k.lower()] = v
#
#     site_ref = {
#         'Walapawalapa': 'JK notebook 5:131 *Estimated from claimants description',
#         'Jakatitinya': 'JK Notebook 3:68', 'Woodstock Law ground 1': "JK Notebook 3:79, O'Connor 1987:61",
#         'Haunted Hole': 'JK Notebook 1:82, 114. *Estimated from topographic map',
#         'Cajuput Spring': 'JK Notebook 1:108-10, 3:78, 89',
#         'Kaamalanha': 'JK Notebook 2:66, 120, 156, 3:88, 5:80',
#         'Karlkurlkah': "O'Connor 1987: fig 5, DIA 23039", 'Warlakanya': 'DIA 757',
#         'Murtuka': 'von Brandenstein 1973:104', 'Ngawuwankuranha': 'von Brandenstein 1973:104',
#         'Parla': 'JK Notebook 1:82, Notebook 3:2 *Estimated from topographic map',
#         'Ten Mile Springs': "O'Connor 1987:61", 'Kirdimaangu': 'von Brandenstein 1965:2',
#         'Waru Waru': "O'Connor 1987:58",
#         'Jirrpayinya': 'JK Notebook 2:62, 5:88-9. *Estimated from topographic map',
#         'Kuntinya': 'Radcliffe-Brown 1910-11:243/35-6; Personal communication with Neale.',
#         'Kurlkuny': 'Personal communication with Vachon and Pannell.',
#         'Manggalirrkura': 'von Brandenstein 1965:2',
#         'Jirrkunya': 'JK notebook 5:131-2. *Estimated from topographic map',
#         'Jupartaparta': 'JK Notebook 2:54, 84, photos', 'Kurrkantina': 'JK Notebook 1:90-2, 100, 4:56',
#         'Stoney Creek': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Boodalyerri Creek': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Murrangany': 'JK Notebook 1:86, 90 *Estimated from track',
#         'Chocolate Hill': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Kaparrkurra Law Ground 2': 'JK Notebook 3/79-80. *Estimated from topographic map',
#         'Marrinyia Spring': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Cloudbreak rain making site': '', 'Pirlinmuna': 'von Brandenstein 1973:104',
#         'Murrumurntunha': 'von Brandenstein 1973:104', 'Kulinha': 'JK Notebook 1:166, 3:82, 4:44',
#         'Wurrunyinya Pool': 'JK Notebook 2:140-1, 5:111-14, photos',
#         'Wakurrajanta': 'JK notebook 5:131-2 *Estimated from claimants description',
#         'Jurakunya': 'JK Notebook 1:102, 3:90 *Estimated from topographic map',
#         'Yikarunguna (P)': 'Palmer 1981:table 23.1', 'Wadra Rockhole': 'JK Notebook 1:106',
#         'Malina': 'As found in DIA website ID 11958',
#         'Pangapininya': 'JK notebook 2:68, 5:135 *Estimated from GPS take on Skull Springs Road',
#         'Black Range': 'JK Notebook 1:67-8, 82', 'Putharrina': 'Notebook 3:58',
#         'Blue Bar Pool 2': 'JK Notebook 5:83', 'Manga Manga': 'referred to in DIA site 757.',
#         'Kathuwakarta': 'JK Notebook 1:44, 84, 114, 126-8, 164-6, Notebook 3:2-3, Palmer 1981:B.40-1 (narratives 72 and 74)',
#         'Japukakinya': 'JK Notebook 3:68',
#         'Pillin Pallin 1': 'JK Notebook 1:104 *Estimated from topographic map',
#         'Peternannie Spring': 'JK Notebook 1:82-4, 100, 112 *Estimated from topogrpahic map',
#         'Baroona Hill': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Pillin Pallin 2': 'Dinkler and Wright / Big Island Research 2012:8', 'Yula': 'DIA 11959',
#         'Wurrunyinya reserve': 'JK Notebook 2:66, 110, 130, 5:77',
#         'Winpikanya': 'referred to in DIA record for site 757',
#         'W Spring': 'JK Notebook 1:48-52, photographs *Estimated from claimants description',
#         'Yipipi': "O'Connor 1987:40-1", 'Minguwirriwirri': '',
#         'Lirrka': 'JK notebook 5:135, 139-40 *Estimated from claimants description',
#         'Ngangykulpa': 'JK Notebook 3:87, 5:82, Personal communication with Neale.', "Women's site": '',
#         'Abydoss Homestead': 'JK Notebook 3: 44',
#         'Kaparrkurra': 'JK Notebook 1:44, 112, 116, 3:72. *Estimated from topographic map',
#         'Kalona': 'JK Notebook 1:106. *Estimated from topographic map', 'Pijangarramanya': 'JK Notebook 2:30-6',
#         'Hillside Law Ground': 'JK Notebook 1:112. *Estimated from topographic map',
#         'Tjiturtakuna': "O'Connor 1987:58", 'Poonawinti': 'JK Notebook 1:108',
#         'Nine Mile Petroglyphs': 'JK Notebook 1:118-124, photos.', 'Jatarrkanha': 'JK Notebook 2:68, 5:133',
#         'Yilmanypangu': 'JK Notebook 1:56', 'Wootiyana': 'JK Notebook 1:114, 4:18',
#         'Minturrina': 'JK Notebook 5:90', 'Kutayitayi': '', 'Nyirrpirringunta': '',
#         'Nullagine Binmal': 'DIA 11960 *Estimated from claimants description of Matingunya Law Ground 2',
#         'Horsewater': 'Palmer 1981:388',
#         'Kaparrkurra Law Ground 1': 'JK Notebook 3/79-80. *Estimated from topographic map',
#         'Kuluminya': 'JK Notebook 1:44, Teddy Allen affadavit p.83',
#         'Jitangamuna': 'JK Notebook 1:166, 3:82, 4:44',
#         'Wanarrangu': 'von Brandenstein 1973:104 *Estimated from Von Brandstein',
#         'Kalampanguninha 2': 'JK notebook 5:125-7', 'Pawara': '', 'Kuntanpoona': 'JK Notebook 1:108',
#         'Marana': 'Tindale 1974:241', 'Jawarta': '*Estimated from topographic map',
#         'Unnamed Hill': 'JK notebook 5:132-3', 'Kalampanguninha 1': 'JK Notebook 2:66, 152',
#         'Peternannie Pool': 'JK Notebook 1:82-4, 100, 112, 3:98', 'Kathuwakarrta Jila 1': '',
#         'Sandy Creek Law Ground': 'JK Notebook 1:46, photographs',
#         'Malganyjarra': 'JK Notebook 1:108-10, 3:78, 89; *Estimated from topographic map ',
#         'Wartirrpa': 'JK Notebook 5:85', 'Nullagine Graves': 'JK Notebook 1:86, 90',
#         'Walparti': 'JK Notebook 1:48-52, photographs *Estimated from track about 2Km to South',
#         'Kunayinya': 'JK Notebook 2:68, 152, JK notebook 5:130', 'Murriyanya': "O'Connor 1987:58",
#         'Pitunumanha': 'Personal communication with Vachon and Pannell.', 'Catjualana': "O'Connor 1987:61",
#         'Taiyana 2': "O'Connor 1987:xxxxx, DIA List",
#         'Pinnacle Hill': 'Personal communication with Vachon and Pannell . *Estimated from topographic map',
#         'Mantana': 'JK Notebook 1:114, 4:10',
#         'Panga': 'JK Notebook 1:102, 2:62, 3:94, 4:56, 60, 5:67, 76, 86, DIA 704, 11958 ',
#         'Ngurntimargu': 'von Brandenstein 1965:2', 'White Donkey Hill': 'DIA list', 'Jiturnpurrpa': '',
#         'Mutila': 'JK notebook 2:78-82',
#         'Euro Spring Sites': 'JK Notebook 1:114, 166, Notebook 3:5, 80-1, Morgan  2009:4-5, DIA list',
#         'Waliyakunha': 'JK Notebook 2:68, 148, JK Notebook 5:77, 81',
#         'Wati Gujarra 4': 'JK Notebook 2:78, photos', 'Parijannila': 'von Brandenstein 1973:104',
#         'Pitiyara': '', 'Coobinacoola': 'JK Notebook 1:90. * Estimated from topographic map',
#         'Wati Gujarra 5': 'JK Notebook 2:84-6, photos', 'Kurduwa': 'von Brandenstein 1973:106',
#         'Jinakalpi': 'JK Notebook 1:66. *Estimated from adjacent track',
#         'Twenty Six Mile / Black Range (Coolyia Creek) Junction': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Murrkurra': 'JK notebook 5:145 *Estimated from topographic map', 'Tambina': 'JK Notebook 3:78',
#         'Mantingunha Law Ground 1': 'JK Notebook 2:66, 98, 110, 140-44, 5:79, 115-120 photos *Estimated from claimants description',
#         'Woodstock Law ground 2': 'JK Notebook 3:79', 'Pukankarra': 'DIA List',
#         'Mt Rudall': 'JK Notebook 1:106 *Estimated from claimants description',
#         'Mikatungana': 'Palmer 1981:390',
#         'Pikurpa': "O'Connor 1987:60, DIA list *Estimated from topographic map",
#         'Wuruninya Law Ground': 'JK Notebook 2:140-1, 5:111-14, JK Notebook 5:115 *Estimated from claimants description',
#         'Kathuwakarrta Jila 2': '', 'White Springs': 'Notebook 3:74, 81, Palmer 1981:388',
#         'Wamerana': "DIA list, O'Connor 1987:62, Worms, E.A. 19xxx, 'Prehistoric Petroglyphs of the Upper Yule River, North-Western Australia'",
#         'White Quartz Hill': 'Notebook 3:75, 81', 'Three Jacks': 'JK notebook 5:131-2',
#         'Noreena Downs Law Ground': 'JK Notebook 2:92 *Estimated from topographic map',
#         'Shag Pool': 'JK Notebook 1:106', 'Rain making site': '', 'Mulyayiningunya': '',
#         'Tarra Tarra': "O'Connor 1987:fig 5, DIA 6656", 'Burial site': '',
#         'Yirrangkaji': 'JK Notebook 2:96, DIA site 6636, von Brandenstein 1973:104.',
#         'Punarra': 'JK notebook 5:145 *Estimated from topographic map',
#         'mantala 1': 'JK notebook 5:134 *Estimated from claimants description',
#         'Mantingunha Law Ground 2': 'JK Notebook 2:66, 98, 110, 140-44, 5:79, 115-120 photos *Estimated from claimants description',
#         'Jukurpunha': 'JK Notebook 2:40, 5:69, photos, Palmer 1981:B.42 (narratives M.76 and M.77), Dinkler and Wright / Big Island Research 2012:8.',
#         'Jumpaku': 'JK Notebook 1:46-7, photographs. *Estimated from topographic map',
#         'Pilarthanna': "O'Connor 1987:60, DIA list *Estimated from O'Connor and topographic map",
#         'Bullock Well': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Woodstock camp': 'JK Notebook 3:41, 44', 'Yarawarainya': "JK Notebook 3:46, photos, O'Connor 1987:58",
#         'Nullagine Engravings': 'JK Notebook 2:70, photos', 'Marnda Pandarranjba': 'von Brandenstein 1973:106',
#         'Thalana': 'JK Notebook 3:87, 5: 76, 90-1, 99-100', 'Malkurntanha': 'von Brandenstein 1973:104',
#         'mantala 2': 'JK notebook 5:134 *Estimated from claimants description', 'Warrapa': 'JK notebok 5:142-3',
#         'Wati Gujarra 3': 'JK Notebook 2:54, 76-82',
#         'Purrunya': 'JK Notebook 1:64, 5:145, Tindale genealogy 52.',
#         'Nuukangunya 1': 'JK notebook 2:78-82 *Estimated from claimants description',
#         'Cajuput Creek': 'DIA 11959', 'Pinga': 'JK notebook 5:136 *Estimated from claimants description',
#         'Ngaparnkajinha': 'von Brandenstein 1973:104',
#         'Milimpirrinha': 'JK Notebook 3:56, 4:22, Nyiyapari site map',
#         'Kaparrkurra Rock Quarry': 'JK Notebook 1:112. *Estimated from topographic map',
#         'Pulamu': 'JK Notebook 1:72 *Estimated from topographic map',
#         'Sandy Creek Petroglyph site': 'JK Notebook 1:52, photographs',
#         'Mantingunha': 'JK Notebook 2:132, 142-4, 5:79, 115-120, photos', 'Pirtilya': '',
#         'Pijinganya': 'JK notebook 5:135', 'Cajuput Creek Engravings': '',
#         'Punumalunha': 'JK Notebook 2:66, 152, 5:83, 123-5', 'Pulicunah': "O'Connor 1987:58",
#         'Cunmagnunna': 'DIA list',
#         'Pakarna': 'JK Notebook 1:124, 5:68; Personal communication with Vachon and Pannell',
#         'Warramarrana': "O'Connor 1987:60",
#         'Kurkangunya': 'JK Notebook 1:74, 3:94; Radclife-Brown 1910-11:243/35-6; Personal communication with Neale. Personal communication with Vachon and Pannell.',
#         'Muntayunmunna': "O'Connor 1987:56, 58 * Estimated from O'Connor and topographic map",
#         'Kurrajong Creek graves': 'JK Notebook 2:90, photos', 'Mandanaladji': 'Tindale 1974:239',
#         'Nullagine rockhole': 'JK Notebook 2:72 *Estimated from claimants description',
#         'Warrie station': 'Notebook 3:86 *Estimated from topographic map',
#         'Cooglegong Law Ground': 'JK Notebook 2:38.* Estimated from topographic map',
#         'Minyminypa': 'JK notebook 5: 87',
#         'Urju': 'Personal communication with  Vachon and Pannell. Check name with claimants.',
#         'Mumpalinya': 'David Milroy email 1.11.2012.', 'Nguruwana': 'von Brandenstein 1973:104',
#         'Pelican Pool': 'JK Notebook 1:82, 114 *Estimated from topographic map',
#         'Nuukangunya 2': 'JK Notebook 1:104, 2:54, 88', 'Kathuwakarrta Jila 3': '',
#         'Redmont Spring': 'Notebook 3:75, 81*Estimated from claimants description',
#         'Kulkakutjarra': "O'Connor 1987:61-2",
#         'Kakurka': "DIA 6655, O'Connor 1987:56, von Brandenstein 19xxx:432 (Narratives from North West of Western Australia: Ngarluma and Jindjparndi (copied at AIATSIS)). *Estimated from topographic map",
#         'Wilgie Tarlu': "O'Connor 1987:61", "Tommy Stream's Grave": 'Notebook 3:97',
#         'Munguliguru': 'Palmer 1981: Appendix B 39-41', 'Shaw River Law Ground': 'JK Notebook 1:112',
#         'Makarra': 'Dinkler and Wright / Big Island Research 2012:8',
#         'Tayaina 1': "JK Notebook 3:78, O'Connor 1987:60", 'Mitarrarra': 'JK Notebook 2:52',
#         'Coolbamunna': "O'Connor 1987:61"}
#
#     for k, v in list(site_ref.items()):
#         site_ref[k.lower()] = v
#     site_names = []
#     claim_check = SiteGeomCheck(r"V:\Custodial\NativeTitle\Claims\Palyku\Palyku_ClaimArea.shp",
#                                 "Outside Claim Area")
#     wa_check = SiteGeomCheck(r"V:\NonCustodial\Admin\State Boundaries\WA_Boundary.shp", "Outside Claim WA")
#     filters = [claim_check, wa_check]
#     c = Counter()
#     reader = csv.DictReader(testfile, delimiter='\t')
#     for index, line in enumerate(reader):
#         db_informants = []
#         site_types = []
#         db_groups = []
#         place_types = line["Site Types "].split(",")
#         for p in place_types:
#             p = p.strip()
#             if p:
#                 site_types.append(SiteType.objects.get(site_classification=p))
#                 c[p] += 1
#         site_number = int(line["Site No."].strip()) if line["Site No."].strip() else None
#         site_name = line["Site Name"]
#         site_group = site_groups[site_name.lower()] if site_name.lower() in site_groups else None
#         if site_group:
#             groups = group_check(site_group)
#             [db_groups.append(SiteGroup.objects.get_or_create(name=g)[0]) for g in groups]
#         reference = site_groups[site_name.lower()] if site_name.lower() in site_groups else None
#         alt_site_name = line["Alternative Name"]
#         if site_name in site_names:
#             print("Non unique site names")
#             break
#         site_names.append(site_name)
#         if not site_name:
#             print(" Finished line number ", index)
#             break
#         site_location_desc = line["Location and Description"]
#         ethno_detail = line["Ethnographic / Historical Significance"]
#         raw_field_notes = line["Sources"].strip() + reference if reference else line["Sources"].strip()
#         dates_found = re.findall(r"\d{1,2}\.\d{1,2}\.\d{2,4}", raw_field_notes)
#         if dates_found:
#             raw_field_notes = re.sub(r"\d{1,2}\.\d{1,2}\.\d{2,4}",
#                                      lambda x: datetime.datetime.strptime(x.group(0), "%d.%m.%Y").strftime("%d/%m/%Y"),
#                                      raw_field_notes)
#             date_recorded = datetime.datetime.strptime(dates_found[0], "%d.%m.%Y")
#         else:
#             date_recorded = None
#         # TODO IF dates found sub for better dates and set recorded
#         informants = [l for l in line["informants"].split(",") if l.strip()]
#         for i in inform_options:
#             if i and i in raw_field_notes:
#                 informants.append(i)
#         if informants:
#             [db_informants.append(SiteInformant.objects.get_or_create(name=inf)[0]) for inf in set(informants) if inf]
#         date_created = datetime.datetime.today()
#         created_by = SiteUser.objects.get(user_name="Cameron Poole")
#         orig_x_val = float(line["East"]) if line["East"] else None
#         orig_y_val = float(line["North"]) if line["North"] else None
#         coordinate_source = line["Coordinate Source"]
#         accuracy_located = line["Located"].lower().strip()
#         if accuracy_located and "est" in accuracy_located or "geoscience" in accuracy_located or "google" in accuracy_located:
#             location_accuracy = "Approximate"
#         elif accuracy_located and "visited" in accuracy_located or "daa" in accuracy_located:
#             location_accuracy = "Located"
#         else:
#             location_accuracy = "Unknown"
#         buf = 10
#         proj = None
#         geom = None
#         if orig_y_val and orig_x_val:
#             datum = "GDA94"
#             zone = line["Zone"]
#             proj = get_projections(datum, zone)
#             try:
#                 geom = get_site(proj, orig_x_val, orig_y_val, filters, 10)
#             except OutsideWAError as e:
#                 # print(e.args)
#                 # print(index, orig_x_val, orig_y_val, proj)
#                 geom = get_site(proj, orig_x_val, orig_y_val)
#         claim_group = SurveyGroup.objects.get(group_id="PAL")
#         rs, created = ResearchSite.objects.get_or_create(
#             site_name=site_name,
#             alt_site_name=alt_site_name,
#             site_label=site_name,
#             site_number=site_number,
#             claim_groups=claim_group,
#             ethno_detail=ethno_detail,
#             site_location_desc=site_location_desc,
#             reference=raw_field_notes,
#             date_created=date_created,
#             date_recorded=date_recorded,
#             created_by=created_by,
#             orig_x_val=orig_x_val,
#             orig_y_val=orig_y_val,
#             buffer=buf,
#             capture_coord_sys=proj,
#             coordinate_accuracy=location_accuracy,
#             coordinate_source=coordinate_source,
#             geom=geom
#         )
#         if site_types:
#             rs.site_type.add(*site_types)
#         if db_informants:
#             rs.informants.add(*db_informants)
#         if db_groups:
#             rs.site_groups.add(*db_groups)
#         rs.save()


# with open(r"X:\Projects\SpatialDatabase\REsearchSites\Nyiya_sites.txt", "r") as testfile:
#     # Clean up objects
#     ResearchSite.objects.filter(claim_groups__group_id="NYI").delete()
#     site_names = []
#     nyi_check = SiteGeomCheck(r"V:\Custodial\NativeTitle\Claims\Nyiyaparli\Nyiyaparli_ClaimArea.shp",
#                               "Outside Claim Area")
#     wa_check = SiteGeomCheck(r"V:\NonCustodial\Admin\State Boundaries\WA_Boundary.shp", "Outside Claim WA")
#     location_check = {
#         "yes": "Located",
#         "located": "Located",
#         "locate- nullagine": "Located",
#         "located imogen dexter fieldnotes": "Located",
#         "approx": "Approximate",
#         "position indicitvie": "Position Indicative",
#         "position indicative": "Position Indicative",
#         "not located": "Unknown",
#         "remotely map": "Unknown",
#         "nja site map?": "Unknown",
#     }
#     filters = [nyi_check, wa_check]
#     c = Counter()
#     reader = csv.DictReader(testfile, delimiter='\t')
#     for index, line in enumerate(reader):
#         informants = []
#         site_types = []
#         place_types = line["Site Type"].split(",")
#         for p in place_types:
#             p = p.strip()
#             if p:
#                 site_types.append(SiteType.objects.get(site_classification=p))
#                 c[p] += 1
#         site_number = line["Final Site No"] if line["Final Site No"] else line["Site No"]
#         site_number = int(site_number) if site_number.strip() else None
#         site_name = line["Place Name"]
#         if site_name in site_names:
#             print("Non unique site names")
#             break
#         site_names.append(site_name)
#         if not site_name:
#             print(" Finished line number ", index)
#             break
#         site_location_desc = line["Description"]
#         ethno_detail = line["Ethnographic Detail "]
#         raw_field_notes = line["Reference"].strip()
#         date_created = datetime.datetime.today()
#         created_by = SiteUser.objects.get(user_name="Cameron Poole")
#         orig_x_val = float(line["East"]) if line["East"] else None
#         orig_y_val = float(line["North"]) if line["North"] else None
#         notes = line["Notes"]
#         accuracy_located = line["Located "].lower().strip()
#         if accuracy_located and accuracy_located not in location_check:
#             print(accuracy_located)
#         if accuracy_located:
#             location_accuracy = location_check[accuracy_located]
#         else:
#             location_accuracy = "Unknown"
#         site_comments = line["Notes"]
#         buf = 10
#         proj = None
#         geom = None
#         if orig_y_val and orig_x_val:
#             datum = "GDA94"
#             zone = line["Map"]
#             proj = get_projections(datum, zone)
#             try:
#                 geom = get_site(proj, orig_x_val, orig_y_val, filters, 10)
#             except OutsideWAError as e:
#                 print(e.args)
#                 print(index, orig_x_val, orig_y_val, proj)
#                 geom = get_site(proj, orig_x_val, orig_y_val)
#         claim_group = SurveyGroup.objects.get(group_id="NYI")
#         rs, created = ResearchSite.objects.get_or_create(
#             site_name=site_name,
#             site_label=site_name,
#             site_number=site_number,
#             claim_groups=claim_group,
#             ethno_detail=ethno_detail,
#             site_comments=site_comments,
#             site_location_desc=site_location_desc,
#             reference=raw_field_notes,
#             date_created=date_created,
#             created_by=created_by,
#             orig_x_val=orig_x_val,
#             orig_y_val=orig_y_val,
#             buffer=buf,
#             capture_coord_sys=proj,
#             coordinate_accuracy=location_accuracy,
#             geom=geom
#         )
#         if site_types:
#             rs.site_type.add(*site_types)

# with open("X:\Projects\SpatialDatabase\REsearchSites\mal_sites.txt", "r") as testfile:
#     reader = csv.DictReader(testfile, delimiter='\t')
#     for index, line in enumerate(reader):
#         informants = []
#         claim_group = SurveyGroup.objects.get(group_id="MAL")
#         site_name = line["Name"]
#         if not site_name:
#                 print(" Finished line number ", index)
#                 break
#         inf_line = line["Informants"]
#         [informants.append(SiteInformant.objects.get(name=i)) for i in informant_check(inf_line)]
#         rs = ResearchSite.objects.get(site_name=site_name, claim_groups=claim_group)
#         if informants:
#             rs.informants.add(*informants)
#             rs.save()
#             print(index,  inf_line.strip(), informants)

# with open("X:\Projects\SpatialDatabase\REsearchSites\mal_sites.txt", "r") as testfile:
#     ds = DataSource(r"V:\Custodial\NativeTitle\Claims\Malgana\Malgana_ClaimArea.shp")
#     c = Counter()
#     replacements = {"camping": "camp",
#                     "foodsource": "food source",
#                     "fighting place": "fighting area",
#                     "namaed place": "named place",
#                     "watersouce": "watersource",
#                     "water source": "watersource",
#                     "fishing place": "fishing",
#                     "geographical feature": "geographical"
#                     }
#     reader = csv.DictReader(testfile, delimiter='\t')
#     for index, line in enumerate(reader):
#         informants = []
#         site_types = []
#         place_types = site_type_clean(line, ' placetype ', replacements)
#         for p in place_types:
#             site_types.append(SiteType.objects.get(site_classification=p))
#             c[p] += 1
#         site_number = line["Map Site ID"]
#         site_name = line["Name"]
#         if not site_name:
#             print(" Finished line number ", index)
#             break
#         alt_site_name = line[" Other Name "]
#         ethno_detail = line["Comments"]
#         [informants.append(SiteInformant.objects.get_or_create(name=i)[0]) for i in informant_check(line["Informants"])]
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
#         raw_field_notes = line["Reference"].replace(",", "\n")
#         field_notes = ""
#         # print(raw_field_notes, date_strings)
#         for f in zip_longest(date_strings, raw_field_notes.split("\n")):
#             if f[0] and f[1]:
#                 field_notes += " ".join(f) + "\n"
#             elif f[1]:
#                 field_notes += f[1]
#             elif f[0]:
#                 field_notes += f[0]
#         date_created = datetime.datetime.today()
#         created_by = SiteUser.objects.get(user_name="Cameron Poole")
#         orig_x_val = float(line["Easting"]) if line["Easting"] else None
#         orig_y_val = float(line["Northing"]) if line["Northing"] else None
#         notes = line["Notes"]
#         accuracy = "Unknown"
#         if "Approximate location" in notes:
#             notes = notes.replace("Approximate location", "")
#             accuracy = "Approximate"
#         buf = 10
#         proj = None
#         geom = None
#         if orig_y_val and orig_x_val:
#             datum = "GDA94"
#             zone = "49"
#             proj = get_projections(datum, zone)
#             try:
#                 geom = get_site(proj, orig_x_val, orig_y_val, ds[0][0].geom, 10)
#             except:
#                 geom = get_site(proj, orig_x_val, orig_y_val)
#         claim_group = SurveyGroup.objects.get(group_id="MAL")
#         rs, created = ResearchSite.objects.get_or_create(
#             site_name=site_name,
#             site_label=site_name,
#             alt_site_name=alt_site_name,
#             site_number=site_number,
#             claim_groups=claim_group,
#             ethno_detail=ethno_detail,
#             reference=field_notes.strip(),
#             date_created=date_created,
#             date_recorded=date_recorded,
#             created_by=created_by,
#             orig_x_val=orig_x_val,
#             orig_y_val=orig_y_val,
#             buffer=buf,
#             capture_coord_sys=proj,
#             coordinate_accuracy=accuracy,
#             geom=geom
#         )
#         if site_types:
#             rs.site_type.add(*site_types)
#         if informants:
#             rs.informants.add(*informants)

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
