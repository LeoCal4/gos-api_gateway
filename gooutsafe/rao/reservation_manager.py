from gooutsafe import app
from gooutsafe.auth.user import User
from .restaurant_manager import RestaurantManager
import requests
from flask import abort


class ReservationManager:
    RESERVATION_ENDPOINT = app.config['RESERVATIONS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']
    """
    Reservation Manager RAO
    """

    @classmethod
    def create_reservation(cls, restaurant_id, user_id, start_time, people_number):
        url = "%s/reservation/" % cls.RESERVATION_ENDPOINT
        json_tables, json_times, _ = cls.get_restaurant_detatils(restaurant_id)
        try:
            response = requests.post(url,
                                     json={
                                         'user_id': user_id,
                                         'restaurant_id': restaurant_id,
                                         'start_time': start_time,
                                         'people_number': people_number,
                                         'tables': json_tables,
                                         'times': json_times
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    @classmethod
    def get_all_reservation_restaurant(cls, restaurant_id):
        url = "%s/reservation/restaurant/%s" % (cls.RESERVATION_ENDPOINT, restaurant_id)
        try:
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    @classmethod
    def get_all_reservation_customer(cls, customer_id):
        url = "%s/reservation/customer/%s" % (cls.RESERVATION_ENDPOINT, customer_id)
        try:
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    @classmethod
    def get_reservation(cls, reservation_id):
        url = "%s/reservation/customer/%s" % (cls.RESERVATION_ENDPOINT, reservation_id)
        try:
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    @classmethod
    def edit_reservation(cls, reservation_id, restaurant_id, start_time, people_number):
        url = "%s/reservation/%s" % (cls.RESERVATION_ENDPOINT, str(reservation_id))
        json_tables, json_times, _ = cls.get_restaurant_detatils(restaurant_id)
        try:
            response = requests.put(url,
                                    json={
                                        'start_time': start_time,
                                        'people_number': people_number,
                                        'tables': json_tables,
                                        'times': json_times
                                    },
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    @classmethod
    def confirm_reservation(cls, reservation_id):
        url = "%s/reservation/confirm/%s" % (cls.RESERVATION_ENDPOINT, str(reservation_id))
        try:
            response = requests.put(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    @classmethod
    def filtered_reservations(cls, restaurant_id, start_time, end_time):
        url = "%s/reservation/dates/" % (cls.RESERVATION_ENDPOINT)
        try:
            response = requests.post(url,
                                     json={
                                         'restaurant_id': restaurant_id,
                                         'start_time': start_time,
                                         'end_time': end_time,
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    @classmethod
    def delete_reservation(cls, reservation_id):
        url = "%s/reservation/%s" % (cls.RESERVATION_ENDPOINT, str(reservation_id))
        try:
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return response

    # Helper Methods
    @classmethod
    def get_restaurant_detatils(cls, restaurant_id):
        json_details = {}
        json_tables = {}
        json_times = {}
        try:
            res = RestaurantManager.get_restaurant_sheet(restaurant_id)
            print(res)
            json_details = res
            json_tables = res['restaurant']['tables']
            json_times = res['restaurant']['availabilities']
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return json_tables, json_times, json_details
