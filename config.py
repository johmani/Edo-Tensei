class Config:
    SECRET_KEY = "uf_a0hxfgrbfyjhyffdacc"

    SESSION_COOKIE_SECURE = True
    DEBUG = False
    TESTING = False

    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video'


class ProductionConfig(Config):
    DEBUG = False
    HOST = '154.41.228.96'
    PORT = 80
    VIDEO_DIR = r'/mohamd/Edo-Tensei/flaskServer/client/video'
    SESSION_COOKIE_DOMAIN = "johmani.mooo.com"
    SESSION_COOKIE_PATH = "/"
    SESSION_COOKIE_SECURE = "false"


class GunicornConfig(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 80
    VIDEO_DIR = r'/mohamd/Edo-Tensei/flaskServer/client/video'



class DevelopmentConfig(Config):
    DEBUG = True

    HOST = '18.0.1.30'
    PORT = 80

    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video'



class TestingConfig(Config):
    TESTING = True


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'gunicorn': GunicornConfig
}

def get_config(env):
    return config_by_name.get(env, DevelopmentConfig)
