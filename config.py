class Config:
    SECRET_KEY = "uf_a0hxfgrbfyjhyffdacc"
    SESSION_COOKIE_SECURE = True
    DEBUG = False
    TESTING = False

    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video'


class ProductionConfig(Config):
    DEBUG = False
    SERVER_NAME = "johmani.mooo.com"
    HOST = 'johmani.mooo.com'
    PORT = 80
    VIDEO_DIR = r'/mohamd/Edo-Tensei/flaskServer/client/video'


class GunicornConfig(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 80
    VIDEO_DIR = r'/mohamd/Edo-Tensei/flaskServer/client/video'


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = "18.0.2.69"
    HOST = '18.0.2.69'
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
