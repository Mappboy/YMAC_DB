#Script for pulling out and processing data from Spatial Request Form
#May contemplate adding into PostGresSQL https://wiki.postgresql.org/wiki/Psycopg2_Tutorial
#Or using smartsheet or trello API to https://github.com/plish/Trolly
# http://smartsheet-platform.github.io/api-docs/?shell#add-row(s) 
#User requests http://www.python-requests.org/en/latest/user/quickstart/
# Smartsheet API 4104lxpew3jppnp3xvoeff7yp

import cgi
import cgitb; cgitb.enable()
import requests
import json
import datetime
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib

COMMASPACE = ', '

#log dir

form = cgi.FieldStorage()
#
name = form.getvalue("element_0")
email = form.getvalue("element_1")
dept = form.getvalue("element_2")
req_type = form.getvalue("element_3")
office = form.getvalue("element_4")
region = form.getvalue("element_5")
claims = form.getlist("element_6")
job_desc = form.getvalue("element_7")
map_size = form.getvalue("element_8")
sup_data = form.getvalue("element_9")
##This should be a date/Maybe convert this who knows
req_by = form.getvalue("element_10")
cc_recip = form.getvalue("element_11")
deliv_instructions = form.getvalue("element_12")
other_instructions = form.getvalue("element_13")
cost_centre = form.getvalue("element_14")
proponent = form.getvalue("element_15")
priority = form.getvalue("element_16")

req_by_formatted = datetime.datetime.strptime(req_by,"%Y-%m-%d").strftime("%d/%m/%Y"),


print 'Content-type: text/html'
print
print '<HTML><HEAD><TITLE>Thanks</TITLE>'
print '<link rel="icon" href="http://ymac.org.au/wp-content/themes/ymac/favicon.png">'
print '<link rel="stylesheet" type="text/css" href="/css/bootstrap.min.css"/>'
print  '<link rel="stylesheet" type="text/css" href="/css/site_global.css"/>'
print '</HEAD>'
#Put style sheet in here
# maybe centralise and add a return link
print '<BODY>'
print '<div class="container main"><!-- group -->'
print '<header>'
print '<img src="/images/logo.png" data-src="/images/logo.png" class="img-responsive logo" alt="YMAC" >'
print '</header>'
print '<div class="container main wrapper">'
print '<div class="jumbotron">'
print '<H1>Thank you %s </H1>' % name
#format req_by
print 'We will aim to have your request completed by %s' % req_by_formatted
print '</br>'


# DO SOME PROCESSING OF MAP TYPE FIRST
MAP_REQUESTS = ["Claim Map",
"Quarterly Maps",
"Customised Map",
"Boundary Research Map"]
ANALYSIS = ["Spatial Analysis",
"Boundary Technical Description",
"Map and Technical Description",
"Heritage Mapping",
"Negotiation Mapping"]
DATA = [
"ArcPad Form",
"ArcGIS Collector setup",
"Data Supply",
"Data Update"]
OTHER = [
"Field Work",
"Other",
"Uncertain"]
#TODO REfactor this it's been to long in between proper coding stints
map, analysis, data, other = [False] * 4
if req_type in MAP_REQUESTS:
	map = True
if req_type in ANALYSIS:
	analysis = True
if req_type in DATA:
	data = True
if req_type in OTHER:
	other = True

headers = {
			"Authorization": "Bearer 4104lxpew3jppnp3xvoeff7yp"
			}
#Smartsheet that contains jobs
surl = "https://api.smartsheet.com/2.0/sheets/3001821196248964"

#Get the top most row and pull out the job control cell and increment and create new id
r = requests.get(url=surl, headers=headers)
if r.status_code == 200:	
	q = json.loads(r.text)
	jobid = [ l for l in q['rows'][0]['cells'] if l.has_key('displayValue') and
			'J201' in l['displayValue'] ][0]['value']
	jid = int(jobid.split("-")[1]) + 1
	new_jobid = "J" + time.strftime("%Y") + "-" + str(jid).zfill(3)

