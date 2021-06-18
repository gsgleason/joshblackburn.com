from app import app
from flask import render_template, session, abort, Response
import os
import config
audio_dir = config.audio.dir

import string
import random
def key_gen(size=8, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class Album(object):
	pass

album_list  =  []

album  =  Album()
album.title = "Brand New Something"
album.artist = "Josh Blackburn"
album.year = "2003"
album.tracks = ["Take Me Away","Starting Zone","Round The Bend","Brand New Something","Right Eye Twitch","Left Eye Spasm","Earthquake","Hey Connection","Listen to Yourself","Pleasure Boat","Two of a Kind","Traveling Band","Here You Go","An Occupational Alternative","Bugs in my Garage"]
album.art = "brand_new_something"
album.blurb = '<p>Brand New Something is Josh\'s debut homebrew album, produced, recorded and performed by Josh himself; a collector\'s item indeed!</p>'
album_list.append(album)

album  =  Album()
album.title = "Starting Ground"
album.artist = "Josh Blackburn"
album.year = "2006"
album.tracks = ["Take Me Away","Sylvia","Earthquake","Bad Girl","Traveling Band","Low Rider","Starting Ground","Time Machine","Risk","Ear","Honky Tonk Blues","Picture Perfect","Breaking Point"]
album.art = "starting_ground"
album.blurb = ''
album.spotify_id = '10k64HAuJ5pLXOOg12CIGh'
album_list.append(album)

album  =  Album()
album.title = "Flipside"
album.artist = "Josh Blackburn"
album.year = "2010"
album.tracks = ["Flipside","Real World","Jump Off","The Reel","Exploidia","Here You Go","I'm Dirt","Just Talkin'","Went to a Party","Into the Cell","Round the Bend, part I","Round the Bend, part II","Round the Bend, part III","Long Ride Home","Something Pink in the Room"]
album.art = "flipside"
album.blurb = '<blockquote><p>Flipside is a piece of work that I recorded in the Spring/Summer of 2010.  The best way that I can describe the album is quite difficult.  It is not your everyday album with a constant theme and sound.  It is constantly contrasting light and dark, heavy and soft, from genre to genre always changing with the only common thread of a vocal.  That is where the title "Flipside" came into play.  I wanted to continually flip from one world to the next with each song.  I think you really need to understand that before you hear this work.  It is intentional.  It is a jumbling of the senses.  Be prepared to jump out of your musical bubble and listen to genres you never would.  I hope you enjoy it.  It is extremely close to my heart.  Peace.</p></blockquote>'
album.spotify_id = '3hvEIx3XndfMFGu17AAUq7'
album_list.append(album)

album  =  Album()
album.title = "Purple Elephant"
album.artist = "Josh Blackburn"
album.year = "2012"
album.tracks = ["Intro","At the Station","Victor the Cat Killer","The Curtain","Gillian's Journey","Purple Elephant","Jenna's Title","I would","Strange Look","Flickering Scene","Please","Patience for Sympathy","Release","Spacious Android Elements","Outro","Washed Up Washed Down","New Light"]
album.art = "purple_elephant"
album.blurb = '<blockquote><p>Purple Elephant is a piece of work written in the Winter/Summer of 2011. I did the whole album start to finish in my guest bedroom on my home computer. I recorded all instruments, produced, mixed, and mastered it myself. Quite the learning experience I must say. Caution: This album is not FLIPSIDE. It is new. It is different. It is my heart on a platter. I hope you enjoy it.</p></blockquote>'
album.spotify_id = '5tkWTICkD6q6I0Esq2zeDn'
album_list.append(album)

album  =  Album()
album.title = "Dirty Bird"
album.artist = "Josh Blackburn"
album.year = "2015"
album.tracks = ["Dirty Bird","In a Moment","Break Him Down","One Song Start","Cry Little Sister","Beauty Queen","Rivertown","Grab Your Things","Tired","Creeper","Rolling to the Reservoir","Words","Fading"]
album.art = "dirty_bird"
album.blurb = ''
album.spotify_id = '65Xu38FQnAw2BrcUvsJZiL'
album_list.append(album)

album  =  Album()
album.title = "Straight & Narrow"
album.artist = "Josh Blackburn"
album.year = "2021"
album.tracks = ["Straight & Narrow", "The Load You Bear", "Remember I Said", "Always Be Me", "What Would You Think", "My Way", "Headlines", "Hurt On Me", "Fall Blues", "Please Believe Me", "I'll Play The Blues for You", "The Ship"]
album.art = "straight_and_narrow"
album.blurb = '<p></p>'
album.spotify_id = '3pWpf4o6XGgpHhOw5gGdN0'
album_list.append(album)

import json
album_json = json.dumps(album_list, default=lambda o: o.__dict__)

album_list = list(reversed(album_list))

@app.route('/albums', methods = ['GET'])
def albums():
	if 'key' not in session:
		session['key'] = key_gen()
	return render_template('albums.html', album_list=album_list)

@app.route('/albums.js')
def albums_js():
	return render_template('albums.js', album_json=album_json)

@app.route('/audio/<fmt>/<album>/<track>')
def getfile(fmt,album,track):
	if session.get('key') is None:
		abort(404)
	fileName = os.path.join(audio_dir,fmt,album,track)
	with open(fileName, mode='rb') as file:
		fileContent = file.read()
	if fmt == "mp3":
		mime = "audio/mpeg"
	if fmt == "ogg":
		mime = "audio/ogg"
	resp = Response(fileContent, mimetype=mime)
	resp.headers['Content-Disposition'] = 'attachment'
	return resp
