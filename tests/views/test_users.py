from unittest.mock import Mock, patch
from .view_test import ViewTest
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker
from random import randint, choice
import requests

from gooutsafe.auth.user import User


class TestUsers(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestUsers, cls).setUpClass()
        from gooutsafe.rao.user_manager import UserManager
        cls.user_manager = UserManager
        
    def generate_user(self, type):
        if type == 'customer':
            extra_data = {
            'firstname': "Mario",
            'lastname': "Rossi",
            'birthdate': self.faker.date(),
            'social_number': self.faker.ssn(),
            'health_status': choice([True, False]),
            'phone': self.faker.phone_number()
            }
        else:
            extra_data = {}

        data = {
            'id': randint(0,999), 
            'email': self.faker.email(),
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
            user.type = 'operator'
            
        return user

    
    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_operator_post_error(self, mock_post, mock_get):
        user = self.generate_user(type='operator')
        user_data = {
            'id': user.id, 
            'email': user.email,
            'is_active' : user.is_active,
            'authenticated': user.is_authenticated,
            'is_anonymous': False,
            'type': 'operator',
        }
        mock_get.return_value = Mock(
            status_code=200,
            json =  lambda : user_data
        )

        mock_post.return_value = Mock(
            status_code=200,
            json =  lambda : {
                'status': 'Already present'
            }
        )
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/create_user/'+ user.type,
                follow_redirects=False
            )

            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_user.html' 
    
    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_create_operator_get(self, mock_get):
        user = self.generate_user(type='operator')
        user_data = {
            'id': user.id, 
            'email': user.email,
            'is_active' : user.is_active,
            'authenticated': user.is_authenticated,
            'is_anonymous': False,
            'type': 'operator',
        }
        mock_get.return_value = Mock(status_code=200)
        with self.captured_templates(self.app) as templates:
            response = self.client.get(
                '/create_user/'+ user.type,
                follow_redirects=False
            )

            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_user.html' 

    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.post')
    def test_create_customer_post_error(self, mock_post, mock_get):
        user = self.generate_user(type='operator')
        user_data = {
            'id': user.id, 
            'email': user.email,
            'is_active' : user.is_active,
            'authenticated': user.is_authenticated,
            'is_anonymous': False,
            'type': 'operator',
        }
        mock_get.return_value = Mock(
            status_code=200,
            json =  lambda : user_data
        )

        mock_post.return_value = Mock(
            status_code=200,
            json =  lambda : {
                'status': 'Already present'
            }
        )
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/create_user/'+ user.type,
                follow_redirects=False
            )

            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_user.html' 

    @patch('gooutsafe.rao.user_manager.requests.get')
    def test_create_customer_get(self, mock_get):
        user = self.generate_user(type='customer')
        user_data = {
            'id': user.id, 
            'email': user.email,
            'is_active' : user.is_active,
            'authenticated': user.is_authenticated,
            'is_anonymous': False,
            'type': 'operator',
        }
        mock_get.return_value = Mock(status_code=200)
        with self.captured_templates(self.app) as templates:
            response = self.client.get(
                '/create_user/'+ user.type,
                follow_redirects=False
            )

            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_user.html'

    @patch('gooutsafe.rao.user_manager.requests.delete')
    def test_delete_user(self, mock_delete):
        user = self.generate_user(type='generic')
        mock_delete.return_value = Mock(
            status_code=202,
            json =  lambda : {
                'status': 'success',
                'message': 'Successfully deleted'
            }
        )
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/delete_user/'+str(user.id),
                follow_redirects=False
            )
            assert response is not None
            assert response.status_code == 302  

    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_customer_get(self, mock_put):
        user = self.generate_user(type='customer')
        mock_put.return_value = Mock(
            status_code=204,
            json=lambda:{
                'status': 'success',
                'message': 'Updated'
            }
        )
        data = { 
            'email': user.email, 
            'password': self.faker.password(),
            'phone': user.phone
        }   
        with self.captured_templates(self.app) as templates:
            response = self.client.get(
                '/update_customer/'+str(user.id),
                json=data,
                follow_redirects=False
            )
            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'update_customer.html' 
    
    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_customer_post(self, mock_put, mock_get):
        user = self.generate_user(type='customer')
        mock_put.return_value = Mock(
            status_code=204,
            json=lambda:{
                'status': 'success',
                'message': 'Updated'
            }
        )
        user_data = {
            'id':user.id,
            'email':user.email,
            'is_active': False,
            'authenticated': False,
            'is_anonymous': False,
            'type': user.type
        }
        mock_get.return_value = Mock(
            status_code=204,
            json=lambda : user_data
        )
        data = { 
            'email': user.email, 
            'password': self.faker.password() ,
            'phone': user.phone
        }   
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/update_customer/'+str(user.id),
                json=data,
                follow_redirects=False
            )
            assert response.status_code == 302

    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_customer_post_error(self, mock_put, mock_get):
        user = self.generate_user(type='customer')
        mock_put.return_value = Mock(
            status_code=204,
            json=lambda:{
                'status': 'success',
                'message': 'Updated'
            }
        )
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
            json=lambda : user_data
        )
        
        data = { 
            'email': user.email, 
            'password': self.faker.password(),
            'phone': user.phone
        }   
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/update_customer/'+str(user.id +1),
                json=data,
                follow_redirects=False
            )
            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'update_customer.html'

    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_operator_get(self, mock_put):
        user = self.generate_user(type='operator')
        mock_put.return_value = Mock(
            status_code=204,
            json=lambda:{
                'status': 'success',
                'message': 'Updated'
            }
        )
        data = { 
            'email': user.email, 
            'password': self.faker.password() 
        }   
        with self.captured_templates(self.app) as templates:
            response = self.client.get(
                '/update_operator/'+str(user.id),
                json=data,
                follow_redirects=False
            )
            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'update_customer.html' 
    
    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_operator_post(self, mock_put, mock_get):
        user = self.generate_user(type='operator')
        mock_put.return_value = Mock(
            status_code=204,
            json=lambda:{
                'status': 'success',
                'message': 'Updated'
            }
        )
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
            json=lambda : user_data
        )
        
        data = { 
            'email': user.email, 
            'password': self.faker.password() 
        }   
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/update_operator/'+str(user.id),
                json=data,
                follow_redirects=False
            )
            assert response.status_code == 302

    @patch('gooutsafe.rao.user_manager.requests.get')
    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_update_operator_post_error(self, mock_put, mock_get):
        user = self.generate_user(type='operator')
        mock_put.return_value = Mock(
            status_code=204,
            json=lambda:{
                'status': 'success',
                'message': 'Updated'
            }
        )
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
            json=lambda : user_data
        )
        
        data = { 
            'email': user.email, 
            'password': self.faker.password() 
        }   
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/update_operator/'+str(user.id +1),
                json=data,
                follow_redirects=False
            )
            assert response.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'update_customer.html'
    
    @patch('gooutsafe.rao.user_manager.requests.put')
    def test_add_social_number(self, mock_post):
        user = self.generate_user(type='customer')
        data = { 'social_number': user.social_number }

        mock_post.return_value = Mock(status_code=200)
            
        with self.captured_templates(self.app) as templates:
            response = self.client.post(
                '/add_social_number/'+str(user.id),
                json=data,
                follow_redirects=False
            )
            
            assert response is not None
            assert response.status_code == 302           