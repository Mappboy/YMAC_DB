import sys
import os
import django
import datetime

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *


staff_list = [
    {
        'email': "avolpe@ymac.org.au",
        'dept': "Research",
        'office': "Geraldton"
    },
    {
        'email': "avaughan@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "aohehir@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "acargill@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "ausher@ymac.org.au",
        'dept': "Research",
        'office': ""
    },
    {
        'email': "amgibbs@ymac.org.au",
        'dept': "Finance",
        'office': ""
    },
    {
        'email': "anoble@ymac.org.au",
        'dept': "Communications",
        'office': ""
    },
    {
        'email': "atoh@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "APrice@ymac.org.au",
        'dept': "Heritage",
        'office': "Geraldton"
    },
    {
        'email': "bfordyce@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "bstjames@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "cforsey@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "cjpoole@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "cpoustie@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "ctrees@ymac.org.au",
        'dept': "Legal",
        'office': "Geraldton"
    },
    {
        'email': "ccummings@ymac.org.au",
        'dept': "Research",
        'office': ""
    },
    {
        'email': "ctan@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "ccollins@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "cmckellar@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "cherrmann@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "CAllsop@ymac.org.au",
        'dept': "Research",
        'office': "Geraldton"
    },
    {
        'email': "DWells@ymac.org.au",
        'dept': "Legal",
        'office': "Geraldton"
    },
    {
        'email': "DFarrell@ymac.org.au",
        'dept': "Legal",
        'office': "Geraldton"
    },
    {
        'email': "dgarner@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "dtaft@ymac.org.au",
        'dept': "Legal",
        'office': "Geraldton"
    },
    {
        'email': "dnegi@ymac.org.au",
        'dept': "Finance",
        'office': "Perth"
    },
    {
        'email': "dfriedl@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "epilkington@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "elee@ymac.org.au",
        'dept': "Finance",
        'office': ""
    },
    {
        'email': "eharper@ymac.org.au",
        'dept': "Finance",
        'office': ""
    },
    {
        'email': "edecinque@ymac.org.au",
        'dept': "Other",
        'office': "Perth"
    },
    {
        'email': "gmcdevitt@ymac.org.au",
        'dept': "Heritage",
        'office': "Tom Price"
    },
    {
        'email': "godell@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "gyoung@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "hdaley@ymac.org.au",
        'dept': "Finance",
        'office': ""
    },
    {
        'email': "hcordell@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "idexter@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "joconnorveth@ymac.org.au",
        'dept': "Heritage",
        'office': "Tom Price"
    },
    {
        'email': "jelder@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "jpage@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "jharman@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "jjoo@ymac.org.au",
        'dept': "Finance",
        'office': "Perth"
    },
    {
        'email': "JKalpers@ymac.org.au",
        'dept': "Research",
        'office': "Geraldton"
    },
    {
        'email': "kjames@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "kholloman@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "krusskikh@ymac.org.au",
        'dept': "Finance",
        'office': "Perth"
    },
    {
        'email': "kbrewster@ymac.org.au",
        'dept': "Research",
        'office': ""
    },
    {
        'email': "KChalmers@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "lhillary@ymac.org.au",
        'dept': "Heritage",
        'office': "Geraldton"
    },
    {
        'email': "lalberghini@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "lgeddes@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "lkeepa@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "mchilala@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "mfort@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "mhealy@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "mmeegan@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "MRaj@ymac.org.au",
        'dept': "Legal",
        'office': ""
    },
    {
        'email': "nbielecki@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "nkimber@ymac.org.au",
        'dept': "Finance",
        'office': "Perth"
    },
    {
        'email': "ncolquhoun@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "onorris@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "rlawless@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "srosenfeld@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "srosenfeld@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "sbarnard@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "snalder@ymac.org.au",
        'dept': "Research",
        'office': ""
    },
    {
        'email': "sbell@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "scimetta@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "swilliamson@ymac.org.au",
        'dept': "Finance",
        'office': ""
    },
    {
        'email': "spiotrowski@ymac.org.au",
        'dept': "HeritageGeraldton",
        'office': "Perth"
    },
    {
        'email': "spashby@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "shawkins@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "smorgan@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "sclews@ymac.org.au",
        'dept': "Communications",
        'office': "Perth"
    },
    {
        'email': "tolliver@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "tnorwell@ymac.org.au",
        'dept': "Heritage",
        'office': "Pilbara"
    },
    {
        'email': "ZGonda@ymac.org.au",
        'dept': "Heritage",
        'office': "Perth"
    },
    {
        'email': "toneill@ymac.org.au",
        'dept': "Research",
        'office': "Perth"
    },
    {
        'email': "tcastro@ymac.org.au",
        'dept': "Finance",
        'office': "Perth"
    },
    {
        'email': "moosthuizen@ymac.org.au",
        'dept': "Finance",
        'office': "Perth"
    },
    {
        'email': "jwhiteaker@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
    {
        'email': "dcallan@ymac.org.au",
        'dept': "Finance",
        'office': "Perth"
    },
    {
        'email': "ccham@ymac.org.au",
        'dept': "Legal",
        'office': "Perth"
    },
]

users = [
    ("mkurubalan", " mkurubalan@ymac.org.au", " Merra", " Kurubalan"),
    ("mlucioli", " mlucioli@ymac.org.au", " Melissa", " Lucioli"),
    ("jgreene", " jgreene@ymac.org.au", " Jackie", " Greene"),
    ("edizon", " edizon@ymac.org.au", "Erika", " Dizon"),
    ("edecinque", " edecinque@ymac.org.au", "Ericka", " Decinque"),
    ("datan", " datan@ymac.org.au", " Daphne", " Tan"),
]

for user in users:
    added_user = False
    for user_dict in staff_list:
        if user[1].lower().strip() == user_dict['email'].lower().strip():
            try:
                print('Creating user {0}.'.format(user))
                adduser = RequestUser.objects.create(
                    name=user[2].strip() + user[3],
                    email=user[1].lower().strip(),
                    department=Department.objects.filter(name=user_dict['dept'])[0],
                    office=user_dict['office']
                )
                added_user = True
            except:
                print(
                'There was a problem creating the {0}.  {1}.' \
                    .format(user, sys.exc_info()[1]))
    if not added_user:
        print("Couldn't add user %s" % user[0])