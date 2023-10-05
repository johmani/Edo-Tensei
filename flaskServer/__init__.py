import config
from flask import Flask
# from flask_cors import CORS

# development
# production

app = Flask(__name__)
# CORS(app, origins='*')

app.config.from_object(config.get_config('production'))
app.jinja_env.globals.update(URL=app.config['URL'])

from flaskServer.controller import navigation, pragmataGirl
