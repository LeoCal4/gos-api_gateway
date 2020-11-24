import unittest
from flask import template_rendered
from contextlib import contextmanager

from gooutsafe.auth.user import User


class ViewTest(unittest.TestCase):

    BASE_URL = "http://localhost"

    @classmethod
    def setUpClass(cls):
        from gooutsafe import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()

    
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