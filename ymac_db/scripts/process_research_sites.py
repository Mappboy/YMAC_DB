import csv
import re
from collections import Counter


def standardise_names(place_type, replacements):
    rep = dict((re.escape(k), v) for k, v in replacements.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], place_type)


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
            if not p:
                print(line)
            c[p] += 1
    print(c)

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
            if not p:
                print(place_types)
            c[p] += 1
    print(c)

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
        "fishing spot" : "fishing",
        "boundary marker": "boundary",
        "bounary":"boundary",
        "mythalogical":"mythological",
        "burial ground":"burial",
        "birth place":"birthplace",
        "arc site??":"archaeological",
        "arc site":"archaeological",
        "masacre site":"massacre site",
        "residence?":"residence"
    }
    for line in reader:
        place_types = site_type_clean(line, "Site Types", replacements, split_type=";", sublines=True)
        for p in place_types:
            if not p:
                print(place_types, line)
            c[p] += 1
    for e,c in c.items():
        print(e)

pkkp_site_replacement = {
"Historical": "Hist",
"Thalu": "Thalu",
"Burial": "Burial",
"Birth": "Birth",
"Living Water": "Yinta",
"Rock Art": "Art",
"Warlu": "Warlu",
"Rock hole": "RH",
"Other Mythological": "Myth",
"Archaelogical": "Arch",
"Ethno-geographic Feature": "Geo",
"Law Ground": "Law",
"Massacre Site": "Mass",
"Camping": "Camp",
"Boundary": "Bound",
"Unclassified General Ethnographic Significance": "Ethno",
"Cultural Objects": "Obj",
}