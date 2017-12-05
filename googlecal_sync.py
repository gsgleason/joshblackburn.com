import config
import requests
import datetime
import iso8601
import json
from pytz import timezone
from pytz import utc
from urllib.parse import quote_plus, urlencode
from ics import Calendar as iCal, Event as iEvent
from base64 import b64encode

from db import session, Event, initDB

mountain = timezone('US/Mountain')

yesterday = datetime.datetime.now(mountain) - datetime.timedelta(days=1)
timeMin = yesterday.isoformat('T')
params = {
	'key' : config.calendar.api_key,
	'singleEvents' : 'true', 
	'orderBy' : 'startTime',
	'timeMin' : timeMin,
	'maxResults' : config.calendar.max_results
}

r = requests.get(config.calendar.uri, params)

if r.status_code == 200:
	initDB()

	items = json.loads(r.text.encode('utf8'))['items']
	
	for item in items:
		try:
			if item['visibility'] == "private":
				continue
		except:
			pass
		event = Event()
		data = {}
		event.title = item['summary']
		event.location = item.get('location')
		if 'date' in item['start']:
			event.all_day = True;
			event.start = iso8601.parse_date(item['start']['date'])
			event.end = iso8601.parse_date(item['end']['date'])
		else:
			event.all_day = False;
			event.start = iso8601.parse_date(item['start']['dateTime']).astimezone(utc)
			event.end = iso8601.parse_date(item['end']['dateTime']).astimezone(utc)
		session.add(event)
	
	session.commit()
	session.close()
