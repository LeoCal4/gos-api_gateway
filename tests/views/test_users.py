from unittest.mock import Mock, patch
from .view_test import ViewTest
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker
import requests


class TestUsers(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestUsers, cls).setUpClass()
        from gooutsafe.rao.user_manager import UserManager
        cls.user_manager = UserManager
        

    """
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
    
    def test_create_customer_get(self, mock_get):
        user = self.login_test_customer()
        data = {
            'email': user.email, 
            'password': user.password,
            'phone': user.phone
        }
        rv = self.client.get(
            self.BASE_URL+'/create_user/'+ user.type, 
            json=data, 
            follow_redirects=False
        )
        assert response.status_code == 200
    """
    def test_delete_user(self):
        user = self.login_test_customer()
        rv = self.client.get(
            self.BASE_URL+'/delete_user/'+str(user.get("id")), 
            follow_redirects=False
        )
        assert rv.status_code == 302
    
    def test_update_customer_get(self):
        user = self.login_test_customer()
        data = {
            'email': user.get("email"), 
            'password': user.get("password"),
            'phone': user.get("phone")
        }
        rv = self.client.get(
            self.BASE_URL+'/update_customer/'+str(user.get("id")), 
            json=data,
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_update_customer_post(self):
        user = self.login_test_customer()
        data = {
            'email': user.get("email"), 
            'password': user.get("password"),
            'phone': user.get("phone")
        }
        rv = self.client.post(
            self.BASE_URL+'/update_customer/'+str(user.get("id")), 
            json=data, 
            follow_redirects=False
        )
        assert rv.status_code == 200

    def test_update_customer_post_error(self):
        user = self.login_test_customer()
        data = {
            'email': user.get("email"), 
            'password': user.get("password"),
            'phone': user.get("phone")
        }
        rv = self.client.post(
            self.BASE_URL+'/update_customer/'+str(user.get("id")+1), 
            json=data, 
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_update_operator_get(self):
        user = self.login_test_operator()
        data = {
            'email': user.get("email"), 
            'password': user.get("password")
        }
        rv = self.client.get(
            self.BASE_URL+'/update_operator/'+str(user.get("id")), 
            json=data, 
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_update_operator_post(self):
        user = self.login_test_operator()
        data = {
            'email': user.get("email"), 
            'password': user.get("password")
        }
        rv = self.client.post(
            self.BASE_URL+'/update_operator/'+str(user.get("id")), 
            json=data, 
            follow_redirects=False
        )
        assert rv.status_code == 200

    def test_update_operator_post_error(self):
        user = self.login_test_operator()
        data = {
            'email': user.get("email"), 
            'password': user.get("password")
        }
        response = self.client.post(
            self.BASE_URL+'/update_operator/'+str(user.get("id") +1),
            json=data,
            follow_redirects=False
        )
        assert response.status_code == 200
    
    def test_add_social_number(self):
        user = self.login_test_customer()
        rv = self.client.post(
            self.BASE_URL+'/add_social_number/'+str(user.get("id")), 
            json={ 'social_number': user.get("social_number") },
            follow_redirects=False
        )
        assert rv.status_code == 302         