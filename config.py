class Config:
    SECRET_KEY = "uf_a0hxfgrbfyjhyffdacc"
    SESSION_COOKIE_SECURE = True
    DEBUG = False
    TESTING = False
    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video\pragmataGirl'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    HOST = 'johmani.mooo.com'
    PORT = 443
    URL = "https://" + HOST
    VIDEO_DIR = r'/mohamd/Edo-Tensei/flaskServer/client/video/pragmataGirl'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    HOST = '18.0.1.19'
    PORT = 80
    URL = "http://" + HOST
    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video\pragmataGirl'


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(env):
    return config_by_name.get(env,ProductionConfig)

