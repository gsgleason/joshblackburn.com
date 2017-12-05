from app import app
from flask import render_template

@app.route('/bio', methods = ['GET'])
def bio():
    return render_template('bio.html')
