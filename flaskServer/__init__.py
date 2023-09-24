from config import get_config
from flask import Flask

# development
# production
# testing
# default
# gunicorn

app = Flask(__name__)
app.config.from_object(get_config('production'))
app.jinja_env.globals.update(HOST=app.config['HOST'])
app.jinja_env.globals.update(PORT=app.config['PORT'])





from flaskServer import views