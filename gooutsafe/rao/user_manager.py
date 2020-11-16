from gooutsafe import app
from gooutsafe.auth.user import User
import requests


class UserManager:
    USERS_ENDPOINT = app.config['USERS_MS_URL']

    @classmethod
    def get_user_by_id(cls, user_id: int) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user id.
        :param user_id: the user id
        :return: User obj with id=user_id
        """
        response = requests.get("%s/user/%d" % (cls.USERS_ENDPOINT, user_id))
        json_payload = response.json()

        if response.status_code == 200:
            # user is authenticated
            user = User.build_from_json(json_payload)
        else:
            raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)

        return user

    @classmethod
    def authenticate_user(cls, email: str, password: str) -> User:
        """
        This method authenticates the user trough users AP
        :param email: user email
        :param password: user password
        :return: None if credentials are not correct, User instance if credentials are correct.
        """
        payload = dict(email=email, password=password)
        response = requests.post('%s/authenticate' % cls.USERS_ENDPOINT, json=payload)
        json_response = response.json()

        if response.status_code == 401:
            # user is not authenticated
            return None
        elif response.status_code == 200:
            user = User.build_from_json(json_response['user'])
            return user
        else:
            raise RuntimeError(
                'Microservice users returned an invalid status code %s, and message %s'
                % (response.status_code, json_response['error_message'])
            )
