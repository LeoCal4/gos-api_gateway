from gooutsafe.auth.user import User
from gooutsafe import app
from flask_login import (logout_user)
from flask import abort
import requests


class UserManager:
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_user_by_id(cls, user_id: int) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user id.
        :param user_id: the user id
        :return: User obj with id=user_id
        """
        try:
            response = requests.get("%s/user/%s" % (cls.USERS_ENDPOINT, str(user_id)), 
                        timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            if response.status_code == 200:
                # user is authenticated
                user = User.build_from_json(json_payload)
            else:
                raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user
    
    @classmethod
    def get_user_by_email(cls, user_email: str):
        """
        This method contacts the users microservice
        and retrieves the user object by user email.
        :param user_email: the user email
        :return: User obj with email=user_email
        """
        try:
            response = requests.get("%s/user_email/%s" % (cls.USERS_ENDPOINT, user_email),
                        timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            user = None

            if response.status_code == 200:
                user = User.build_from_json(json_payload)
                
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user
    
    @classmethod
    def get_user_by_phone(cls, user_phone: str) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user phone.
        :param user_phone: the user phone
        :return: User obj with phone=user_phone
        """
        try:
            response = requests.get("%s/user_phone/%s" % (cls.USERS_ENDPOINT, user_phone),
                        timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            user = None

            if response.status_code == 200:
                user = User.build_from_json(json_payload)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user

    @classmethod
    def get_user_by_social_number(cls, user_social_number: str) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user social_number.
        :param user_social_number: the user social_number
        :return: User obj with social_number=user_social_number
        """
        try:
            response = requests.get("%s/user_social_number/%s" % (cls.USERS_ENDPOINT, user_social_number),
                        timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            user = None

            if response.status_code == 200:
                user = User.build_from_json(json_payload)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user

    @classmethod
    def get_all_positive_customer(cls) -> [User]:
        """
        This method contacts the users microservice
        and retrieves all positive customers.
        :return: A list of User obj with health_status = True
        """
        try:
            response = requests.get("%s/positive_customers" % (cls.USERS_ENDPOINT),
                        timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            pos_customers = []

            if response.status_code == 200:
                #TODO append in pos_customers all item of the json_payload
                for json in json_payload:
                    pos_customers.append(User.build_from_json(json))
                return pos_customers

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return None

    @classmethod
    def add_social_number(cls, user_id: int, social_number:str):
        """
        This method contacts the users microservice
        to add the social number for a customer
        :param user_id: the user id
        :return: User updated
        """
        try:
            response = None
            url = "%s/social_number/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.put(url,
                                json={
                                    'social_number': social_number
                                },
                                timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def create_customer(cls, type: str, 
                        email:str, password:str, social_number:str,
                        firstname: str, lastname: str,
                        birthdate, phone:str):
        try:
            url = "%s/customer" % (cls.USERS_ENDPOINT)
            response = requests.post(url,
                                    json={
                                        'type': 'customer',
                                        'email': email, 
                                        'password': password,
                                        'social_number': social_number,
                                        'firstname': firstname,
                                        'lastname': lastname,
                                        'birthdate': birthdate,
                                        'phone': phone
                                    },
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                    )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def create_operator(cls, type: str, email:str, password:str):
        try:
            url = "%s/operator" % (cls.USERS_ENDPOINT)
            response = requests.post(url, 
                                    json={
                                        'type': 'operator',
                                        'email': email, 
                                        'password': password
                                    },
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                    )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def update_customer(cls, user_id: int, email:str, password:str, phone:str):
        """
        This method contacts the users microservice
        to allow the customers to update their profiles
        :param user_id: the customer id
            email: the customer email
            password: the customer password
            phone: the customer phone
        :return: User updated
        """
        try:
            url = "%s/customer/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.put(url,
                                json={
                                    'email': email,
                                    'password': password,
                                    'phone': phone
                                },
                                timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                )
            return response

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        raise RuntimeError('Error with searching for the user %s' % user_id)
    
    @classmethod
    def update_operator(cls, user_id: int, email:str, password:str):
        """
        This method contacts the users microservice
        to allow the operators to update their profiles
        :param user_id: the operator id
            email: the operator email
            password: the operator password
            phone: the operator phone
        :return: User updated
        """
        try:
            url = "%s/operator/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.put(url,
                                json={
                                    'email': email,
                                    'password': password,
                                },
                                timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                )
            return response
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        raise RuntimeError('Error with searching for the user %s' % user_id)

    @classmethod
    def update_health_status(cls, user_id: int):
        """Mark a customer as positive

        Args:
            user_id (int)

        Returns:
            PUT response
        """
        try:
            url = "%s/mark_positive/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.put(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def delete_user(cls, user_id: int):
        """
        This method contacts the users microservice
        to delete the account of the user
        :param user_id: the user id
        :return: User updated
        """
        try:
            logout_user()
            url = "%s/user/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def authenticate_user(cls, email: str, password: str) -> User:
        """
        This method authenticates the user trough users AP
        :param email: user email
        :param password: user password
        :return: None if credentials are not correct, User instance if credentials are correct.
        """
        payload = dict(email=email, password=password)
        try:
            response = requests.post('%s/authenticate' % cls.USERS_ENDPOINT, 
                                        json=payload, 
                                        timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                    )
            json_response = response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

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
