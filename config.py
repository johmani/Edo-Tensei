class Config:
    SECRET_KEY = "uf_a0hxfgrbfyjhyffdacc"
    SESSION_COOKIE_SECURE = True
    DEBUG = False
    TESTING = False



class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    HOST = 'johmani.mooo.com'
    PORT = 443
    URL = "https://" + HOST



class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000
    URL = f'http://{HOST}:{PORT}'



config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(env):
    return config_by_name.get(env,ProductionConfig)

