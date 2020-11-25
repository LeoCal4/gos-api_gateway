from unittest.mock import Mock, patch
from .view_test import ViewTest
import requests
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker
from random import randint, choice

class ReservationTest(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(ReservationTest, cls).setUpClass()
        from gooutsafe.rao.reservation_manager import ReservationManager
        cls.reservation_manager = ReservationManager


    def test_create_reservation_get_as_operator(self):
        self.login_test_operator()
        url = self.BASE_URL + '/create_reservation/'+ str(1)
        response = self.client.get(url)
        assert response.status_code == 302

    def test_create_reservation_get_as_customer(self):
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
        url = self.BASE_URL + '/reservations/'+ str(1)
        response = self.client.post(url)
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
