import sys
import os
import django
import datetime

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()

from ymac_db.models import *


staff_list = [
    {'email': "avolpe@ymac.org.au",
     'dept': "Research",
     'office': "Geraldton"
     },

    {'email': "avaughan@ymac.org.au",
     'dept': "Research",
     'office': "Perth"
     },

    {'email': "aohehir@ymac.org.au",
     'dept': "Research",
     'office': "Perth"
     },

    {'email': "acargill@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "ausher@ymac.org.au",
     'dept': "Research",
     'office': ""
     },

    {'email': "amgibbs@ymac.org.au",
     'dept': "Finance",
     'office': ""
     },

    {'email': "anoble@ymac.org.au",
     'dept': "Communications",
     'office': ""
     },

    {'email': "atoh@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "APrice@ymac.org.au",
     'dept': "Heritage",
     'office': "Geraldton"
     },

    {'email': "amilroy@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "bstjames@ymac.org.au",
     'dept': "Heritage",
     'office': "Perth"
     },

    {'email': "cforsey@ymac.org.au",
     'dept': "Heritage",
     'office': "Perth"
     },

    {'email': "cjpoole@ymac.org.au",
     'dept': "Heritage",
     'office': "Perth"
     },

    {'email': "cpoustie@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "ctrees@ymac.org.au",
     'dept': "Legal",
     'office': "Geraldton"
     },

    {'email': "ccummings@ymac.org.au",
     'dept': "Research",
     'office': ""
     },

    {'email': "ctan@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "ccollins@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "cpoole@ymac.org.au",
     'dept': "Heritage",
     'office': "Perth"
     },

    {'email': "cmckellar@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "cherrmann@ymac.org.au",
     'dept': "Research",
     'office': "Perth"
     },

    {'email': "Callsop@ymac.org.au",
     'dept': "Research",
     'office': "Geraldton"
     },

    {'email': "DWells@ymac.org.au",
     'dept': "Legal",
     'office': "Geraldton"
     },

    {'email': "DFarrell@ymac.org.au",
     'dept': "Legal",
     'office': "Geraldton"
     },

    {'email': "dgarner@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "dtaft@ymac.org.au",
     'dept': "Legal",
     'office': "Geraldton"
     },

    {'email': "dnegi@ymac.org.au",
     'dept': "Finance",
     'office': "Perth"
     },

    {'email': "dfriedl@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "epilkington@ymac.org.au",
     'dept': "",
     'office': "Perth"
     },

    {'email': "elee@ymac.org.au",
     'dept': "Finance",
     'office': ""
     },

    {'email': "eharper@ymac.org.au",
     'dept': "Finance",
     'office': ""
     },

    {'email': "edecinque@ymac.org.au",
     'dept': "",
     'office': "Perth"
     },

    {'email': "godell@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "gyoung@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "hdaley@ymac.org.au",
     'dept': "Finance",
     'office': ""
     },

    {'email': "hwoods@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "jpage@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "jharman@ymac.org.au",
     'dept': "Heritage",
     'office': "Perth"
     },

    {'email': "jjoo@ymac.org.au",
     'dept': "Finance",
     'office': "Perth"
     },

    {'email': "JKalpers@ymac.org.au",
     'dept': "Research",
     'office': "Geraldton"
     },

    {'email': "kholloman@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "krusskikh@ymac.org.au",
     'dept': "Finance",
     'office': "Perth"
     },

    {'email': "kbrewster@ymac.org.au",
     'dept': "Research",
     'office': ""
     },

    {'email': "KChalmers@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "lalberghini@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "lgeddes@ymac.org.au",
     'dept': "Research",
     'office': "Perth"
     },

    {'email': "lkeepa@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "mchilala@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "mfort@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "mhealy@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "mmeegan@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "MRaj@ymac.org.au",
     'dept': "Legal",
     'office': ""
     },

    {'email': "nbielecki@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "nkimber@ymac.org.au",
     'dept': "Finance",
     'office': "Perth"
     },

    {'email': "ncolquhoun@ymac.org.au",
     'dept': "Research",
     'office': "Perth"
     },
    {'email': "onorris@ymac.org.au",
     'dept': "Research",
     'office': "Perth"
     },

    {'email': "rlawless@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "srosenfeld@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "srosenfeld@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "sbarnard@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "snalder@ymac.org.au",
     'dept': "Research",
     'office': ""
     },

    {'email': "scimetta@ymac.org.au",
     'dept': "Legal",
     'office': "Perth"
     },

    {'email': "swilliamson@ymac.org.au",
     'dept': "Finance",
     'office': ""
     },

    {'email': "spiotrowski@ymac.org.au",
     'dept': "HeritageGeraldton",
     'office': "Perth"
     },

    {'email': "shawkins@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "smorgan@ymac.org.au",
     'dept': "Research",
     'office': "Perth"
     },

    {'email': "sclews@ymac.org.au",
     'dept': "Communications",
     'office': "Perth"
     },

    {'email': "toliver@ymac.org.au",
     'dept': "Heritage",
     'office': "Perth"
     }]

