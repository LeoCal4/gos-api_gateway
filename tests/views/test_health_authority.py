from unittest.mock import Mock, patch
from .view_test import ViewTest
import requests
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker
from random import randint, choice
import datetime

class HealthAuthority(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(HealthAuthority, cls).setUpClass()
        from gooutsafe.rao.reservation_manager import ReservationManager
        cls.reservation_manager = ReservationManager
        from gooutsafe.rao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from gooutsafe.rao.user_manager import UserManager
        cls.user_manager = UserManager
        from .test_restaurants import TestRestaurantViews
        cls.test_restaurant = TestRestaurantViews()
        cls.test_restaurant.setUpClass()


    def test_search_customer_as_customer(self):
        self.login_test_customer()
        url = self.BASE_URL + '/ha/search_customer'
        response = self.client.post(url)
        assert response.status_code == 200

    def test_search_customer_success(self):
        customer = self.login_test_customer()
        customer = self.user_manager.get_user_by_email(customer['email'])
        user_id = customer.id
        print(customer)
        authority = self.login_test_authority()
        url = self.BASE_URL + '/ha/search_customer'
        #search by SSN
        SSN = 'FORZAMUSCA123456'
        self.user_manager.add_social_number(user_id, SSN)
        track_type = 'SSN'
        data = {
            'track_type': track_type,
            'customer_ident':SSN
        }
        response = self.client.post(url, json = data)
        assert response.status_code == 302
        #search by email
        track_type = 'Email'
        customer_ident = customer.email
        data = {
            'track_type': track_type,
            'customer_ident':customer_ident
        }
        response = self.client.post(url, json = data)
        assert response.status_code == 302
        #search by phone
        track_type = 'SSN'
        customer_ident = customer.phone
        data = {
            'track_type': track_type,
            'customer_ident':customer_ident
        }
        response = self.client.post(url, json = data)
        assert response.status_code == 302

    def test_mark_positive(self):
        customer = self.login_test_customer()
        customer = self.user_manager.get_user_by_email(customer['email'])
        authority = self.login_test_authority()
        #mark as positive
        url = self.BASE_URL + '/ha/mark_positive/%s' % str(customer.id)
        response = self.client.post(url, follow_redirects=True)
        assert response.status_code == 200
        #customer is already positive
        response = self.client.post(url,follow_redirects=True)
        assert response.status_code == 200
        #contact tracing
        url = self.BASE_URL + '/ha/contact/%s' % str(customer.id)
        response = self.client.get(url,follow_redirects=True)
        assert response.status_code == 200

