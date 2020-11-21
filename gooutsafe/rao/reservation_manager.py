from gooutsafe import app
from gooutsafe.auth.user import User
import requests

class ReservationManager:
    RESERVATION_ENDPOINT = app.config['RESERVATION_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']
    """
    Reservation Manager RAO
    """

    @classmethod
    def create_reservation(cls, restaurant_id, user_id, start_time, people_number):
        url = "%s/reservation/" % (cls.RESERVATION_ENDPOINT)
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
        except requests.exceptions.ConnectionError:
            return abort(500)
        except requests.exceptions.Timeout:
            return abort(500)
        return response


    @classmethod
    def get_all_reservation_restaurant(cls, restaurant_id):
        url = "%s/reservation/restaurant/%s" % (cls.RESERVATION_ENDPOINT, restaurant_id)
        try:
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except requests.exceptions.ConnectionError:
            return abort(500)
        except requests.exceptions.Timeout:
            return abort(500)
        return response

    @classmethod
    def get_all_reservation_customer(cls, customer_id):
        url = "%s/reservation/customer/%s" % (cls.RESERVATION_ENDPOINT, customer_id)
        try:
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except requests.exceptions.ConnectionError:
            return abort(500)
        except requests.exceptions.Timeout:
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
        except requests.exceptions.ConnectionError:
            return abort(500)
        except requests.exceptions.Timeout:
            return abort(500)        
        return response

    @classmethod
    def confirm_reservation(cls, reservation_id):
        url = "%s/reservation/%s" % (cls.RESERVATION_ENDPOINT, str(reservation_id))
        pass

    @classmethod    
    def filtered_reservations(cls, start_time, end_time):
        url = "%s/reservation/dates/" % (cls.RESERVATION_ENDPOINT)
        try:
            response = requests.put(url,
                                    json={
                                        'start_time': start_time,
                                        'people_number': people_number, 
                                        'tables': json_tables,
                                        'times': json_times
                                    },
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except requests.exceptions.ConnectionError:
            return abort(500)
        except requests.exceptions.Timeout:
            return abort(500)        
        return response 

    @classmethod
    def delete_reservation(cls, reservation_id):
        url = "%s/reservation/%s" % (cls.RESERVATION_ENDPOINT, str(reservation_id))
        try:
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except requests.exceptions.ConnectionError:
            return abort(500)
        except requests.exceptions.Timeout:
            return abort(500)        
        return response

# Helper Methods
    @classmethod
    def get_restaurant_detatils(cls,restaurant_id):
        RESTA_MS_URL = app.config['RESTA_MS_URL']
        url = "%s/restaurants/restaurant_details/%s" % (RESTA_MS_URL, str(restaurant_id))
        json_details = {}            
        json_tables = {}
        json_times = {}        
        try:
            res = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            payload = res.json()
            if res.status_code != 200:
                return None
            json_details = payload['details']            
            json_tables = json_details['tables']
            json_times = json_details['times']
        except requests.exceptions.ConnectionError:
            return abort(500)
        except requests.exceptions.Timeout:
            return abort(500)    
        return json_tables, json_times, json_details

