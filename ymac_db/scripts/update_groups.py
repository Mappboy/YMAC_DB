import sys, os
import django
# Loading in HSIF and PA
sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()
#from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from ymac_db.models import RequestUser

User = get_user_model()

for u in User.objects.all():
    ru = RequestUser.objects.filter(name__icontains=u.first_name).filter(name__icontains=u.last_name)
    if u.username != 'spuser' and ru:
        print(u.groups.add(*Group.objects.filter(name=ru[0].department)))