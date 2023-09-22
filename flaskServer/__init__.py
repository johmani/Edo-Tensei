from config import get_config
from flask import Flask

# development
# production
# testing
# default


app = Flask(__name__)
app.config.from_object(get_config('production'))



from flaskServer import views