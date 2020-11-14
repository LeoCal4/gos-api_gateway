class Config(object):
    DEBUG = False
    TESTING = False


class DebugConfig(Config):
    """
    This is the main configuration object for application.
    """
    DEBUG = True
    TESTING = True

    SECRET_KEY = b'isreallynotsecretatall'


class DevConfig(DebugConfig):
    """
    This is the main configuration object for application.
    """
    pass


class TestConfig(Config):
    """
    This is the main configuration object for application.
    """
    TESTING = True

    import os
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    """
    This is the main configuration object for application.
    """
    TESTING = False
    DEBUG = False

    import os
    SECRET_KEY = os.getenv('APP_SECRET_KEY', os.urandom(24))

