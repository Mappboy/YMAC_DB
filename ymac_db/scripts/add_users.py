import sys

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

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

for username, email, first_name, last_name in users:
    try:
        print('Creating user {0}.'.format(username))
        user = User.objects.create_user(
            username=username,
            email=email,
            is_staff=True,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password("password123")
        user.save()

        assert authenticate(username=username, password="password123")
    except:
        print('There was a problem creating the user: {0}.  Error: {1}.' \
            .format(username, sys.exc_info()[1]))
