from gooutsafe.auth.user import User
import requests


class UserManager:

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user id.
        :param user_id: the user id
        :return: User obj with id=user_id
        """
        response = requests.get("http://127.0.0.1:5001/users/%d" % user_id)
        json_payload = response.json()

        if response.status_code == 200:
            # user is authenticated
            user = User.build_from_json(json_payload)
        else:
            raise RuntimeError('Boh non lo so')

        return user
