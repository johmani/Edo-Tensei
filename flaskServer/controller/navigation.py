from flask import render_template
from flaskServer import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pragmataGirl')
def pragmata_girl_page():
    return render_template('pragmataGirl.html')

@app.route('/about')
def about():
    return render_template('about.html')
