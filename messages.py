from app import app
from flask import render_template, request
import requests
from db import Contact, session
import pytz
import config


@app.route('/messages', methods = ['GET','POST'])
def messages():
	if request.method == 'POST':
		errors = []
		password = request.form.get('password')
		if password != config.messages.password:
			errors.append('Password Failure')
			return render_template('error.html',errors=errors), 403
		g_recaptcha_response = request.form.get('g-recaptcha-response')
		secret = config.reCaptcha.secret
		url = config.reCaptcha.url
		if request.headers.getlist("X-Forwarded-For"):
			ip = request.headers.getlist("X-Forwarded-For")[0]
		else:
			ip = request.remote_addr
		site_key = config.reCaptcha.site_key
		data = {'secret':secret,'response':g_recaptcha_response,'remoteip':ip}
		r = requests.post(url,data=data)
		if r.status_code != 200:
			errors.append('reCAPTCHA service failure')
			return render_template('error.html',errors=errors)
		result = r.json()
		success = result.get('success')
		if success is not True:
			errors.append('reCAPTCHA failure')
			for error in result.get('error-codes'):
				errors.append(error)
			return render_template('error.html',errors=errors), 429

		items = []
		for item in session.query(Contact).all():
			utc = pytz.utc
			localtz = pytz.timezone('America/Denver')
			item.localtime = utc.localize(item.utctime).astimezone(localtz)
			items.append(item)
		session.close()
		return render_template('messages.html', items=items)
	else:
		site_key = config.reCaptcha.site_key
		return render_template('password.html', site_key=site_key)