users = [
    ("bstjames", "bstjames@ymac.org.au", "Brooke", "St James"),
    ("amgibbs", "amgibbs@ymac.org.au", "Anna Marie", "Gibbs"),
    ("wliu", " wliu@ymac.org.au", " Wenli", " Liu"),
    ("tolliver", " tolliver@ymac.org.au", " Tim", " Olliver"),
    ("toneill", " toneill@ymac.org.au", " Teri", " ONeill"),
    ("tcastro", " tcastro@ymac.org.au", " Tatiana", " Castro"),
    ("sclews", " sclews@ymac.org.au", " Suzanne", " Clews"),
    ("spashby", " spashby@ymac.org.au", " Steve", " Pashby"),
    ("smorgan", " smorgan@ymac.org.au", " Stephen", " Morgan"),
    ("shawkins", " shawkins@ymac.org.au", " Simon", " Hawkins"),
    ("swilliamson", " swilliamson@ymac.org.au", " Sarah", " Williamson"),
    ("scimetta", " scimetta@ymac.org.au", " Sarah", " Cimetta"),
    ("sbell", " sbell@ymac.org.au", " Sarah", " Bell"),
    ("sbarnard", " sbarnard@ymac.org.au", " Sandez", " Barnard"),
    ("srosenfeld", " srosenfeld@ymac.org.au", " Samantha", " Rosenfeld"),
    ("rlawless", " rlawless@ymac.org.au", " Ruth", " Lawless"),
    ("onorris", " onorris@ymac.org.au", " Olivia", " Norris"),
    ("ncolquhoun", " ncolquhoun@ymac.org.au", " Nyssa", " Colquhoun"),
    ("nkimber", " nkimber@ymac.org.au", " Nicholas", " Kimber"),
    ("nbielecki", " nbielecki@ymac.org.au", " Natalie", " Bielecki"),
    ("mmeegan", " mmeegan@ymac.org.au", " Michael", " Meegan"),
    ("mkurubalan", " mkurubalan@ymac.org.au", " Merra", " Kurubalan"),
    ("mlucioli", " mlucioli@ymac.org.au", " Melissa", " Lucioli"),
    ("mhealy", " mhealy@ymac.org.au", " Megan", " Healy"),
    ("moosthuizen", " moosthuizen@ymac.org.au", " Martie", " Oosthuizen"),
    ("mfort", " mfort@ymac.org.au", " Marcus", " Fort"),
    ("mchilala", " mchilala@ymac.org.au", " Maimbo", " Chilala"),
    ("lkeepa", " lkeepa@ymac.org.au", " Louise", " Keepa"),
    ("lgeddes", " lgeddes@ymac.org.au", " Linda", " Geddes"),
    ("lalberghini", " lalberghini@ymac.org.au", " Leanne", " Alberghini"),
    ("kbrewster", " kbrewster@ymac.org.au", " Kim", " Brewster"),
    ("kholloman", " kholloman@ymac.org.au", " Kate", " Holloman"),
    ("kjames", " kjames@ymac.org.au", " Kari", " James"),
    ("jjoo", " jjoo@ymac.org.au", " Jimin", " Joo"),
    ("jwhiteaker", " jwhiteaker@ymac.org.au", " Jessica", " Whiteaker"),
    ("jharman", " jharman@ymac.org.au", " Jason", " Harman"),
    ("jpage", " jpage@ymac.org.au", " Janet", " Page"),
    ("jelder", " jelder@ymac.org.au", " James", " Elder"),
    ("jgreene", " jgreene@ymac.org.au", " Jackie", " Greene"),
    ("idexter", " idexter@ymac.org.au", " Imogen", " Dexter"),
    ("hdaley", " hdaley@ymac.org.au", " Helen", " Daley"),
    ("gyoung", " gyoung@ymac.org.au", " Greg", " Young"),
    ("godell", " godell@ymac.org.au", " Graham", "O'Dell"),
    ("edizon", " edizon@ymac.org.au", " Erika", " Dizon"),
    ("edecinque", " edecinque@ymac.org.au", " Ericka", " Decinque"),
    ("eharper", " eharper@ymac.org.au", " Elizabeth", " Harper"),
    ("elee", " elee@ymac.org.au", " Eglantyne", " Lee"),
    ("epilkington", " epilkington@ymac.org.au", " Ebony", " Pilkington"),
    ("dcallan", " dcallan@ymac.org.au", " Deirdre", " Callan"),
    ("dnegi", " dnegi@ymac.org.au", " Deepak", " Negi"),
    ("datan", " datan@ymac.org.au", " Daphne", " Tan"),
    ("cherrmann", " cherrmann@ymac.org.au", " Corey", " Herrmann"),
    ("cmckellar", " cmckellar@ymac.org.au", " Colin", " McKellar"),
    ("ccollins", " ccollins@ymac.org.au", " Cheryl", " Collins"),
    ("ccham", " ccham@ymac.org.au", " Cheryl", " Cham"),
    ("ctan", " ctan@ymac.org.au", " Carolyn", " Tan"),
    ("ccummings", " ccummings@ymac.org.au", " Carmen", " Cummings"),
    ("cjpoole", " cjpoole@ymac.org.au", " Cameron", " Poole"),
    ("cforsey", " cforsey@ymac.org.au", " Callum", " Forsey"),
    ("bstjames", " bstjames@ymac.org.au", " Brooke", " St James"),
    ("bfordyce", " bfordyce@ymac.org.au", " Ben", " Fordyce"),
    ("aprice", " aprice@ymac.org.au", " Anys", " Price"),
    ("atoh", " atoh@ymac.org.au", " Annie", " Toh"),
    ("amgibbs", " amgibbs@ymac.org.au", " Anna Marie", " Gibbs"),
    ("ausher", " ausher@ymac.org.au", " Amy", " Usher"),
    ("acargill", " acargill@ymac.org.au", " Amy", " Cargill"),
    ("aohehir", " aohehir@ymac.org.au", " Amanda", " OHehir"),
    ("avaughan", " avaughan@ymac.org.au", " Alistair", " Vaughan"),
]

for user in users:
    for user_dict in staff_list:
        if user[1].lower().strip() == user_dict['email'].lower().strip():
            try:
                print('Creating user {0}.'.format(user))
                user = RequestUser.objects.create(
                    username=user[0],
                    email=user[1],
                    first_name=user[2],
                    last_name=user[3],
                    department=user_dict['dept'],
                    office=user_dict['office']
                )
            except:
                print
                'There was a problem creating the user: {0}.  Error: {1}.' \
                    .format(username, sys.exc_info()[1])
