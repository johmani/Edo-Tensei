class Config:
    SECRET_KEY = "mkjshsikvnikvdpdfj"
    SESSION_COOKIE_SECURE = True
    DEBUG = False
    TESTING = False

    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video'


class ProductionConfig(Config):
    DEBUG = False
    HOST = '154.41.228.96'
    PORT = 5000





class DevelopmentConfig(Config):
    DEBUG = True

    HOST = '18.0.1.24'
    PORT = 5000

    VIDEO_DIR = r'C:\Users\mohamd\Desktop\Edo-Tensei\flaskServer\client\video'



class TestingConfig(Config):
    TESTING = True


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}

def get_config(env):
    return config_by_name.get(env, DevelopmentConfig)