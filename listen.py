from app import app
from flask import render_template 
from albums import album_list

@app.route('/listen', methods = ['GET'])
def listen():
	return render_template('listen.html', album_list=album_list)

