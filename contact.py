from app import app
from flask import render_template, request, abort
import requests
from db import session, Contact
import smtplib
from email.mime.text import MIMEText
import datetime
from pytz import timezone
import config

errors = []

@app.route('/contact', methods = ['GET','POST'])
def contact():
	if request.method == 'POST':
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
			return render_template('error.html',errors=errors), 400
		result = r.json()
		success = result.get('success')
		if success is not True:
			errors.append('reCAPTCHA failure')
			for error in result.get('error-codes'):
				errors.append(error)
			return render_template('error.html',errors=errors), 429
		contact = Contact()
		contact.name = request.form.get('name')
		contact.email = request.form.get('email')
		contact.message = request.form.get('message')
		contact.ip = ip
		session.add(contact)
		session.commit()
		session.close()

		date = datetime.datetime.now(timezone('US/Mountain')).strftime('%Y-%m-%d %I:%M:%S %p')
		msg = MIMEText("Date/Time: {}\nName: {}\nEmail: {}\n\n{}".format(date,contact.name,contact.email,contact.message))
		msg['Subject'] = "Website Comment {}".format(date) 
		msg['Reply-To'] = '"{}" <{}>'.format(contact.name,contact.email)
		msg['From'] = "www@joshblackburn.com"
		msg['To'] = "josh@joshblackburn.com, admin@joshblackburn.com"
		server = smtplib.SMTP(config.mail.host,config.mail.port)
		server.ehlo()
		server.starttls()
		server.login(config.mail.user,config.mail.password)
		server.sendmail("www@joshblackburn.com", ["josh@joshblackburn.com","admin@joshblackburn.com"], msg.as_string())
		server.quit()

		return render_template('contact_thanks.html')
	else:
		site_key = config.reCaptcha.site_key
		return render_template('contact.html', site_key=site_key)
