from unittest.mock import Mock, patch
from .view_test import ViewTest
import requests
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker

class TestHome(ViewTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestHome, cls).setUpClass()

    def test_home(self):
        rv = self.client.get(self.BASE_URL+'/')
        print(rv)
        assert rv.status_code == 200

    def test_search_by(self):
        from gooutsafe.views.home import search_by
        search_filter = 'Name'
        search_field = TestHome.faker.company()
        with self.assertRaises(ValueError):
            self.assertIsNotNone(search_by(search_filter,search_field))




    def test_search_restaurant(self):
        url = self.BASE_URL + '/search'
        #search restaurant with name filter
        data = dict(keyword=TestHome.faker.company(), filters='Name')
        rv = self.client.get(url, query_string=data)
        assert rv.status_code == 200
        #search restaurant with city filter
        data = dict(keyword=TestHome.faker.city(), filters='City')
        rv = self.client.get(url, query_string=data)
        assert rv.status_code == 200
        #search restaurant with menu filter
        data = dict(keyword=TestHome.faker.country(), filters='Menu Type')
        rv = self.client.get(url, query_string=data)
        assert rv.status_code == 200
        #search restaurants with no keyword for the filters
        data = dict(keyword='', filters='Name')
        rv = self.client.get(url, query_string=data)
        assert rv.status_code == 200
        #search restaurants with no filters
        data = dict(keyword=TestHome.faker.company(), filters=None)
        rv = self.client.get(url, query_string=data)
        assert rv.status_code == 200
