import unittest
from flask import template_rendered
from contextlib import contextmanager
from faker import Faker
from gooutsafe.auth.user import User
from random import choice, randint
from flask_login import login_user

class ViewTest(unittest.TestCase):
    faker = Faker()

    BASE_URL = "http://localhost"

    @classmethod
    def setUpClass(cls):
        from gooutsafe import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        from gooutsafe.rao.user_manager import UserManager
        cls.user_manager = UserManager
    

    def login_test_customer(self):
        """
        Simulate the customer login for testing the views with @login_required
        :return: customer
        """
        customer = self.generate_user('customer')
        response = self.user_manager.create_customer(
                'customer',
                customer.get('email'),
                customer.get('password'),
                customer.get('social_number'),
                customer.get('firstname'),
                customer.get('lastname'),
                customer.get('birthdate'),
                customer.get('phone')
                )

        rv = self.client.post (
            self.BASE_URL+'/login',
            json=customer
        )
        return customer

    def login_test_operator(self):
        """
        Simulate the operator login for testing the views with @login_required
        :return: operator
        """
        operator = self.generate_user('operator')
        response = self.user_manager.create_operator(
                operator.get('email'),
                operator.get('password'),
                )

        rv = self.client.post (
            self.BASE_URL+'/login',
            json=operator
        )
        return operator
    #it has to be fixed
    def login_test_authority(self):
        """
        Simulate the operator login for testing the views with @login_required
        :return: operator
        """
        authority = self.user_manager.get_user_by_email("aslpisa@asl.it")
        #authority exists in users ms db
        if authority is None:
            #create authority
            self.user_manager.create_authority()
            authority = self.user_manager.get_user_by_email("aslpisa@asl.it")
        #login authority
        rv = self.client.post (
            self.BASE_URL+'/login',
            json={"email": "aslpisa@asl.it", "password": "aslpisa"}
        )
        return authority
    
    def generate_user(self, user_type):
        """Generates a random user, depending on the type

        Args:
            user_type (str): type of the user to be created

        Returns:
            (dict): a dictionary with the user's data
        """
        if user_type == 'customer':
            data = {
                'id': randint(0,999),
                'email': self.faker.email(),
                'password': self.faker.password(),
                'is_active' : choice([True,False]),
                'authenticated': False,
                'is_anonymous': False,
                'type': user_type,
                'firstname': self.faker.first_name(),
                'lastname': self.faker.last_name(),
                'birthdate': self.faker.date(),
                'health_status_change_datetime': self.faker.date(),
                'social_number': self.faker.ssn(),
                'health_status': choice([True, False]),
                'phone': self.faker.phone_number()
            }
        elif user_type == 'authority':
            data = {
                'id': randint(0,999),
                'email': "aslpisa@asl.it",
                'password': "aslpisa",
                'is_active' : choice([True,False]),
                'authenticated': False,
                'is_anonymous': False,
                'type': user_type,
                'name': self.faker.company(),
                'city': self.faker.city(),
                'address': self.faker.address(),
                'phone': self.faker.phone_number()
            }
        else:
            data = {
                'id': randint(0,999),
                'email': self.faker.email(),
                'password': self.faker.password(),
                'is_active' : choice([True,False]),
                'authenticated': False,
                'is_anonymous': False,
                'type': user_type
            }
        return data
