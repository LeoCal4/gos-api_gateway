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
        rv = requests.get(self.BASE_URl + '/')
        assert rv.status_code == 200

    def test_search_with_keyword(self):
        data = {'keyword': self.faker.company(), 'filters': ''}
        rv = requests.get('/search', query_string=data)
        assert rv.status_code == 200


"""
    def test_home(self):
        with self.captured_templates(self.app) as templates:
            rv = self.client.get('/')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'index.html'

    def test_search_with_keyword(self):
        with self.captured_templates(self.app) as templates:
            data = {'keyword': self.faker.company(), 'filters': ''}
            rv = self.client.get('/search', query_string=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'explore.html'

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_search_without_keyword(self, mock):
        with self.captured_templates(self.app) as templates:
            data = {'keyword': '', 'filters': ''}
            mock.return_value = Mock(status_code=200, json=lambda : {'message': 0, 
                        'restaurants': [{'name': 0, 'lat': 0, 'lon': 0}]})
            rv = self.client.get('/search', query_string=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'explore.html'
"""