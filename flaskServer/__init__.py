import config
from flask import Flask
from flask_cors import CORS

# development
# production

app = Flask(__name__)
CORS(app, origins='*')

app.config.from_object(config.get_config('production'))

app.jinja_env.globals.update(ENV=app.config['ENV'])
app.jinja_env.globals.update(HOST=app.config['HOST'])
app.jinja_env.globals.update(PORT=app.config['PORT'])

from flaskServer import views