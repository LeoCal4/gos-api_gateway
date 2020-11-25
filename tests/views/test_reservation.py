from unittest.mock import Mock, patch
from .view_test import ViewTest
import requests
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker
from random import randint, choice
import datetime

class ReservationTest(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(ReservationTest, cls).setUpClass()
        from gooutsafe.rao.reservation_manager import ReservationManager
        cls.reservation_manager = ReservationManager
        from gooutsafe.rao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from .test_restaurants import TestRestaurantViews
        cls.test_restaurant = TestRestaurantViews()
        cls.test_restaurant.setUpClass()


    def test_create_reservation_get_as_operator(self):
        self.login_test_operator()
        url = self.BASE_URL + '/create_reservation/'+ str(1)
        response = self.client.get(url)
        assert response.status_code == 302

    def test_create_reservation_get_as_customer(self):
        rsp = self.generate_random_reservation()
        print(rsp)
        self.login_test_customer()
        data = { 
            'restaurant_name': 'Pizza da Musca',
        }
        url = self.BASE_URL + '/create_reservation/'+ str(1)
        response = self.client.get(url, json=data)
        assert response.status_code == 200

    def test_create_reservation_post(self):
        self.login_test_customer()
        start_date = "2020-11-30"
        start_time = "12:00"
        people_number = 1
        data = {'start_date': start_date,
                'start_time' : start_time,
                'people_number': people_number}
        url = self.BASE_URL + '/create_reservation/'+ str(1)
        response = self.client.post(url, json=data)
        assert response.status_code == 302


    def test_reservation_all_get(self):
        url = self.BASE_URL + '/reservations/'+ str(1)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_reservation_all_post(self):
        customer = self.login_test_customer()
        restaurant = self.test_restaurant.create_random_restaurant(op_id=1)
        restaurant_id = restaurant['id']
        self.restaurant_manager.post_add_tables(restaurant_id, {'number':1,'max_capacity':4})
        day = 'Monday'
        start_time = '10:00:00'
        end_time = '20:00:00'
        ava_dict = {
            'day':day,
            'start_time':start_time,
            'end_time':end_time
        }
        self.restaurant_manager.post_add_time(restaurant['id'], ava_dict)
        rest = self.restaurant_manager.get_restaurant_sheet(restaurant_id)
        start_time = "2020-11-30 14:00:00"
        people_number = 1
        response = self.reservation_manager.create_reservation(restaurant_id, 1, start_time, people_number)
        filter_date = '2020-11-30'
        start_time = '00:00'
        end_time = '23:00'
        data = {
            'filter_date':filter_date,
            'start_time':start_time,
            'end_time':end_time
        }
        url = self.BASE_URL + '/reservations/'+ str(restaurant_id)
        response = self.client.post(url, json=data)
        assert response.status_code == 200

    def test_delete_reservation_customer(self):
        self.login_test_customer()
        url = self.BASE_URL + '/reservation/delete/' + str(1) + '/' + str(0) 
        response = self.client.get(url)
        assert response.status_code == 302

    def test_delete_reservation_restaurant(self):
        self.login_test_operator()
        url = self.BASE_URL + '/reservation/delete/' + str(1) + '/' + str(0) 
        response = self.client.get(url)
        assert response.status_code == 302

    def test_edit_reservation_get(self):
        self.login_test_customer()
        url = self.BASE_URL + '/reservation/edit/' + str(1) + '/' + str(0) 
        response = self.client.get(url)
        assert response.status_code == 302

    def test_edit_reservation_post(self):
        self.login_test_customer()
        start_date = "2020-11-30"
        start_time = "12:00"
        people_number = 1
        data = {'start_date': start_date,
                'start_time' : start_time,
                'people_number': people_number}
        url = self.BASE_URL + '/reservation/edit/' + str(1) + '/' + str(0) 
        response = self.client.post(url, json=data)
        assert response.status_code == 302


    def test_confirm_reservation_success(self):
        url = self.BASE_URL + '/reservation/confirm/' + str(1) + '/' + str(0) 
        response = self.client.get(url)
        assert response.status_code == 302

    def test_my_reservations(self):
        self.login_test_operator()
        url = self.BASE_URL + '/my_reservations'
        response = self.client.get(url)
        assert response.status_code == 200

#   <------- Helper Methods -------->

    def generate_random_reservation(self, restaurant_id=None, user_id=None):
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if restaurant_id is None:
            restaurant = self.test_restaurant.create_random_restaurant(op_id=1)
            restaurant_id = restaurant['id']
            self.restaurant_manager.post_add_tables(restaurant_id, {'number':4,'max_capacity':4})
            for day in week_days:
                start_time = '10:00:00'
                end_time = '20:00:00'
                ava_dict = {
                    'day':day,
                    'start_time':start_time,
                    'end_time':end_time
                }
                self.restaurant_manager.post_add_time(restaurant['id'], ava_dict)
        else:
            restaurant_id = restaurant_id
        if user_id is None:
            user_id = self.faker.random_int(min=1, max=999)
        else:
            user_id = user_id
        month = self.faker.random_int(min=1, max=12)
        day = self.faker.random_int(min=1, max=30)
        hour = self.faker.random_int(min=10, max=20)
        start_time = datetime.datetime(year=2020, month=month, day=day, hour=hour)
        start_time_str = datetime.datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S")
        people_number = self.faker.random_int(min=1, max=4)
        response = self.reservation_manager.create_reservation(restaurant_id, user_id, start_time_str, people_number)
        return response
