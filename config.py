class Config(object):
    """
    Main Configuration for Go Out Safe API Gateway
    """
    DEBUG = False
    TESTING = False

    # configuring microservices endpoints
    import os

    # users microservice
    USERS_MS_PROTO = os.getenv('USERS_MS_PROTO', 'http')
    USERS_MS_HOST = os.getenv('USERS_MS_HOST', 'localhost')
    USERS_MS_PORT = os.getenv('USERS_MS_PORT', 5001)
    USERS_MS_URL = '%s://%s:%s' % (USERS_MS_PROTO, USERS_MS_HOST, USERS_MS_PORT)

    # restaurants
    RESTA_MS_PROTO = os.getenv('RESTAURANTS_MS_PROTO', 'http')
    RESTA_MS_HOST = os.getenv('RESTAURANTS_MS_HOST', 'localhost')
    RESTA_MS_PORT = os.getenv('RESTAURANTS_MS_PORT', 5002)
    RESTA_MS_URL = '%s://%s:%s' % (RESTA_MS_PROTO, RESTA_MS_HOST, RESTA_MS_PORT)

    # reservation
    RESERVATION_MS_PROTO = os.getenv('RESERVATION_MS_PROTO', 'http')
    RESERVATION_MS_HOST = os.getenv('RESERVATION_MS_HOST', 'localhost')
    RESERVATION_MS_PORT = os.getenv('RESERVATION_MS_PORT', 5003)
    RESERVATION_MS_URL = '%s://%s:%s' % (RESERVATION_MS_PROTO, RESERVATION_MS_HOST, RESERVATION_MS_PORT)


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

