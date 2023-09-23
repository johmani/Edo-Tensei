from config import get_config
from flask import Flask

# development
# production
# testing
# default
# gunicorn

app = Flask(__name__)
app.config.from_object(get_config('gunicorn'))



from flaskServer import views