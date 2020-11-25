import requests
from flask import abort
from gooutsafe import app
from gooutsafe.auth.user import User


class RestaurantManager:
    """
    Restaurant Manager RAO
    """

    RESTAURANTS_MS_URL = app.config['RESTAURANTS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_restaurant_sheet(cls, restaurant_id: int):
        """Requests the restaurant sheet of the restaurant linked 
        to the restaurant_id

        Args:
            restaurant_id (int): restaurant's unique identifier

        Returns:
            None: the Restaurant MS doesn't have the restaurant
            Restaurant sheet: the requests is successful
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/%s" % (cls.RESTAURANTS_MS_URL, restaurant_id)
            res = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_data = res.json()
            if res.status_code != 200:
                print(json_data['message'])
                return None
            return json_data['restaurant_sheet']
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
    
    @classmethod
    def get_restaurant_by_op_id(cls, op_id: int):
        """Requests the restaurant sheet of the restaurant owned
        by the operator specified by the op_id

        Args:
            op_id (int): operator's unique identifier

        Returns:
            None: the Restaurant MS doesn't have the restaurant
            Restaurant sheet: the requests is successful
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/by_operator_id/%s" % (cls.RESTAURANTS_MS_URL, op_id)
            res = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_data = res.json()
            if res.status_code != 200:
                print(json_data['message'])
                return None
            return json_data['restaurant_sheet']
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
    
    @classmethod
    def put_toggle_like(cls, restaurant_id: int, user_id: int):
        """Requests a toggle on the like of the restaurant linked to restaurant_id, 
        from the user_id

        Args:
            restaurant_id (int): 
            user_id (int): 

        Returns:
            False: if the Restaurant MS could not toggle the like
            True: the request was accepted successfully
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/like/%s" % (cls.RESTAURANTS_MS_URL, restaurant_id)
            res = requests.put(url, json={'user_id': user_id}, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_data = res.json()
            if res.status_code != 200:
                print(json_data['message'])
                return False
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def post_add(cls, json_data: dict):
        """Handles the post request needed to create a new restaurant

        Args:
            json_data (dict): the restaurant data to be sent in the request

        Returns:
            None: if the Restaurant MS could not create the restaurant
            restaurant_id: the request was accepted successfully
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant" % cls.RESTAURANTS_MS_URL
            res = requests.post(url, json=json_data, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                print(res.json()['message'])
                return None
            return res.json()['restaurant_id']
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def post_add_tables(cls, restaurant_id: int, json_post_data: dict):
        """Handles the post request needed to add new tables to the restaurant
        linked to restaurant_id

        Args:
            restaurant_id (int)
            json_post_data (dict): data that specify the tables to add

        Returns:
            False: if the Restaurant MS could add the tables
            True: the request was accepted successfully
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/tables/%d" % (cls.RESTAURANTS_MS_URL, restaurant_id)
            res = requests.post(url, json=json_post_data, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                print(res.json()['message'])
                return False
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def post_add_time(cls, rest_id: int, json_data_to_send: dict):
        """Handles the post request needed to add availabilities to the restaurant
        linked to restaurant_id

        Args:
            restaurant_id (int)
            json_post_data (dict): data that specify the availability to add

        Returns:
            False: if the Restaurant MS could add the availability
            True: the request was accepted successfully
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/time/%d" % (cls.RESTAURANTS_MS_URL, rest_id)
            res = requests.post(url, json=json_data_to_send, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                print(res.json()['message'])
                return False
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def put_add_measure(cls, rest_id: int, json_data_to_send: dict):
        """Handles the put request needed to add safety measures to the restaurant
        linked to restaurant_id

        Args:
            restaurant_id (int)
            json_post_data (dict): data that specify the safety measure to add

        Returns:
            False: if the Restaurant MS could add the safety measure
            True: the request was accepted successfully
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/measure/%d" % (cls.RESTAURANTS_MS_URL, rest_id)
            res = requests.put(url, json=json_data_to_send, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                print(res.json()['message'])
                return False
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def put_add_avg_stay(cls, rest_id: int, json_data_to_send: dict):
        """Handles the put request needed to add the average stay time to 
        the restaurant linked to restaurant_id

        Args:
            restaurant_id (int)
            json_post_data (dict): data that specify the average stay time to add

        Returns:
            False: if the Restaurant MS could add the average stay time
            True: the request was accepted successfully
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/avg_stay/%d" % (cls.RESTAURANTS_MS_URL, rest_id)
            res = requests.put(url, json=json_data_to_send, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                print(res.json()['message'])
                return False
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def put_edit_restaurant(cls, rest_id: int, json_data_to_send: dict):
        """Handles the put request needed to add edit the restaurant
        linked to restaurant_id

        Args:
            restaurant_id (int)
            json_post_data (dict): data that specify the average stay time to add

        Returns:
            False: if the Restaurant MS could edit the restaurant
            True: the request was accepted successfully
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/%d" % (cls.RESTAURANTS_MS_URL, rest_id)
            res = requests.put(url, json=json_data_to_send, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                print(res.json()['message'])
                return False
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def get_get_all(cls):
        """Handles the get request to return all the resturants

        Returns:
            A json containing all the restaurants
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            res = requests.get('%s/restaurant/all' % cls.RESTAURANTS_MS_URL, 
                                timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                print(res.json()['message'])
                return None
            return res.json()['restaurants']
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def get_search_by(cls, search_filter: str, search_field: str):
        """Handles the get request to search for restaurants

        Args:
            search_filter (str): one of the possible filters for the search
            search_field (str): the words searched by the user

        Returns:
            A json containing all the restaurants in the search
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            url = "%s/restaurant/search_by/%s/%s" % (cls.RESTAURANTS_MS_URL, search_filter, search_field)
            res = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code != 200:
                return None
            return res.json()['restaurants']
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def get_rating_bounds(cls):
        """Handles the get request to get the value bounds of 
        the ratings

        Returns:
            Bounds: the min and max values bounds for the ratings
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            res = requests.get('%s/restaurant/rating_bounds' % cls.RESTAURANTS_MS_URL,
                                timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            return res.json()['bounds']
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

    @classmethod
    def post_review(cls, json_data: dict):
        """Handles the post request to create a review

        Args:
            json_data (dict): the review data

        Returns:
            Tuple of True, already_written: if the request was successfull
            Tuple of False, None: if the review could not be added
            500 error page: in case of timeout or connection error with
                the Restaurant MS service 
        """
        try:
            res = requests.post('%s/restaurant/review' % cls.RESTAURANTS_MS_URL, json=json_data,
                                timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if res.status_code == 201 or res.status_code == 200:
                return (True, res.json()['already_written'])
            return (False, None)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
