from unittest.mock import Mock, patch
from flask import current_app
from faker import Faker
from random import randint, choice
from werkzeug.exceptions import HTTPException
import requests

from gooutsafe.auth.user import User
from .rao_test import RaoTest


class TestUserManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestUserManager, self).setUp()
        from gooutsafe.rao.user_manager import UserManager
        self.user_manager = UserManager
        from gooutsafe import app
        self.app = app

    def generate_user(self, type):
        if type == 'customer':
            extra_data = {
            'firstname': "Mario",
            'lastname': "Rossi",
            'birthdate': TestUserManager.faker.date(),
            'social_number': TestUserManager.faker.ssn(),
            'health_status': choice([True, False]),
            'phone': TestUserManager.faker.phone_number()
            }
        else:
            extra_data = {}

        data = {
            'id': randint(0,999), 
            'email': TestUserManager.faker.email(),
            'is_active' : choice([True,False]),
            'authenticated': choice([True,False]),
            'is_anonymous': False,
            'type': choice(['customer', 'operator']),
            'extra': extra_data,
        }
        user = User(**data)
        if type == 'customer':
            user.type = 'customer'
        elif type == 'operator':
            user.type ='operator'
            
        return user

    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_get_user_by_id(self, mock_get):
        user = self.generate_user(type='generic')
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'authenticated': False,
                'is_anonymous': False,
                'type': user.type
            }
        )
        response = self.user_manager.get_user_by_id(id)
        assert response is not None

    def test_get_user_by_id_error(self):
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_user_by_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_get_user_by_email(self, mock_get):
        user = self.generate_user(type='customer')
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'authenticated': False,
                'is_anonymous': False,
                'type': user.type
            }
        )
        response = self.user_manager.get_user_by_email(user.email)
        assert response is not None
    
    def test_get_user_by_email_error(self):
        email = TestUserManager.faker.email()
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_user_by_email(email)
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_get_user_by_phone(self, mock_get):
        user = self.generate_user(type='customer')
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'authenticated': False,
                'is_anonymous': False,
                'type': user.type
            }
        )
        response = self.user_manager.get_user_by_phone(user.phone)
        assert response is not None

    def test_get_user_by_phone_error(self):
        phone = TestUserManager.faker.phone_number()
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_user_by_phone(phone)
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_get_user_by_social_number(self, mock_get):
        user = self.generate_user(type='customer')
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'authenticated': False,
                'is_anonymous': False,
                'type': user.type
            }
        )
        response = self.user_manager.get_user_by_social_number(user.social_number)
        assert response is not None

    def test_get_user_by_social_number_error(self):
        ssn = TestUserManager.faker.ssn()
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_user_by_social_number(ssn)
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_get_all_positive_customer(self, mock_get):
        pass
    
    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_add_social_number(self, mock_get):
        user = self.generate_user(type='customer')
        mock_get.return_value = Mock(status_code=200)
        response = self.user_manager.add_social_number(user.id, user.social_number)
        assert response is not None

    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_customer(self, mock_get):
        user = self.generate_user(type='customer')
        mock_get.return_value = Mock(status_code=200)
        password = TestUserManager.faker.password()
        response = self.user_manager.create_customer(
            type="customer", email=user.email, password=password,
            social_number=user.social_number, firstname=user.firstname,
            lastname=user.lastname, birthdate=user.birthdate,
            phone=user.phone
        )
        assert response is not None
        
    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_operator(self, mock_get):
        user = self.generate_user(type='operator')
        mock_get.return_value = Mock(status_code=200)
        password = TestUserManager.faker.password()
        response = self.user_manager.create_operator(
            type="operator", email=user.email, password=password
        )
        assert response is not None

    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_customer(self, mock_put):
        user = self.generate_user(type='customer')
        mock_put.return_value = Mock(
            status_code = 200,
            json=lambda : {
                'status': 'success',
                'message': 'Updated'
            }
        )
        password = TestUserManager.faker.password()
        response = self.user_manager.update_customer(
            user_id=user.id, email=user.email, password=password, phone=user.phone
        )

        assert response is not None

    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_operator(self, mock_put):
        user = self.generate_user(type='operator')
        mock_put.return_value = Mock(
            status_code = 204,
            json=lambda : {
                'status': 'success',
                'message': 'Updated'
            }
        )
        password = TestUserManager.faker.password()
        response = self.user_manager.update_operator(
            user_id=user.id, email=user.email, password=password
        )
        assert response is not None

    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_health_status(self, mock_get):
        pass
    
    @patch('gooutsafe.rao.user_manager.requests.delete')
    def test_delete_user(self, mock_get):
        user = self.generate_user(type='generic')
        mock_get.return_value = Mock(status_code=200)        

        with self.app.test_request_context ():
            response = self.user_manager.delete_user(user_id=user.id)            
            assert response is not None

    def test_delete_user_error(self):
        with self.app.test_request_context ():
            with self.assertRaises(HTTPException) as http_error:
                self.user_manager.delete_user(user_id=randint(0,999))
                self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_authenticate_user(self, mock_get):        
        user = self.generate_user(type='generic')
        user_data = {
            'id':user.id,
            'email':user.email,
            'is_active': False,
            'authenticated': False,
            'is_anonymous': False,
            'type': user.type
        }
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'user': user_data
            }
        )
        password = TestUserManager.faker.password()
        response = self.user_manager.authenticate_user(
            email=user.email, password=password
        )
        assert response is not None
