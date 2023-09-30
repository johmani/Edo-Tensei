class Config:
    SECRET_KEY = "uf_a0hxfgrbfyjhyffdacc"
    SESSION_COOKIE_SECURE = True
    DEBUG = False
    TESTING = False

    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    # SERVER_NAME = "johmani.mooo.com"
    HOST = '127.0.0.1'
    PORT = 5000
    VIDEO_DIR = r'/mohamd/Edo-Tensei/flaskServer/client/video'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    # SERVER_NAME = "18.0.1.75"
    HOST = '18.0.1.75'
    PORT = 80

    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video'



config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(env):
    return config_by_name.get(env, DevelopmentConfig)
