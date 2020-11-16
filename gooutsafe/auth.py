from flask_login import LoginManager
from gooutsafe.rao.user_manager import UserManager


def init_login_manager(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.refresh_view = 'auth.relogin'

    @login_manager.user_loader
    def load_user(user_id):
        """
        We need to connect to users endpoint and load the user.
        Here we can implement the redis caching

        :param user_id: user id
        :return: the user object
        """
        return UserManager.get_user_by_id(user_id)

    return login_manager