url = surl + "/rows"
headers["Content-Type"] = "application/json"

#Column id comes from calling api columns/ can't use name as id
today = datetime.date.today().strftime("%Y-%m-%d")
payload = {
			"toTop": 'true',
			"cells": [
						#Task NAME	
						{"columnId": 6673625647474564,
						"value": req_type},
						#Job Description
						{"columnId": 8870449879771012,
						"value": job_desc
						},
                        #Map Size
                        {
                        "columnId": 974271080324,
						"value": map_size
                        },
                        #Supplementary Data
                        {"columnId": 9006524258379652,
						"value": sup_data
                        },
						#Job Control #
						{"columnId": 3404520484038532,
						"value": new_jobid
						},
						#Requested By
						{"columnId": 4366850252400516,
						"value": email,
                        "displayValue":name
						},
						#Map
						{"columnId" : 3778411379353476,
						"value" : map
						},
						#Data 
						{"columnId" : 8282011006723972,
						"value" : data
						},
						#Analysis 
						{"columnId" : 963661612246916,
						"value" : analysis
						},
						#Other 
						{"columnId" : 5467261239617412,
						"value" : data
						}  ,
						#Request Source 
						{"columnId" : 4533976019822468,
						"value" : "New Spatial Form"
						},
						#Email ME# 
						{"columnId" : 30376392451972,
						"value" : "N/A"
						},
						#CC
						{"columnId" : 74356857563012,
						"value" : cc_recip
						},
						#Priority Urgency
						{"columnId" : 8633780001892228,
						"value" : priority 
						},
						#Request Date 
						{"columnId" : 6248973640984452,
						"value" : today
						},
						#Due Date 
						{"columnId" : 4421825833789316,
						"value" : req_by
						},
						#Comments
						{"columnId" : 4632932066322308,
						"value" : other_instructions
						},
					]
			}
# Post directly to smartsheet This is working I am bloody amazing...
# Man Clivie REALLY would of enjoyed this. FAWK.
r = requests.post(url=url, headers=headers, data=json.dumps(payload))

if r.status_code != 200:
	print "<em>Failed to post to smartsheet %s</em>" % r.text

print '<a href="/">Click Me to return</a>'
print '</div>'
print '</div>'
print  '<footer class="fixed footer">'
print  '  <div class="container">'
print  '    <p class="text-muted">&copy; YMAC 2015</p>'
print  '  </div>'
print  '</footer>'
print '</BODY>'
print '</html>'

# Cool now send email out


#This is what needs to go into the email

body = """
Name: {0}\n
Email: {1}\n
Department: {2}\n
Request Type: {3}\n
Office: {4}\n
Region: {5}\n
Job Description: {6}\n
Supplementary Data: {12}\n
Map Size: {13}\n
Required by: {7} \n
Delivery and/or Product Instructions: {8} {9}\n
Cost Centre: {10}\n
Priority and urgency: {11}\n""".format(
									name,
									email,
									dept,
									req_type,
									office,
									region,
									job_desc,
									req_by_formatted,
									deliv_instructions,
									other_instructions,
									cost_centre,
									priority,
                                    sup_data,
                                    map_size
									)


# "spatialjobs@ymac.org.au" Should probably be the default
toaddr = ["spashby@ymac.org.au",
		  "cjpoole@ymac.org.au",
		  "cforsey@ymac.org.au"]
	
msg = MIMEMultipart()
msg['From'] = email if email else "spatialjobs@ymac.org.au"
msg['To'] = COMMASPACE.join(toaddr)
msg['Subject'] = "{map_type} {job_id} request".format(map_type=req_type,job_id=new_jobid)

msg.attach(MIMEText(body, 'plain'))
s = smtplib.SMTP('ymac-org-au.mail.protection.outlook.com',25)
s.sendmail(email, toaddr, msg.as_string())
s.quit()