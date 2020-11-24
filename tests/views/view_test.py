import unittest
from flask import template_rendered
from contextlib import contextmanager
from faker import Faker
from random import randint, choice

from gooutsafe.auth.user import User


class ViewTest(unittest.TestCase):

    BASE_URL = "http://localhost"

    @classmethod
    def setUpClass(cls):
        from gooutsafe import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()

    
    def generate_user(self, user_type):
        if user_type == 'customer':
            extra_data = {
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'birthdate': self.faker.date(),
            'social_number': self.faker.ssn(),
            'health_status': choice([True, False]),
            'phone': self.faker.phone_number()
            }
        elif user_type == 'authority':
            extra_data = {
            'name': self.faker.company(),
            'city': self.faker.city(),
            'address': self.faker.address(),
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
            'type': user_type,
            'extra': extra_data,
        }

        user = User(**data)            
        return user