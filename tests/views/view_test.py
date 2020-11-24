import unittest
from flask import template_rendered
from contextlib import contextmanager


class ViewTest(unittest.TestCase):

    BASE_URL = "http://localhost"

    @classmethod
    def setUpClass(cls):
        from gooutsafe import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.config['LOGIN_DISABLED'] = True

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
