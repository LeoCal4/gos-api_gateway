import unittest
from flask import template_rendered
from contextlib import contextmanager
from faker import Faker
from gooutsafe.auth.user import User


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
