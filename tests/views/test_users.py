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
    

    def test_create_operator_post(self):
        user = self.generate_user('operator')
        rv = self.client.post(
            '/create_user/'+ user.get("type"),
            json=user,
            follow_redirects=False
        )
        assert rv.status_code == 302

    def test_create_operator_get(self):
        user = self.login_test_operator()
        rv = self.client.get(
            '/create_user/'+ user.get("type"),
            follow_redirects=False
        )
        assert rv.status_code == 200

    def test_create_customer_post(self):
        user = self.login_test_customer()
        rv = self.client.post(
            '/create_user/'+ user.get("type"),
            json=user,
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_create_customer_get(self):
        user = self.login_test_customer()
        rv = self.client.get(
            self.BASE_URL+'/create_user/'+ user.get("type"), 
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_delete_user(self):
        user = self.login_test_customer()
        rv = self.client.get(
            self.BASE_URL+'/delete_user/'+str(user.get("id")), 
            follow_redirects=False
        )
        assert rv.status_code == 302
    
    def test_update_customer_get(self):
        user = self.login_test_customer()
        rv = self.client.get(
            self.BASE_URL+'/update_customer/'+str(user.get("id")), 
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_update_customer_post(self):
        user = self.login_test_customer()
        data = {
            'email': self.faker.email(), 
            'password': user.get("password"),
            'phone': user.get("phone")
        }
        rv = self.client.post(
            self.BASE_URL+'/update_customer/'+str(user.get("id")), 
            json=data, 
            follow_redirects=False
        )
        assert rv.status_code == 302

    def test_update_customer_post_error(self):
        user = self.login_test_customer()
        data = {
            'email': user.get("email"), 
            'password': user.get("password"),
            'phone': user.get("phone")
        }
        rv = self.client.post(
            self.BASE_URL+'/update_customer/'+str(0), 
            json=data, 
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_update_operator_get(self):
        user = self.login_test_operator()
        rv = self.client.get(
            self.BASE_URL+'/update_operator/'+str(user.get("id")), 
            follow_redirects=False
        )
        assert rv.status_code == 200
    
    def test_update_operator_post(self):
        user = self.login_test_operator()
        data = {
            'email': self.faker.email(), 
            'password': user.get("password")
        }
        rv = self.client.post(
            self.BASE_URL+'/update_operator/'+str(user.get("id")), 
            json=data, 
            follow_redirects=False
        )
        assert rv.status_code == 302

    def test_update_operator_post_error(self):
        user = self.login_test_operator()
        data = {
            'email': user.get("email"), 
            'password': user.get("password")
        }
        response = self.client.post(
            self.BASE_URL+'/update_operator/'+str(0),
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