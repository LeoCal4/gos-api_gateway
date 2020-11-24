import unittest
from flask import template_rendered
from contextlib import contextmanager
from faker import Faker
from gooutsafe.auth.user import User
from random import choice, randint


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

    @contextmanager
    def captured_templates(self, app):
        recorded = []
        def record(sender, template, context, **extra):
            recorded.append((template, context))
        template_rendered.connect(record, app)
        try:
            yield recorded
        finally:
            template_rendered.disconnect(record, app)
    
    def login_test_customer(self):
        """
        Simulate the customer login for testing the views with @login_required
        :return: customer
        """
        customer = generate_random_customer()
        psw = customer.password
        # create customer
        response = self.user_manager.create_customer(
                'customer',
                customer.email,
                customer.password,
                customer.social_number,
                customer.firstname,
                customer.lastname,
                customer.date,
                customer.phone
                )
        user = response.json()
        if user["status"] == "success":
            to_login = User.build_from_json(user["user"])
            login_user(to_login)
        data = {'email': customer.email, 'password': psw}
        return customer

    
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
