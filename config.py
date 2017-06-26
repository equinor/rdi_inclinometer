class BaseConfig(object):
    DEBUG = False
    TESTING = False
    LOG_FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    LOG_FILE = "mmo_dev.log"


class ProductionConfig(BaseConfig):
    DEBUG = True
    LOG_FILE = "mmo_prod.log"
