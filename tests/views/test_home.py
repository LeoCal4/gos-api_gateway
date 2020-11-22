from unittest.mock import Mock, patch
from .view_test import ViewTest
import requests
from werkzeug.exceptions import HTTPException
from flask import url_for


class TestHome(ViewTest):

    @classmethod
    def setUpClass(self):
        super(TestHome, self).setUpClass()

    def test_home(self):
        with self.captured_templates(self.app) as templates:
            rv = self.client.get('/')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'index.html'

    def test_search(self):
        with self.captured_templates(self.app) as templates:
            rv = self.client.get('/search')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'explore.html'
