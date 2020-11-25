from unittest.mock import Mock, patch
from .view_test import ViewTest
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker
from random import randint, choice
import requests

from gooutsafe.auth.user import User


class TestReview(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestReview, cls).setUpClass()
        from gooutsafe.rao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from .test_restaurants import TestRestaurantViews
        cls.test_restaurant = TestRestaurantViews()
        cls.test_restaurant.setUpClass()


    def test_write_review_get(self):
        customer = self.login_test_customer()
        restaurant = self.test_restaurant.create_random_restaurant(1)
        response = self.client.get(
            '/restaurants/'+ str(randint(0,999))+'/review')
        assert response.status_code == 200

    def test_write_review_post(self):
        customer = self.login_test_customer()
        restaurant = self.test_restaurant.create_random_restaurant(1)
        review = {
            'customer_id': customer.get('id'),
            'restaurant_id': restaurant.get('id'),
            'customer_name': 'Leo',
            'value': 7,
            'review': 'Muscas'
        }

        response = self.client.post(
            '/restaurants/'+ str(restaurant['id']) +'/review', json=review)
        
        assert response.status_code == 200
