from unittest.mock import Mock, patch
from .view_test import ViewTest
import requests
from werkzeug.exceptions import HTTPException
from flask import url_for
from faker import Faker
import requests

class TestHome(ViewTest):
    faker = Faker()

    BASE_URl = 'http://localhost'

    @classmethod
    def setUpClass(cls):
        super(TestHome, cls).setUpClass()

    def test_home(self):
        rv = self.client.get(self.BASE_URL)
        assert rv.status_code == 200

    def test_search_with_keyword(self):
        data = {'keyword': self.faker.company(), 'filters': ''}
        url = self.BASE_URL + '/search'
        rv = self.client.get(url, json=data)
        assert rv.status_code == 200

    def test_search_without_keyword(self):
        data = {'keyword': '', 'filters': ''}
        url = self.BASE_URL + '/search'
        rv = self.client.get(url, json=data)
        assert rv.status_code == 200

