class BaseConfig(object):
    DEBUG = False
    TESTING = False
    LOG_FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    LOG_FILE = "log_dev.log"


class ProductionConfig(BaseConfig):
    DEBUG = False
    LOG_FILE = "log_prod.log"
