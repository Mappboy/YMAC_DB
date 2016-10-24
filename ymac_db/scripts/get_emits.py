import os
import sys

import django

sys.path.append(r"C:\Users\cjpoole\PycharmProjects\ymac_sdb\\")
os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'

django.setup()
from datetime import date, timedelta
from ymac_db.models import Emit, YmacClaim

emit_array = []
#tenements = TenementsAll.objects.filter(fmt_tenid_in=past_week_emit).first()
for eobj in Emit.objects.filter(datereceived__gt=date.today()-timedelta(days=6)):
    emit_dict = {'title': eobj.title,
     'date_received': eobj.datereceived.strftime("%d/%m/%Y"),
     'objectiondate': eobj.objectiondate,
     'applicants': eobj.applicants}
    tenement = eobj.tenement
    if tenement:
        emit_dict['mapped'] = bool(tenement)
        claims = YmacClaim.objects.filter(geom__intersects=tenement.geom)
        if claims:
            emit_dict['claims'] = ",".join((str(c) for c in claims))
        else:
            emit_dict['claims'] = "outside Ymac Claims"
    else:
        emit_dict['tenement'] = False
        emit_dict['claim'] = "Potentially " + eobj.possibleclaimgroups
    emit_array.append(emit_dict)
print(emit_array)