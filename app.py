from flask import Flask

app = Flask(__name__)
app.config.from_object('config.flask')

import db
import index
import shows
import albums
import contact
import listen
import messages
import error
