from gooutsafe import app
from gooutsafe.auth.user import User
import requests

class ReservationManager:
    RESERVATION_ENDPOINT = app.config['RESERVATION_MS_URL']
    """
    Reservation Manager RAO
    """

    @classmethod
    def create_reservation(cls, restaurant_id: int, user_id: int, start_time: str, poeple_number: int):

        url = "%s/reservation/restaurants/create/%d" % (cls.RESERVATION_ENDPOINT, restaurant_id)
        json_tables, json_times = self.get_restaurant_detatils(restaurant_id)
        response = requests.post(url,
                                json={
                                    'restaurant_id': restaurant_id,
                                    'user_id': user_id,
                                    'start_time': start_time,
                                    'poeple_number': poeple_number, 
                                    'tables': json_tables,
                                    'times': json_times
                                })
        return response


    @classmethod
    def retrieve_by_customer_id(id):
        pass


# Helper Methods

    def get_restaurant_detatils(self,restaurant_id):
        RESTA_MS_URL = app.config['RESTA_MS_URL']
        url = "%s/restaurants/details/%s" % (RESTA_MS_URL, id_op)
        res = requests.get(url)
        payload = res.json()
        print(payload)
        if res.status_code != 200:
            return None
        json_details = payload['details']            
        json_tables = payload['tables']
        json_times = payload['times']
        return json_tables, json_times

