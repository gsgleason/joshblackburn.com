from app import app
from flask import render_template, redirect, url_for, request
from db import session, Event
import datetime
from pytz import timezone, utc
from urllib.parse import urlencode, quote_plus, quote
from ics import Calendar as iCal, Event as iEvent
import re

mountain = timezone('US/Mountain')

@app.route('/shows')
def shows():
	now = datetime.datetime.now(mountain)
	return render_template('shows.html', events=get_events())

def get_events():
	if re.search('(?:iPhone|iPad|iPod)', request.user_agent.string):
		iOS = True
	else:
		iOS = False
	now = datetime.datetime.now(mountain)
	events = []
	for event in session.query(Event).all():
		if event.all_day:
			start = mountain.localize(event.start)
			end = mountain.localize(event.end)
		else:
			start = utc.localize(event.start).astimezone(mountain)
			end = utc.localize(event.end).astimezone(mountain)
		if now >  end:
			continue
		event.date = start.strftime('%a %b %d')
		event.time = start.strftime('%I:%M %p') + " - " + end.strftime('%I:%M %p')
		data = {}
		data['action'] = 'TEMPLATE'
		data['hl'] = 'en'
		data['ctz'] = 'America/Denver'
		data['text'] = 'Josh Blackburn at {}'.format(event.title)
		if event.location:
			data['location'] = event.location
			event.gmap_link = "//maps.google.com/maps?q={}".format(quote_plus(event.location))
			event.imap_link = "//maps.apple.com/?q={}".format(quote_plus(event.location))
		else:
			data['location'] = event.title
			event.gmap_link = None
			event.imap_link = None
		if event.all_day:
			data['dates'] = start.strftime('%Y%m%d') + '/' + end.strftime('%Y%m%d')
		else:
			data['dates'] = start.strftime('%Y%m%dT%H%M%S') + '/' + end.strftime('%Y%m%dT%H%M%S')
		event.gcal_link = 'https://calendar.google.com/calendar/event?{}'.format(urlencode(data))
		c = iCal()
		e = iEvent()
		e.name = data['text']
		e.begin = start
		e.end = end
		e.location = data['location']
		c.events.append(e)
		event.ics_link = "data:text/calendar,{}".format(quote(str(c)))
		if iOS:
			event.cal_link = event.ics_link
			event.map_link = event.imap_link
		else:
			event.cal_link = event.gcal_link
			event.map_link = event.gmap_link
		events.append(event)
	session.close()
	return events

