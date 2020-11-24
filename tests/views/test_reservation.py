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
    """
    def test_create_reservation_get(self):
        data = { 
            'restaurant_name': 'Pizza da Musca',
        }
        url = self.BASE_URL + '/create_reservation/'+ str(1)
        response = requests.get(url, json=data)
        assert response.status_code == 200

        
    
    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_reservation_post_success(self, mock_post, mock_get):
        pass

    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_reservation_post_error(self, mock_post, mock_get):
        pass
    """

    def test_reservation_all_get(self):
        url = self.BASE_URL + '/reservations/'+ str(1)
        response = requests.get(url)
        assert response.status_code == 200

    def test_reservation_all_post(self):
        url = self.BASE_URL + '/reservations/'+ str(1)
        response = requests.post(url)
        assert response.status_code == 200

    def test_delete_reservation_customer(self):
        pass

    """
    def test_delete_reservation_restaurant(self):
        url = self.BASE_URL + '/reservation/delete/' + str(1) + '/' + str(0) 
        response = requests.post(url)
        assert response.status_code == 200
    """
    def test_edit_reservation(self):
        pass

    def test_customer_my_reservation(self):
        pass

    def test_confirm_reservation_success(self):
        url = self.BASE_URL + '/reservation/confirm/' + str(1) + '/' + str(0) 
        response = requests.get(url)
        print(response.url)
        print(response.status_code)
        assert response.status_code == 200

    def test_my_reservations(self):
        pass