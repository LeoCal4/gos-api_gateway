from unittest.mock import Mock, patch
from flask import current_app
from faker import Faker
from random import randint, choice
from werkzeug.exceptions import HTTPException
import requests

from .rao_test import RaoTest


class TestNotificationManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestNotificationManager, self).setUp()
        from gooutsafe.rao.notification_tracing_manager import NotificationTracingManager
        self.notification_tracing_manager = NotificationTracingManager
        from gooutsafe import app
        self.app = app
    
    @patch('gooutsafe.rao.notification_tracing_manager.requests.get')
    def test_retrieve_by_target_user_id(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200
        )
        response = self.notification_tracing_manager.retrieve_by_target_user_id(
            randint(0,999)
        )
        assert response is not None
    
    @patch('gooutsafe.rao.notification_tracing_manager.requests.get')
    def test_retrieve_by_target_user_id_void(self, mock_get):
        mock_get.return_value = Mock(
            status_code=404
        )
        response = self.notification_tracing_manager.retrieve_by_target_user_id(
            randint(0,999)
        )
        assert response == []

    @patch('gooutsafe.rao.notification_tracing_manager.requests.get')
    def test_retrieve_by_target_user_id_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.notification_tracing_manager.retrieve_by_target_user_id(
                randint(0, 999)
            )
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.notification_tracing_manager.requests.get')
    def test_get_contact_tracing_list_void(self, mock_get):
        mock_get.return_value = Mock(
            status_code=404
        )
        response = self.notification_tracing_manager.get_contact_tracing_list(
            randint(0,999)
        )
        assert response == []

    @patch('gooutsafe.rao.notification_tracing_manager.requests.get')
    def test_get_contact_tracing_list_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.notification_tracing_manager.get_contact_tracing_list(
                randint(0, 999)
            )
            self.assertEqual(http_error.exception.code, 500)
    
    @patch('gooutsafe.rao.notification_tracing_manager.requests.post')
    def test_trigger_contact_tracing(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        response = self.notification_tracing_manager.trigger_contact_tracing(
            randint(0,990)
        )
        assert response is not None
    
    @patch('gooutsafe.rao.notification_tracing_manager.requests.post')
    def test_trigger_contact_tracing_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.notification_tracing_manager.trigger_contact_tracing(
                randint(0, 999)
            )
            self.assertEqual(http_error.exception.code, 500)