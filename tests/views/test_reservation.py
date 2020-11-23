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

    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_create_reservation_get(self, mock_get):
        mock_get.return_value = Mock(status_code=200, 
                                    json = lambda:{
                                        'restaurant_sheet':{
                                            'restaurant':{
                                                'tables':{},
                                                'availabilities': {},
                                            },
                                        },
                                    })
        data = { 
            'restaurant_name': 'Pizza da Musca',
        }
        with self.captured_templates(self.app) as templates:
            response = self.client.get(
                '/create_reservation/'+str(1),
                json=data,
                follow_redirects=False
            )
            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_reservation.html' 
        
        pass

    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_reservation_post_success(self, mock_post, mock_get):
        pass

    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_reservation_post_error(self, mock_post, mock_get):
        pass

    def test_reservation_all(self):
        pass

    def test_delete_reservation(self):
        pass

    def test_edit_reservation(self):
        pass

    def test_customer_my_reservation(self):
        pass

    def test_confirm_reservation(self):
        pass

    def test_my_reservations(self):
        pass
