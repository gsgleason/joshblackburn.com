from app import app
from flask import render_template
from db import session, Event
import datetime
from pytz import timezone, utc
mountain = timezone('US/Mountain')
from shows import get_events

@app.route('/', methods = ['GET'])
def index():
	todayShows = []
	now = datetime.datetime.now(mountain)
	for event in get_events():
		if event.all_day:
			start = mountain.localize(event.start)
			end = mountain.localize(event.end)
		else:
			start = utc.localize(event.start).astimezone(mountain)
			end = utc.localize(event.end).astimezone(mountain)
		if start.date() == now.date() and now < end:
			todayShows.append(event)
	return render_template('index.html', todayShows=todayShows)

