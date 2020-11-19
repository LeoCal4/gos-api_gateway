from gooutsafe import app
from gooutsafe.auth.user import User
import requests
from gooutsafe import app


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
    def get_user_by_email(cls, user_email: str):
        """
        This method contacts the users microservice
        and retrieves the user object by user email.
        :param user_email: the user email
        :return: User obj with email=user_email
        """
        response = requests.get("%s/user_email/%s" % (cls.USERS_ENDPOINT, user_email))
        json_payload = response.json()
        user = None

        if response.status_code == 200:
            user = User.build_from_json(json_payload)
    
        return user
    
    @classmethod
    def get_user_by_phone(cls, user_phone: str) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user phone.
        :param user_phone: the user phone
        :return: User obj with phone=user_phone
        """
        response = requests.get("%s/user_phone/%s" % (cls.USERS_ENDPOINT, user_phone))
        json_payload = response.json()
        user = None

        if response.status_code == 200:
            user = User.build_from_json(json_payload)
        
        return user

    @classmethod
    def get_user_by_social_number(cls, user_social_number: str) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user social_number.
        :param user_social_number: the user social_number
        :return: User obj with social_number=user_social_number
        """
        response = requests.get("%s/user_social_number/%s" % (cls.USERS_ENDPOINT, user_social_number))
        json_payload = response.json()
        user = None

        if response.status_code == 200:
            user = User.build_from_json(json_payload)
       
        return user

    @classmethod
    def add_social_number(cls, user_id: int, social_number:str):
        """
        This method contacts the users microservice
        to add the social number for a customer
        :param user_id: the user id
        :return: User updated
        """
        url = "%s/social_number/%d" % (cls.USERS_ENDPOINT, user_id)

        response = requests.put(url,
                            json={
                                'social_number': social_number
                            })
        return response

    @classmethod
    def update_user(cls, user_id: int, email:str, password:str, phone:str):
        """
        This method contacts the users microservice
        to allow the users to update their profiles
        :param user_id: the user id
            email: the user email
            password: the user password
            phone: the user phone
        :return: User updated
        """

        user = UserManager.get_user_by_id(user_id)
        if user.type == "customer":
            url = "%s/customer/%d" % (cls.USERS_ENDPOINT, user_id)
            response = requests.put(url,
                                json={
                                    'email': email,
                                    'password': password,
                                    'phone': phone
                                })
            return response

        elif user.type == "operator":
            url = "%s/operator/%d" % (cls.USERS_ENDPOINT, user_id)
            response = requests.put(url,
                                json={
                                    'email': email,
                                    'password': password
                                })
            return response 
        
        raise RuntimeError('Error with searching for the user %d' % user_id)
        
    @classmethod
    def delete_user(cls, user_id: int):
        """
        This method contacts the users microservice
        to delete the account of the user
        :param user_id: the user id
        :return: User updated
        """
        pass

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
