class Config:
    SECRET_KEY = "uf_a0hxfgrbfyjhyffdacc"
    SESSION_COOKIE_SECURE = True
    DEBUG = False
    TESTING = False



class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    HOST = 'edo-tensei.mooo.com'
    PORT = 443
    URL = "https://" + HOST



class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    HOST = '18.0.1.12'
    PORT = 80
    URL = f'http://{HOST}:{PORT}'



config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(env):
    return config_by_name.get(env,ProductionConfig)

