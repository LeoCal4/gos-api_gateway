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


    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_write_review_get(self, mock_get):
        data = {
            'status': 'Success',
            'message': 'Review already written',
            'bounds': {
                'min_value': 0, 
                'max_value': 10
            }
        }
        mock_get.return_value = Mock(
            status_code=200,
            json =  lambda : data
        )

        with self.captured_templates(self.app) as templates:
            response = self.client.get(
                '/restaurants/'+ str(randint(0,999))+'/review',
                follow_redirects=False
            )

            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_review.html'        