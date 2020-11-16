import os

from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_environments import Environments

__version__ = '0.1'

login = None
debug_toolbar = None
celery = None
app = None


def create_app():
    """
    This method create the Flask application.
    :return: Flask App Object
    """
    global app
    global login

    app = Flask(__name__, instance_relative_config=True)

    flask_env = os.getenv('FLASK_ENV', 'None')
    if flask_env == 'development':
        config_object = 'config.DevConfig'
    elif flask_env == 'testing':
        config_object = 'config.TestConfig'
    elif flask_env == 'production':
        config_object = 'config.ProdConfig'
    else:
        raise RuntimeError(
            "%s is not recognized as valid app environment. You have to setup the environment!" % flask_env)

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_handlers(app)

    # loading login manager
    import gooutsafe.auth.login_manager as lm
    login = lm.init_login_manager(app)

    if flask_env == 'testing' or flask_env == 'development':
        register_test_blueprints(app)

    return app


def register_extensions(app):
    """
    It register all extensions
    :param app: Flask Application Object
    :return: None
    """
    global debug_toolbar

    if app.debug:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            debug_toolbar = DebugToolbarExtension(app)
        except ImportError:
            pass

    # adding bootstrap and date picker
    Bootstrap(app)


def register_blueprints(app):
    """
    This function registers all views in the flask application
    :param app: Flask Application Object
    :return: None
    """
    from gooutsafe.views import blueprints
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix='/')


def register_test_blueprints(app):
    """
    This function registers the blueprints used only for testing purposes
    :param app: Flask Application Object
    :return: None
    """

    from gooutsafe.views.utils import utils
    app.register_blueprint(utils)


def register_handlers(app):
    """
    This function registers all handlers to application
    :param app: application object
    :return: None
    """
    from .handlers import page_404, error_500

    app.register_error_handler(404, page_404)
    app.register_error_handler(500, error_500)
